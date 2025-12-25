from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

OWL_REPO = "https://github.com/mdlacasse/Owl.git"
OWL_COMMIT = "7abca00"  # short or full SHA, both OK

ROOT = Path(__file__).resolve().parents[1]
TMP = ROOT / ".tmp_owl"
SRC = TMP / "examples"
DST = ROOT / "examples" / "owlplanner"


def run(cmd: list[str], cwd: Path | None = None) -> None:
    subprocess.run(cmd, check=True, cwd=cwd)


def main() -> None:
    if TMP.exists():
        shutil.rmtree(TMP)

    print("Cloning OWL...")
    run(["git", "clone", "--depth", "1", OWL_REPO, str(TMP)])

    print(f"Checking out OWL commit {OWL_COMMIT}...")
    run(["git", "checkout", OWL_COMMIT], cwd=TMP)

    print("Syncing examples...")
    if DST.exists():
        shutil.rmtree(DST)

    shutil.copytree(SRC, DST)

    shutil.rmtree(TMP)
    print("Done.")


if __name__ == "__main__":
    main()
