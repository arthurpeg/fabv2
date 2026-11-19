# Stop : régénère wiki/hot.md, puis, si l'arbre a changé, git add -A + commit
# horodaté + push. Les deux étapes sont dans un seul script pour qu'elles
# s'exécutent dans l'ordre (Claude Code lance les hooks d'un même événement en
# parallèle). Tout est best-effort : sortie 0 quoi qu'il arrive.
$ErrorActionPreference = 'SilentlyContinue'
try {
    Set-Location (Resolve-Path "$PSScriptRoot\..\..")

    $py = if (Test-Path '.venv\Scripts\python.exe') { '.venv\Scripts\python.exe' }
          elseif (Get-Command py -ErrorAction SilentlyContinue) { 'py' }
          else { 'python' }
    & $py 'wiki/update_hot.py' *> $null

    # Pas de commit pendant un merge, un rebase ou un cherry-pick en cours.
    $git = (git rev-parse --git-dir 2>$null)
    if (-not $git) { exit 0 }
    foreach ($f in 'MERGE_HEAD', 'rebase-merge', 'rebase-apply', 'CHERRY_PICK_HEAD') {
        if (Test-Path (Join-Path $git $f)) { exit 0 }
    }

    if (git status --porcelain 2>$null) {
        $env:GIT_TERMINAL_PROMPT = '0'
        git add -A *> $null
        git commit --quiet -m ("auto: sync " + (Get-Date -Format 'yyyy-MM-dd HH:mm')) *> $null
        git push --quiet origin HEAD *> $null
    }

    # Coffre Obsidian en lecture seule (..\fabv2-obsidian, worktree détaché sur
    # propfirm-ftmo, la branche qui contient tout) : ramené sur origin/propfirm-ftmo.
    $coffre = Join-Path (Split-Path (Get-Location) -Parent) 'fabv2-obsidian'
    if (Test-Path (Join-Path $coffre '.git')) {
        $env:GIT_TERMINAL_PROMPT = '0'
        git fetch --quiet origin propfirm-ftmo *> $null
        $cible = (git rev-parse origin/propfirm-ftmo 2>$null)
        if ($cible -and ((git -C $coffre rev-parse HEAD 2>$null) -ne $cible)) {
            git -C $coffre checkout --quiet --force --detach $cible *> $null
        }
    }
} catch {}
exit 0
