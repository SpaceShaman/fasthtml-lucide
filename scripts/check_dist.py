"""Verify bundled resources and rebuild the sdist offline without npm."""

import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path
from zipfile import ZipFile


def assets(wheel):
    with ZipFile(wheel) as archive:
        names = archive.namelist()
        assert not any("node_modules" in name for name in names)
        bundled = {
            name: archive.read(name)
            for name in names
            if name.startswith("fasthtml_lucide/")
        }
        assert "fasthtml_lucide/icons/sun.svg" in bundled
        assert "fasthtml_lucide/LUCIDE-LICENSE" in bundled
        assert "fasthtml_lucide/lucide-version.txt" in bundled
        return bundled


uv = shutil.which("uv")
(wheel,) = Path("dist").glob("*.whl")
(sdist,) = Path("dist").glob("*.tar.gz")
expected = assets(wheel)
with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    with tarfile.open(sdist) as archive:
        archive.extractall(root / "source", filter="data")
    (source,) = (root / "source").iterdir()
    subprocess.run(
        [uv, "venv", "--python", sys.executable, str(root / "venv")], check=True
    )
    python = root / "venv" / "bin" / "python"
    subprocess.run(
        [uv, "pip", "install", "--python", str(python), "hatchling>=1.27"], check=True
    )
    subprocess.run(
        [
            uv,
            "build",
            str(source),
            "--wheel",
            "--offline",
            "--no-build-isolation",
            "--python",
            str(python),
            "--out-dir",
            str(root / "dist"),
        ],
        env={**os.environ, "PATH": ""},
        check=True,
    )
    (rebuilt,) = (root / "dist").glob("*.whl")
    assert assets(rebuilt) == expected
print("Wheel assets verified; sdist rebuilt offline without npm.")
