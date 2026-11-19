# SessionStart : synchronise le dépôt (best-effort) puis affiche wiki/hot.md,
# que Claude Code ajoute au contexte de la session. Ne bloque jamais : sortie 0.
$ErrorActionPreference = 'SilentlyContinue'
try {
    [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
    Set-Location (Resolve-Path "$PSScriptRoot\..\..")
    $env:GIT_TERMINAL_PROMPT = '0'
    git pull --ff-only --quiet *> $null
    $branche = (git rev-parse --abbrev-ref HEAD 2>$null)
    Write-Output "Branche courante : $branche. Avant d'ecrire quoi que ce soit, choisir la branche selon CLAUDE.md (section Branches : main = recherche/phenomenes, strategies-vbt = backtests, propfirm-ftmo = propfirm + bot, ml = machine learning ; jamais vps-journal), l'annoncer et faire git switch si besoin."
    if (Test-Path 'wiki/hot.md') {
        Write-Output 'Etat courant du wiki (wiki/hot.md). Lire aussi wiki/index.md et wiki/Failed Ideas/ledger.md avant tout travail substantiel.'
        Get-Content -Raw -Encoding UTF8 'wiki/hot.md'
    }
} catch {}
exit 0
