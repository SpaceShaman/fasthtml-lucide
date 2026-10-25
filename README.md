# fasthtml-lucide

Lucide SVG icons for FastHTML. Icons are bundled in the Python package: no Node.js, JavaScript, CDN or static-file setup is needed in your application.

```sh
uv add fasthtml-lucide
```

```python
from fasthtml.common import Button
from fasthtml_lucide import Icon

Button(Icon("sun", cls="size-5 text-yellow-500"), "Light mode")
```

`Icon(name, *, cls="", size=24)` accepts kebab-case Lucide names and returns an inline SVG. Colors inherit through `currentColor`. Original SVG classes are kept. Invalid or unknown names raise `ValueError`.

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

For a Python-only fix, use a `.postN` version (for example, `1.61.0.post1`), commit and push the change, then run the workflow manually. The bundled Lucide version remains `1.61.0`.

## License

The Python wrapper is MIT licensed. Bundled Lucide icons retain the upstream ISC license and the MIT notices for icons derived from Feather, included in `fasthtml_lucide/LUCIDE-LICENSE`.
