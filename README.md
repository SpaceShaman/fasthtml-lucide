# fasthtml-lucide

[![License](https://img.shields.io/github/license/SpaceShaman/fasthtml-lucide)](LICENSE)
[![Release](https://img.shields.io/github/actions/workflow/status/SpaceShaman/fasthtml-lucide/release.yml?label=release)](https://github.com/SpaceShaman/fasthtml-lucide/actions/workflows/release.yml)
[![Python versions](https://img.shields.io/pypi/pyversions/fasthtml-lucide)](https://pypi.org/project/fasthtml-lucide/)
[![PyPI version](https://img.shields.io/pypi/v/fasthtml-lucide)](https://pypi.org/project/fasthtml-lucide/)
[![FastHTML](https://img.shields.io/badge/FastHTML-Answer.AI-7854F7)](https://github.com/AnswerDotAI/fasthtml)
[![Lucide](https://img.shields.io/badge/icons-Lucide-F56565)](https://lucide.dev/)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Pytest](https://img.shields.io/badge/testing-pytest-0A9EDC?logo=pytest)](https://docs.pytest.org/)
[![Ruff](https://img.shields.io/badge/linting-Ruff-D7FF64?logo=ruff)](https://github.com/astral-sh/ruff)

Lucide SVG icons for [FastHTML](https://github.com/AnswerDotAI/fasthtml). Icons are bundled in the Python package: no Node.js, JavaScript, CDN or static-file setup is needed in your application.

```sh
uv add fasthtml-lucide
```

```python
from fasthtml.common import Button
from fasthtml_lucide import Icon

Button(Icon("sun", cls="size-5 text-yellow-500"), "Light mode")
```

`Icon(name, *, cls="", size=24)` accepts kebab-case Lucide names and returns an inline SVG. Colors inherit through `currentColor`. Original SVG classes are kept. Invalid or unknown names raise `ValueError`. The generated `IconName` type lists every bundled icon, so type checkers can flag misspelled names and editors can suggest valid ones. You can also import `IconName` to annotate your own variables and parameters.

Icons are decorative (`aria-hidden="true"`). Give icon-only buttons an accessible label on the button itself.

The library is automatically updated to the latest stable `lucide-static` release on npm, with checks running daily. The PyPI version matches the npm version; Python-only fixes may add a `.postN` suffix.

## Development

### Build

Requires Python 3.11+, uv and Node.js/npm when building from Git:

```sh
uv build
```

The build hook downloads the matching `lucide-static` release and bundles its SVGs and license in both the wheel and sdist. Building from the sdist does not require Node.js/npm.

To run the tests against the built package:

```sh
uv venv
uv pip install --group test dist/*.whl
uv run --no-project python -m pytest tests
uv run --no-project python scripts/check_dist.py
```

### Automated releases

The [Release workflow](.github/workflows/release.yml) checks npm daily and can also be run manually. It updates the package version, builds and tests the release, creates a Git tag and publishes to PyPI using Trusted Publishing.

### Manual releases

For a Python-only fix, increment the post-release version (for example, `1.61.0` → `1.61.0.post1` → `1.61.0.post2`):

```sh
uv version --bump post --frozen --no-sync
```

Commit your fix and `pyproject.toml`, push to the default branch, then select **Actions → Release → Run workflow** on GitHub. The workflow creates the tag and publishes to PyPI. The Lucide version stays the same unless a newer npm release is available.

## License

The Python wrapper is MIT licensed. Bundled Lucide icons retain the upstream ISC license and the MIT notices for icons derived from Feather, included in `fasthtml_lucide/LUCIDE-LICENSE`.
