# fasthtml-lucide

Lucide SVG icons for FastHTML. Icons are bundled in the Python package: no Node.js,
JavaScript, CDN or static-file setup is needed in your application.

```sh
uv add fasthtml-lucide
```

```python
from fasthtml.common import Button
from fasthtml_lucide import Icon

Button(Icon("sun", cls="size-5 text-yellow-500"), "Light mode")
```

`Icon(name, *, cls="", size=24)` accepts kebab-case Lucide names and returns an
inline SVG. Colors inherit through `currentColor`. Original SVG classes are kept.
Invalid or unknown names raise `ValueError`.

Icons are decorative (`aria-hidden="true"`). Give icon-only buttons an accessible
label on the button itself.

## Build

Requires Python 3.11+, uv and Node.js/npm when building from Git:

```sh
uv build
```

The Hatchling hook installs the exact matching `lucide-static` version in a
temporary directory, with npm lifecycle scripts disabled. It bundles only SVGs,
the upstream license and a version marker alongside the Python component.
Generated assets are ignored by Git. Both the wheel and sdist contain the assets;
building from the sdist does not need npm or access to the npm registry.
Python build dependencies still need to be available.

```sh
uv venv
uv pip install dist/*.whl
uv run --no-project python -m unittest discover -s tests
uv run --no-project python scripts/check_dist.py
```

The second check compares package resources with an offline rebuild of the sdist
using an empty PATH (no npm). It first installs Hatchling into a temporary venv.

## Automated releases

`.github/workflows/release.yml` checks npm daily at 06:23 UTC and can also be run
manually. It updates `pyproject.toml`, builds and tests the package, commits the
version, pushes `vX.Y.Z`, then publishes the built artifacts to PyPI with uv.
It skips complete PyPI releases and retries missing or incomplete releases.
Build and publishing run in separate jobs; only publishing receives OIDC access.

One-time repository setup:

1. Push this project to `SpaceShaman/fasthtml-lucide` on GitHub.
2. Enable Actions and allow the release workflow to push to the default branch.
   Branch protection must permit the bot's version commits.
3. Create a GitHub environment named `pypi`. Leave required reviewers unset for
   fully automatic releases.
4. On PyPI, configure a Trusted Publisher (a pending publisher for a new project):
   project `fasthtml-lucide`, owner `SpaceShaman`, repository `fasthtml-lucide`,
   workflow `release.yml`, environment `pypi`.
5. Run the Release workflow manually for the first release.

The schedule runs from the default branch. Tags are created in the same workflow
as publishing; no second workflow depends on a bot-generated tag event.
Do not move published tags. If a publication fails, rerun the failed job before
adding unrelated commits to that release.

For a Python-only fix, update the version with:

```sh
uv version 1.61.0.post1 --frozen --no-sync
```

Commit and push it, then run Release. This version still bundles Lucide 1.61.0.
The next newer stable Lucide version resumes matching upstream numbering.

## License

The Python wrapper is MIT licensed. Bundled Lucide icons retain the upstream ISC
license and the MIT notices for icons derived from Feather, included in
`fasthtml_lucide/LUCIDE-LICENSE`.
