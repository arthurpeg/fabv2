# Mise a jour automatique du bot sur le VPS (tache planifiee toutes les 5 minutes, voir live/README.md).
# 1. git fetch ; rien a faire si la branche locale est a jour.
# 2. Avance rapide seulement (jamais de fusion ni d'ecrasement de fichiers modifies a la main).
# 3. uv sync si pyproject.toml / uv.lock ont change.
# 4. Tests du bot (tests/test_live.py) : en cas d'echec, retour au commit precedent, le bot continue avec l'ancien code,
#    et ce commit n'est plus retente (live/etat/maj_refusee.txt) jusqu'au suivant.
# 5. Si le code du bot a change : drapeau live/etat/redemarrer_A et _B ; chaque bot sort proprement entre deux pas
#    de sa boucle et live/lancer.bat le relance avec le nouveau code.
# 0. Avant tout : publication des journaux du VPS sur la branche vps-journal (Publie-Journal).
# Journal : live/etat/maj_auto.log. Fichier volontairement en ASCII (PowerShell 5.1).

$ErrorActionPreference = "Continue"
$env:Path = "$env:USERPROFILE\.local\bin;$env:Path"
$repo = Split-Path -Parent $PSScriptRoot
Set-Location $repo
$etat = Join-Path $repo "live\etat"
New-Item -ItemType Directory -Force -Path $etat | Out-Null
$log = Join-Path $etat "maj_auto.log"
$refus = Join-Path $etat "maj_refusee.txt"
$verrou = Join-Path $etat "maj_auto.lock"

function Log([string]$m) {
    "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') $m" | Out-File -FilePath $log -Append -Encoding utf8
}

# Publication des journaux sur la branche vps-journal (separee du code : jamais de conflit avec la mise a jour).
# Copie de travail dediee a cote du depot (..\fabv2-journal). Commit seulement si un fichier a change.
# Le 1er push demande l'acces GitHub : lancer ce script une fois a la main dans un terminal (voir live/README.md).
function Publie-Journal {
    $jr = Join-Path (Split-Path -Parent $repo) "fabv2-journal"
    if (-not (Test-Path (Join-Path $jr ".git"))) {
        git fetch --quiet origin vps-journal 2>$null
        if ($LASTEXITCODE -eq 0) { git worktree add --quiet -B vps-journal $jr origin/vps-journal 2>$null }
        else { git worktree add --quiet --orphan -b vps-journal $jr 2>$null }
        if (-not (Test-Path (Join-Path $jr ".git"))) { Log "journal : copie de travail $jr non creee"; return }
    }
    foreach ($b in "A", "B") {
        $src = Join-Path $etat $b
        if (-not (Test-Path $src)) { continue }
        $dst = Join-Path $jr $b
        New-Item -ItemType Directory -Force -Path $dst | Out-Null
        foreach ($f in "trades.csv", "signaux.csv", "compte.json", "etat.json", "bot.log") {
            $p = Join-Path $src $f
            if (Test-Path $p) { Copy-Item -Force $p $dst }
        }
    }
    foreach ($f in "pnl.md", "maj_auto.log", "relances_A.log", "relances_B.log") {
        $p = Join-Path $etat $f
        if (Test-Path $p) { Copy-Item -Force $p $jr }
    }
    git -C $jr add -A 2>$null
    git -C $jr diff --cached --quiet
    if ($LASTEXITCODE -eq 0) { return }
    git -C $jr -c user.name="VPS fabv2" -c user.email="vps@fabv2.invalid" commit --quiet -m "journal VPS $(Get-Date -Format 'yyyy-MM-dd HH:mm')" 2>$null
    git -C $jr push --quiet origin vps-journal 2>$null
    if ($LASTEXITCODE -ne 0) { Log "journal : push en echec (acces GitHub ? lancer live\maj_auto.ps1 une fois a la main)" }
}

# une seule mise a jour a la fois (un verrou de plus de 30 min est considere comme abandonne)
if ((Test-Path $verrou) -and ((Get-Item $verrou).LastWriteTime -gt (Get-Date).AddMinutes(-30))) { exit 0 }
New-Item -ItemType File -Force -Path $verrou | Out-Null
try {
    try { Publie-Journal } catch { Log "journal : erreur $($_.Exception.Message)" }
    git fetch --quiet origin 2>$null
    if ($LASTEXITCODE -ne 0) { Log "git fetch en echec (reseau ou identifiants GitHub ?)"; exit 1 }
    $branche = (git rev-parse --abbrev-ref HEAD).Trim()
    $local = (git rev-parse HEAD).Trim()
    $distant = (git rev-parse "origin/$branche" 2>$null)
    if (-not $distant) { Log "branche origin/$branche introuvable"; exit 1 }
    $distant = $distant.Trim()
    if ($local -eq $distant) { exit 0 }
    if ((Test-Path $refus) -and ((Get-Content $refus -Raw).Trim() -eq $distant)) { exit 0 }

    git merge-base --is-ancestor $local $distant
    if ($LASTEXITCODE -ne 0) { Log "avance rapide impossible ($local -> $distant) : rien fait"; exit 1 }
    $changes = @(git diff --name-only $local $distant)
    git merge --ff-only --quiet $distant 2>$null
    if ($LASTEXITCODE -ne 0) { Log "mise a jour refusee par git (fichier suivi modifie sur le VPS ?) : git status"; exit 1 }

    $deps = $changes | Where-Object { $_ -eq "pyproject.toml" -or $_ -eq "uv.lock" }
    if ($deps) { uv sync --quiet 2>&1 | Out-File -FilePath $log -Append -Encoding utf8 }

    $sortie = uv run python -m pytest tests/test_live.py -q -p no:cacheprovider 2>&1
    if ($LASTEXITCODE -ne 0) {
        $sortie | Select-Object -Last 15 | Out-File -FilePath $log -Append -Encoding utf8
        git reset --hard --quiet $local
        if ($deps) { uv sync --quiet 2>&1 | Out-File -FilePath $log -Append -Encoding utf8 }
        Set-Content -Path $refus -Value $distant
        Log "TESTS EN ECHEC sur $distant : retour a $local, les bots gardent l'ancien code"
        exit 1
    }

    # code ou calendrier des annonces (lu au demarrage) ; la doc seule ne relance pas les bots
    $bot = $changes | Where-Object { $_ -match '^(live|propfirm)/.*\.(py|csv)$' -or $deps -contains $_ }
    if ($bot) {
        foreach ($b in "A", "B") { New-Item -ItemType File -Force -Path (Join-Path $etat "redemarrer_$b") | Out-Null }
        Log "mise a jour $($local.Substring(0,7)) -> $($distant.Substring(0,7)), tests OK, bots relances : $($bot -join ', ')"
    } else {
        Log "mise a jour $($local.Substring(0,7)) -> $($distant.Substring(0,7)), tests OK (code du bot inchange)"
    }
} finally {
    Remove-Item -Force $verrou -ErrorAction SilentlyContinue
}
