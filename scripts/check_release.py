"""Select the latest stable Lucide version and retry incomplete PyPI releases."""

import json
import os
import re
import subprocess
import tomllib
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import urlopen

current = tomllib.loads(Path("pyproject.toml").read_text())["project"]["version"]
latest = subprocess.check_output(
    ["npm", "view", "lucide-static", "version"], text=True
).strip()
if not re.fullmatch(r"\d+\.\d+\.\d+", latest):
    raise ValueError(f"Expected a stable npm version, got {latest!r}")
if tuple(map(int, latest.split("."))) > tuple(
    map(int, current.split(".post")[0].split("."))
):
    subprocess.run(["uv", "version", latest, "--frozen", "--no-sync"], check=True)
    current = latest

try:
    with urlopen(
        f"https://pypi.org/pypi/fasthtml-lucide/{current}/json", timeout=30
    ) as response:
        artifacts = json.load(response)["urls"]
    published = {item["packagetype"] for item in artifacts} >= {"bdist_wheel", "sdist"}
except HTTPError as error:
    if error.code != 404:
        raise
    published = False

with open(os.environ["GITHUB_OUTPUT"], "a") as output:
    output.write(f"version={current}\nrelease={str(not published).lower()}\n")
