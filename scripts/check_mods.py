#!/usr/bin/env python3
"""
Controllo della lista mod di ELDERGATE.

Verifica:
  1. che ogni voce abbia i campi obbligatori (name, side, status)
  2. che `status` sia uno dei valori ammessi
  3. che non ci siano nomi duplicati
  4. che ogni dipendenza dichiarata in `requires` esista nella lista
  5. che non sia entrata nessuna mod vietata
  6. che non ci siano più "overhaul" dello stesso piano (Nether/End)

Uso:
    python3 scripts/check_mods.py
    python3 scripts/check_mods.py --strict   # blocca anche su status: check

Esce con codice 1 se trova errori, 0 se è tutto a posto.
Non richiede dipendenze esterne tranne PyYAML.
"""

from __future__ import annotations

import argparse
import glob
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("Serve PyYAML:  pip install pyyaml")

ROOT = Path(__file__).resolve().parent.parent
MODS_DIR = ROOT / "mods"

ALLOWED_STATUS = {"verified", "check", "risky", "optional"}
ALLOWED_SIDE = {"both", "client", "server"}

# Vietate: decisione del gruppo, non si riaprono.
BANNED = {
    "better combat": "conflitto con Epic Fight",
    "badoptimizations": "instabile su Forge 1.20.1",
    "middle-earth": "fuori tema",
    "embeddium++": "fork non supportato",
    "starlight": "sostituito da altre mod di luce",
    "radium reforged": "incompatibile con Embeddium",
    "canary": "incompatibile con Embeddium",
}

# Una sola mod per questi gruppi: due insieme si escludono tecnicamente.
EXCLUSIVE_GROUPS = {
    "nether overhaul": ["incendium", "jaden's nether", "nether remastered",
                        "nether exorcism", "infernal expansion"],
    "end overhaul": ["eldritch end", "end's phantasm", "betterend"],
    "krypton": ["krypton reno", "krypton reforged", "ceres", "pluto", "kryptonfoxified"],
    "mappa": ["journeymap", "xaero's minimap", "xaero's world map"],
    "gravestone": ["yet another gravestone", "you're in grave dangers",
                   "soul bound enchantment", "bonfires"],
    "spawn": ["mob control", "you shall not spawn!", "mob population control",
              "despawntweaker", "harder spawners"],
    "difficolta": ["l2 hostility", "difficulty enhancement", "dungeon difficulty",
                   "majrusz's progressive difficulty", "progressive difficulty"],
    "quest": ["ftb quests", "superior quests", "bountiful"],
    "sangue": ["bn blood particles", "i have blood n' bones", "bleeding system",
               "blood magic", "tome of blood"],
}


def load_all():
    """Restituisce [(file, sezione, voce), ...] per tutte le voci delle ondate."""
    entries = []
    for path in sorted(glob.glob(str(MODS_DIR / "*.yml"))):
        with open(path, encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
        if not isinstance(data, dict):
            continue
        for section, value in data.items():
            if not isinstance(value, list):
                continue
            for item in value:
                if isinstance(item, dict) and "name" in item:
                    entries.append((Path(path).name, section, item))
    return entries


def norm(s: str) -> str:
    return " ".join(s.lower().split())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true",
                        help="considera errore anche le voci con status: check")
    args = parser.parse_args()

    entries = load_all()
    errors, warnings = [], []

    if not entries:
        print("Nessuna voce trovata in mods/*.yml")
        return 1

    seen = {}

    for fname, section, item in entries:
        name = str(item.get("name", "")).strip()
        key = norm(name)

        # 1. campi obbligatori
        for field in ("name", "side", "status"):
            if field not in item:
                errors.append(f"[{fname}:{section}] '{name}' manca il campo '{field}'")

        # 2. valori ammessi
        side = item.get("side")
        if side is not None and side not in ALLOWED_SIDE:
            errors.append(f"[{fname}] '{name}' ha side='{side}' non valido")
        status = item.get("status")
        if status is not None and status not in ALLOWED_STATUS:
            errors.append(f"[{fname}] '{name}' ha status='{status}' non valido")

        # 3. doppioni
        if key in seen:
            warnings.append(f"Doppione: '{name}' in {fname} (già in {seen[key]})")
        else:
            seen[key] = fname

        # 5. vietate
        if key in BANNED:
            errors.append(f"VIETATA: '{name}' ({BANNED[key]})")

        if args.strict and status == "check":
            errors.append(f"[{fname}] '{name}' è ancora 'check'")

    # 4. dipendenze
    for fname, section, item in entries:
        for dep in item.get("requires", []) or []:
            if norm(dep) not in seen:
                errors.append(
                    f"[{fname}] '{item['name']}' richiede '{dep}' che non è in lista")

    # 6. gruppi esclusivi
    for group, members in EXCLUSIVE_GROUPS.items():
        present = [m for m in members if m in seen]
        if len(present) > 1:
            errors.append(
                f"Gruppo '{group}': ci sono {len(present)} mod che si escludono ({', '.join(present)})")

    # ── report ────────────────────────────────────────────────────
    per_file = {}
    per_status = {}
    for fname, section, item in entries:
        per_file[fname] = per_file.get(fname, 0) + 1
        st = item.get("status", "?")
        per_status[st] = per_status.get(st, 0) + 1

    print("╭─ ELDERGATE · controllo lista mod ─────────────────────────")
    for fname in sorted(per_file):
        print(f"│  {fname:24} {per_file[fname]:>3} voci")
    print("├───────────────────────────────────────────────────────────")
    print("│  voci totali: " + ", ".join(f"{k}={v}" for k, v in sorted(per_status.items())))
    print("╰───────────────────────────────────────────────────────────")

    if warnings:
        print("\nAVVISI")
        for w in warnings:
            print("  ! " + w)

    if errors:
        print(f"\nERRORI ({len(errors)})")
        for e in errors:
            print("  ✗ " + e)
        print("\nLa lista NON è pronta.")
        return 1

    print("\nTutto a posto. Le dipendenze dichiarate esistono, "
          "nessuna mod vietata, nessun gruppo in conflitto.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
