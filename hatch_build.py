"""Bundle the matching npm release when building from a Git checkout."""

import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class CustomBuildHook(BuildHookInterface):
    def initialize(self, version, build_data):
        match = re.fullmatch(r"(\d+\.\d+\.\d+)(?:\.post\d+)?", self.metadata.version)
        if match is None:
            raise ValueError("Use a Lucide version, optionally followed by .postN")
        lucide_version = match[1]
        package = Path(self.root) / "src" / "fasthtml_lucide"
        icons = package / "icons"
        marker = package / "lucide-version.txt"
        license_file = package / "LUCIDE-LICENSE"

        if not (
            marker.is_file()
            and marker.read_text(encoding="utf-8").strip() == lucide_version
            and any(icons.glob("*.svg"))
            and license_file.is_file()
        ):
            npm = shutil.which("npm")
            if npm is None:
                raise RuntimeError(
                    "Building from Git requires npm; install Node.js first"
                )
            with tempfile.TemporaryDirectory(prefix="fasthtml-lucide-") as tmp:
                workdir = Path(tmp)
                (workdir / "package.json").write_text(
                    '{"private":true}', encoding="utf-8"
                )
                subprocess.run(
                    [
                        npm,
                        "install",
                        "--ignore-scripts",
                        "--no-audit",
                        "--no-fund",
                        "--save-exact",
                        f"lucide-static@{lucide_version}",
                    ],
                    cwd=workdir,
                    check=True,
                )
                source = workdir / "node_modules" / "lucide-static"
                installed = json.loads(
                    (source / "package.json").read_text(encoding="utf-8")
                )
                if installed["version"] != lucide_version:
                    raise RuntimeError("Unexpected lucide-static version")
                svgs = sorted((source / "icons").glob("*.svg"))
                if not svgs or not (source / "LICENSE").is_file():
                    raise RuntimeError(
                        "lucide-static is missing SVG icons or its LICENSE"
                    )
                # Invalidate the marker before replacing assets, including on failure.
                marker.unlink(missing_ok=True)
                if icons.exists():
                    shutil.rmtree(icons)
                icons.mkdir(parents=True)
                for svg in svgs:
                    shutil.copyfile(svg, icons / svg.name)
                shutil.copyfile(source / "LICENSE", license_file)
                marker.write_text(lucide_version + "\n", encoding="utf-8")

        build_data["artifacts"].extend(
            [
                "src/fasthtml_lucide/icons/**",
                "src/fasthtml_lucide/lucide-version.txt",
                "src/fasthtml_lucide/LUCIDE-LICENSE",
            ]
        )
