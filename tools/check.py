#!/usr/bin/env python3
"""Validate present planning artifacts; does not validate a Godot game."""
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.simulate import load_config  # noqa: E402


def main() -> int:
    load_config()
    broken = []
    for path in ROOT.rglob("*.md"):
        for target in re.findall(r"\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
            if "://" in target or target.startswith("#"):
                continue
            local = unquote(target.split("#", 1)[0])
            if local and not (path.parent / local).exists():
                broken.append(f"{path.relative_to(ROOT)}: {target}")
    if broken:
        print("Broken local document links:\n" + "\n".join(broken))
        return 1
    print("Balance configuration and local document targets: OK", flush=True)
    synced = subprocess.run([sys.executable, "tools/sync_prototype.py", "--check"], cwd=ROOT)
    if synced.returncode:
        return synced.returncode
    result = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], cwd=ROOT)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
