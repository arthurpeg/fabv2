"""Régénère wiki/hot.md (état courant) à partir de log.md, des pages d'expérience,
du registre des échecs et des rapports. Bibliothèque standard uniquement.

python wiki/update_hot.py

Ne plante jamais : un fichier manquant donne une section vide, et toute erreur
inattendue est écrite sur stderr avec un code de sortie 0. Le bloc entre les
marqueurs NEXT-ACTIONS de l'ancien hot.md est conservé tel quel.
"""

from __future__ import annotations

import re
import sys
from datetime import datetime
from pathlib import Path

WIKI = Path(__file__).resolve().parent
ROOT = WIKI.parent
HOT = WIKI / "hot.md"
N_LOG = 8

START = "<!-- NEXT-ACTIONS:START -->"
END = "<!-- NEXT-ACTIONS:END -->"
DEFAULT_ACTIONS = "- (à remplir : ce bloc est conservé à chaque régénération)"

COUNTER = re.compile(r"[Cc]ompteur[^0-9\n]{0,40}?(\d{1,3}(?:[   ]\d{3})+|\d+)")


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def frontmatter(text: str) -> dict[str, str]:
    m = re.match(r"---\s*\n(.*?)\n---", text, re.S)
    out = {}
    for line in (m.group(1).splitlines() if m else []):
        if ":" in line:
            k, v = line.split(":", 1)
            out[k.strip()] = v.split("#", 1)[0].strip()
    return out


def log_entries() -> list[str]:
    return [l.strip() for l in read(WIKI / "log.md").splitlines() if l.startswith("## [")]


def trial_counter() -> tuple[int, str] | None:
    """Plus grande valeur du compteur d'essais citée dans reports/ et RESULTS.md."""
    best = None
    for path in sorted((ROOT / "reports").glob("*.md")) + [ROOT / "RESULTS.md"]:
        for m in COUNTER.finditer(read(path)):
            n = int(re.sub(r"\D", "", m.group(1)))
            if best is None or n > best[0]:
                best = (n, path.relative_to(ROOT).as_posix())
    return best


def latest_prereg() -> int | None:
    nums = [int(m.group(1) or 1) for p in ROOT.glob("PREREGISTRATION*.md")
            if (m := re.fullmatch(r"PREREGISTRATION(?:_(\d+))?\.md", p.name))]
    return max(nums) if nums else None


def experiments() -> list[tuple[str, str, str, str]]:
    rows = []
    for p in sorted((WIKI / "experiments").glob("*.md")):
        text = read(p)
        fm = frontmatter(text)
        title = next((l[2:].strip() for l in text.splitlines() if l.startswith("# ")), p.stem)
        rows.append((p.stem, title, fm.get("status", "?"), fm.get("verdict", "?")))
    return rows


def ledger_rows() -> int:
    lines = read(WIKI / "Failed Ideas" / "ledger.md").splitlines()
    return sum(1 for l in lines if re.match(r"\|\s*\d{4}-\d{2}-\d{2}", l))


def next_actions() -> str:
    m = re.search(re.escape(START) + r"\n?(.*?)\n?" + re.escape(END), read(HOT), re.S)
    return m.group(1).strip("\n") if m and m.group(1).strip() else DEFAULT_ACTIONS


def build() -> str:
    entries = log_entries()
    counter = trial_counter()
    prereg = latest_prereg()
    exps = experiments()
    open_exps = [e for e in exps if e[2] not in ("done", "abandoned")]

    out = [
        "---",
        "type: hot",
        f"updated: {datetime.now():%Y-%m-%d %H:%M}",
        "---",
        "",
        "> **Généré automatiquement par `wiki/update_hot.py` (hook Stop). Ne pas éditer à la main**, "
        "sauf le bloc « Prochaines actions », conservé à chaque régénération.",
        "",
        "# État courant",
        "",
        f"- Compteur global d'essais : **{counter[0]:,}** (source : [[{counter[1][:-3]}]])".replace(",", " ")
        if counter else "- Compteur global d'essais : introuvable",
        f"- Dernier pré-enregistrement : n° {prereg} ([[PREREGISTRATION_{prereg}]])" if prereg
        else "- Dernier pré-enregistrement : aucun",
        f"- Idées abandonnées au registre : {ledger_rows()} ([[wiki/Failed Ideas/ledger]])",
        f"- Dernière activité : {entries[-1][4:14] if entries else '—'}",
        "",
        "## Expériences ouvertes",
        "",
    ]
    if open_exps:
        out += ["| Expérience | Statut | Verdict |", "|---|---|---|"]
        cell = lambda x: x.replace("|", "\\|")  # noqa: E731
        out += [f"| [[wiki/experiments/{s}\\|{cell(t)}]] | {cell(st)} | {cell(v)} |"
                for s, t, st, v in open_exps]
    else:
        out.append("Aucune.")
    out += ["", f"## Dernières entrées du journal ({min(N_LOG, len(entries))})", ""]
    out += [f"- {e[3:]}" for e in entries[-N_LOG:][::-1]] or ["- (journal vide)"]
    out += ["", "## Prochaines actions", "", START, next_actions(), END, ""]
    return "\n".join(out)


def main() -> None:
    try:
        text = build()
        tmp = HOT.with_suffix(".md.tmp")
        tmp.write_text(text, encoding="utf-8")
        tmp.replace(HOT)
    except Exception as exc:  # ne doit jamais casser la session
        print(f"update_hot: {exc!r}", file=sys.stderr)


if __name__ == "__main__":
    main()
