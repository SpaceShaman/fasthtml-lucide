"""Lucide SVG icons for FastHTML."""

import re
from functools import cache
from importlib.resources import files
from xml.etree import ElementTree as ET

from fasthtml.common import NotStr

__all__ = ["Icon"]

ET.register_namespace("", "http://www.w3.org/2000/svg")


@cache
def _icon_source(name: str) -> str:
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        raise ValueError(f"Invalid icon name: {name}")
    resource = files("fasthtml_lucide").joinpath("icons", f"{name}.svg")
    try:
        return resource.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise ValueError(f"Unknown Lucide icon: {name}") from None


def Icon(name: str, *, cls: str = "", size: int = 24) -> NotStr:
    """Render a decorative inline SVG using a kebab-case Lucide icon name."""
    svg = ET.fromstring(_icon_source(name))
    svg.set("width", str(size))
    svg.set("height", str(size))
    svg.set("class", f"{svg.get('class', '')} {cls}".strip())
    svg.set("aria-hidden", "true")
    return NotStr(ET.tostring(svg, encoding="unicode"))
