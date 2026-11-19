"""Synchronise les branches du dépôt (voir CLAUDE.md, section « Branches »).

Hiérarchie : main → strategies-vbt → {propfirm-ftmo, ml}. Le socle commun (wiki,
protocole, pré-enregistrements, code commun) vit sur main ; chaque branche fille
le reçoit par merge. vps-journal n'est jamais touchée.

Ce que fait le script, depuis la branche courante (arbre propre exigé) :
1. Si la branche courante n'est pas main : remonte sur main ses modifications des
   chemins communs (wiki, PREREGISTRATION*, RESULTS.md, ...) faites depuis la
   dernière synchro (patch appliqué en 3 voies dans un worktree temporaire).
2. Cascade : merge main → strategies-vbt, puis strategies-vbt → propfirm-ftmo et → ml.
3. Push de chaque branche modifiée (avance rapide seulement ; jamais de force).

S'arrête net au premier conflit (rien n'est poussé pour la branche en conflit) et
dit quoi faire. Usage : uv run python tools/sync_branches.py [--dry-run] [--no-push]
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAIN = "main"
CASCADE = [("main", "strategies-vbt"), ("strategies-vbt", "propfirm-ftmo"), ("strategies-vbt", "ml")]
INTERDITE = "vps-journal"
# Chemins communs remontés vers main (hot.md exclu : régénéré par le hook Stop).
COMMUNS = ["wiki", "CLAUDE.md", "PROTOCOLE.md", "RESULTS.md", "PAPER_SPECS.md", ":(glob)PREREGISTRATION*.md",
           "templates", "fab", "tools", "config", ".claude", ".gitignore", "pyproject.toml", "uv.lock",
           "tests/test_protocole.py", ":(exclude)wiki/hot.md"]


def git(*args: str, cwd: Path = ROOT, check: bool = True, inp: bytes | None = None) -> str:
    r = subprocess.run(["git", "-c", "core.quotepath=off", *args], cwd=cwd, input=inp,
                       capture_output=True)
    if check and r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} : {r.stderr.decode('utf-8', 'replace').strip()}")
    return r.stdout.decode("utf-8", "replace").strip()


def existe(ref: str) -> bool:
    return subprocess.run(["git", "rev-parse", "--verify", "--quiet", ref], cwd=ROOT,
                          capture_output=True).returncode == 0


class Worktree:
    """Worktree temporaire sur une branche (ou la copie de travail si c'est la branche courante)."""

    def __init__(self, branche: str, courante: str):
        self.branche, self.temp = branche, None
        self.path = ROOT
        if branche != courante:
            self.temp = Path(tempfile.mkdtemp(prefix=f"sync-{branche}-"))
            shutil.rmtree(self.temp)
            git("worktree", "add", "--quiet", str(self.temp), branche)
            self.path = self.temp

    def __enter__(self):
        return self.path

    def __exit__(self, *exc):
        if self.temp:
            git("worktree", "remove", "--force", str(self.temp), check=False)
            shutil.rmtree(self.temp, ignore_errors=True)


def remonte(courante: str, dry: bool) -> bool:
    base = git("merge-base", MAIN, courante)
    patch = subprocess.run(["git", "diff", "--binary", base, courante, "--", *COMMUNS], cwd=ROOT,
                           capture_output=True).stdout
    if not patch.strip():
        print(f"remontée : rien à remonter de {courante} vers {MAIN}")
        return False
    fichiers = git("diff", "--name-only", base, courante, "--", *COMMUNS).splitlines()
    print(f"remontée {courante} → {MAIN} : {len(fichiers)} fichier(s) : {', '.join(fichiers[:8])}"
          + (" …" if len(fichiers) > 8 else ""))
    if dry:
        return False
    with Worktree(MAIN, courante) as wt:
        r = subprocess.run(["git", "apply", "--3way", "--index", "--whitespace=nowarn"], cwd=wt,
                           input=patch, capture_output=True)
        if r.returncode != 0:
            print(r.stderr.decode("utf-8", "replace"))
            raise SystemExit(f"CONFLIT en remontant vers {MAIN} : rien n'est commité. Reporter à la main "
                             f"(git switch {MAIN} ; git checkout {courante} -- <fichiers>) puis relancer.")
        if not git("diff", "--cached", "--name-only", cwd=wt):
            print("remontée : déjà présent sur main")
            return False
        git("commit", "--quiet", "-m", f"sync : socle commun remonté de {courante}", cwd=wt)
    return True


def merge(parent: str, enfant: str, courante: str, dry: bool) -> bool:
    if not existe(enfant):
        print(f"merge {parent} → {enfant} : branche absente, ignorée")
        return False
    if git("rev-list", "--count", f"{enfant}..{parent}") == "0":
        print(f"merge {parent} → {enfant} : déjà à jour")
        return False
    print(f"merge {parent} → {enfant}")
    if dry:
        return False
    with Worktree(enfant, courante) as wt:
        r = subprocess.run(["git", "merge", "--no-edit", "--quiet", "-m",
                            f"sync : merge {parent} → {enfant}", parent], cwd=wt, capture_output=True)
        if r.returncode != 0:
            conflits = git("diff", "--name-only", "--diff-filter=U", cwd=wt).splitlines()
            if conflits == ["wiki/hot.md"]:  # généré : on garde la version de l'enfant, le hook la refera
                git("checkout", "--ours", "wiki/hot.md", cwd=wt)
                git("add", "wiki/hot.md", cwd=wt)
                git("commit", "--quiet", "--no-edit", cwd=wt)
            else:
                git("merge", "--abort", cwd=wt, check=False)
                raise SystemExit(f"CONFLIT en mergeant {parent} → {enfant} sur {conflits} : merge annulé. "
                                 f"Le résoudre à la main (git switch {enfant} ; git merge {parent}).")
    return True


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-push", action="store_true")
    a = ap.parse_args()

    courante = git("rev-parse", "--abbrev-ref", "HEAD")
    if courante == INTERDITE:
        raise SystemExit("branche vps-journal : on n'y touche pas")
    if git("status", "--porcelain"):
        raise SystemExit("arbre de travail non propre : commiter d'abord")
    git("fetch", "--quiet", "origin", check=False)
    for b in {MAIN, *(e for _, e in CASCADE)}:  # avance rapide locale sur origin si en retard
        if existe(b) and existe(f"origin/{b}") and git("rev-list", "--count", f"{b}..origin/{b}") != "0":
            if git("rev-list", "--count", f"origin/{b}..{b}") != "0":
                raise SystemExit(f"{b} et origin/{b} ont divergé : réconcilier à la main d'abord")
            if b == courante:
                git("merge", "--ff-only", "--quiet", f"origin/{b}")
            else:
                git("branch", "-f", b, f"origin/{b}")

    modifiees = set()
    if courante != MAIN and remonte(courante, a.dry_run):
        modifiees.add(MAIN)
    for parent, enfant in CASCADE:
        if merge(parent, enfant, courante, a.dry_run):
            modifiees.add(enfant)

    if a.dry_run or a.no_push or not modifiees:
        print("rien poussé" if not modifiees else f"non poussé : {sorted(modifiees)}")
        return
    for b in sorted(modifiees):
        r = subprocess.run(["git", "push", "--quiet", "origin", f"{b}:{b}"], cwd=ROOT, capture_output=True)
        print(f"push {b} : {'ok' if r.returncode == 0 else r.stderr.decode('utf-8', 'replace').strip()}")


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as e:
        sys.exit(str(e))
