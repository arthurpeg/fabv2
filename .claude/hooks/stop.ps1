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
} catch {}
exit 0
