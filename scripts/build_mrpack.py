#!/usr/bin/env python3
"""
Genera un .mrpack installabile dalla lista a ondate di ELDERGATE.

Legge mods/W*.yml, risolve ogni voce su Modrinth (slug -> versione Forge 1.20.1),
e scrive un file .mrpack conforme al formato Modrinth (formatVersion 1).

Perché serve uno script e non un file scritto a mano:
  il mrpack vuole sha1 + sha512 + URL + dimensione ESATTI di ogni jar.
  Quelli esistono solo interrogando l'API: inventarli = pack che non si installa.

Uso:
    python3 scripts/build_mrpack.py --wave 0 --dry-run
    python3 scripts/build_mrpack.py --wave 0 -o dist/ELDERGATE-W0-0.1.0.mrpack

Nota: gira su GitHub Actions (che ha internet). In sandbox offline stampa un
errore chiaro invece di produrre un pacchetto bucato.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from dataclasses import dataclass, field
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("Serve PyYAML:  pip install pyyaml")

ROOT = Path(__file__).resolve().parent.parent
MODS_DIR = ROOT / "mods"
MANIFEST_DIR = ROOT / "manifest"
OVERRIDES_DIR = ROOT / "overrides"
PACK_FILE = ROOT / "pack.json"

API = "https://api.modrinth.com/v2"
UA = "eldergate-mrpack-builder/1.0 (modpack interno)"

# side -> env del formato mrpack
ENV = {
    "both":   {"client": "required", "server": "required"},
    "client": {"client": "required", "server": "unsupported"},
    "server": {"client": "unsupported", "server": "required"},
}


# ─────────────────────────────────────────────────────────────
@dataclass
class Entry:
    name: str
    slug: str | None
    side: str
    status: str
    wave_file: str
    section: str


@dataclass
class Resolved:
    entry: Entry
    version_number: str
    filename: str
    url: str
    sha1: str
    sha512: str
    size: int


class ResolutionError(Exception):
    pass


class NetworkDown(ResolutionError):
    """Rete assente: inutile provare le altre 29 mod, si esce subito."""


# ─────────────────────────────────────────────────────────────
def load_pack() -> dict:
    if not PACK_FILE.exists():
        sys.exit(f"Manca {PACK_FILE}")
    return json.loads(PACK_FILE.read_text(encoding="utf-8"))


def load_entries(wave: int) -> list[Entry]:
    """Legge le voci della sola ondata richiesta (tutte le sezioni)."""
    entries: list[Entry] = []
    pattern = re.compile(rf"^W{wave}-.*\.yml$")
    files = sorted(p for p in MODS_DIR.iterdir() if pattern.match(p.name))
    if not files:
        sys.exit(f"Nessun file mods/W{wave}-*.yml trovato.")

    for path in files:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        for section, value in data.items():
            if not isinstance(value, list):
                continue
            for item in value:
                if not isinstance(item, dict) or "name" not in item:
                    continue
                entries.append(Entry(
                    name=item["name"],
                    slug=item.get("slug"),
                    side=item.get("side", "both"),
                    status=item.get("status", "check"),
                    wave_file=path.name,
                    section=section,
                ))
    return entries


# ─────────────────────────────────────────────────────────────
def api_get(path: str, **params) -> object:
    url = f"{API}{path}"
    if params:
        url += "?" + urllib.parse.urlencode({k: json.dumps(v) if isinstance(v, list) else v
                                             for k, v in params.items()})
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        if e.code == 404:
            raise ResolutionError(f"404 su {path}") from e
        raise ResolutionError(f"HTTP {e.code} su {path}") from e
    except urllib.error.URLError as e:
        raise NetworkDown(str(e.reason)) from e
    except (TimeoutError, ConnectionError, OSError) as e:
        raise NetworkDown(str(e)) from e


def resolve(entry: Entry, game_version: str, loader: str) -> Resolved:
    """Trova la build più recente della mod per la versione/loader richiesti."""
    if not entry.slug:
        raise ResolutionError(f"'{entry.name}': nessuno slug Modrinth (voce 'da scegliere')")

    versions = api_get(f"/project/{entry.slug}/version",
                       loaders=[loader],
                       game_versions=[game_version])
    if not isinstance(versions, list) or not versions:
        raise ResolutionError(
            f"'{entry.name}' ({entry.slug}): nessuna build {loader} {game_version}")

    # le versioni arrivano dalla più recente: prendiamo la prima
    v = versions[0]
    files = v.get("files") or []
    if not files:
        raise ResolutionError(f"'{entry.name}': versione senza file")
    f = next((x for x in files if x.get("primary")), files[0])

    hashes = f.get("hashes") or {}
    if "sha1" not in hashes or "sha512" not in hashes:
        raise ResolutionError(f"'{entry.name}': hash mancanti nel file")

    return Resolved(
        entry=entry,
        version_number=v.get("version_number", "?"),
        filename=f["filename"],
        url=f["url"],
        sha1=hashes["sha1"],
        sha512=hashes["sha512"],
        size=f["size"],
    )


# ─────────────────────────────────────────────────────────────
def to_index_file(r: Resolved) -> dict:
    return {
        "path": f"mods/{r.filename}",
        "hashes": {"sha1": r.sha1, "sha512": r.sha512},
        "env": ENV.get(r.entry.side, ENV["both"]),
        "downloads": [r.url],
        "fileSize": r.size,
    }


def build_index(pack: dict, resolved: list[Resolved], wave: int) -> dict:
    return {
        "formatVersion": 1,
        "game": "minecraft",
        "versionId": f"{pack['version']}-w{wave}",
        "name": f"{pack['name']} — W{wave}",
        "summary": pack["summary"],
        "files": [to_index_file(r) for r in resolved],
        "dependencies": {
            "minecraft": pack["minecraft"],
            "forge": pack["forge"],
        },
    }


def write_mrpack(index: dict, out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("modrinth.index.json",
                   json.dumps(index, indent=2, ensure_ascii=False))
        # overrides: config, options.txt, ecc.
        if OVERRIDES_DIR.exists():
            for p in OVERRIDES_DIR.rglob("*"):
                if p.is_file():
                    z.write(p, str(Path("overrides") / p.relative_to(OVERRIDES_DIR)))
    digest = hashlib.sha1(out.read_bytes()).hexdigest()
    print(f"\n  scritto: {out}  ({out.stat().st_size / 1_048_576:.1f} MB)")
    print(f"  sha1:    {digest}")


def write_lock(resolved: list[Resolved], wave: int) -> Path:
    MANIFEST_DIR.mkdir(exist_ok=True)
    path = MANIFEST_DIR / f"lock-w{wave}.json"
    path.write_text(json.dumps({
        "wave": wave,
        "mods": [
            {
                "name": r.entry.name,
                "slug": r.entry.slug,
                "version": r.version_number,
                "filename": r.filename,
                "sha512": r.sha512,
                "side": r.entry.side,
            }
            for r in sorted(resolved, key=lambda x: x.entry.name.lower())
        ],
    }, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


# ─────────────────────────────────────────────────────────────
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--wave", type=int, required=True, help="ondata da impacchettare (0-7)")
    ap.add_argument("-o", "--out", type=Path, help="percorso del .mrpack")
    ap.add_argument("--dry-run", action="store_true",
                    help="risolve e stampa, senza scrivere il .mrpack")
    args = ap.parse_args()

    pack = load_pack()
    entries = load_entries(args.wave)
    print(f"╭─ {pack['name']} · W{args.wave} · {len(entries)} voci ─────────────")

    resolved: list[Resolved] = []
    errors: list[str] = []

    for e in entries:
        try:
            r = resolve(e, pack["minecraft"], "forge")
            resolved.append(r)
            mark = "✓"
            print(f"│ {mark} {e.name[:34]:34} {r.version_number[:26]:26} "
                  f"[{e.side:6}] {r.entry.slug}")
        except NetworkDown as ex:
            print("│")
            print(f"│ ✗ RETE ASSENTE: {ex}")
            print("│   api.modrinth.com non è raggiungibile da qui.")
            print("│   Lo script gira su GitHub Actions (vedi .github/workflows/build-mrpack.yml).")
            print("╰───────────────────────────────────────────────────────────")
            return 2
        except ResolutionError as ex:
            errors.append(str(ex))
            print(f"│ ✗ {e.name[:34]:34} {ex}")

    print("╰───────────────────────────────────────────────────────────")
    print(f"  risolte {len(resolved)}/{len(entries)}")

    if errors:
        print(f"\nERRORI ({len(errors)}) — il pack NON viene generato:")
        for err in errors:
            print("  ✗ " + err)
            # annotazione visibile nei check di GitHub, senza aprire i log
            if os.environ.get("GITHUB_ACTIONS"):
                print(f"::error title=Mod non risolta::{err}")
        print("\nCorreggi gli slug in mods/W%d-*.yml oppure rimuovi le voci." % args.wave)
        return 1

    if args.dry_run:
        print("\n--dry-run: nessun file scritto. Tutto risolto correttamente.")
        return 0

    index = build_index(pack, resolved, args.wave)
    out = args.out or (ROOT / "dist" /
                       f"{pack['name'].replace(' ', '-')}-W{args.wave}-{pack['version']}.mrpack")
    write_mrpack(index, out)
    lock = write_lock(resolved, args.wave)
    print(f"  lock:    {lock}")
    print("\n  Importalo con Prism Launcher o Modrinth App.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
