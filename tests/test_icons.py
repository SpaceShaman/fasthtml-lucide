from importlib.resources import files
from xml.etree import ElementTree as ET

import pytest
from fasthtml.common import Div, to_xml

from fasthtml_lucide import Icon


def test_rendering():
    svg = ET.fromstring(str(Icon("sun", cls="text-yellow-500", size=32)))
    assert svg.tag == "{http://www.w3.org/2000/svg}svg"
    assert svg.get("width") == "32"
    assert svg.get("height") == "32"
    assert svg.get("aria-hidden") == "true"
    classes = svg.get("class", "").split()
    assert "text-yellow-500" in classes
    original = ET.fromstring(
        files("fasthtml_lucide").joinpath("icons/sun.svg").read_text()
    )
    assert set(original.get("class", "").split()) <= set(classes)
    assert "<svg" in str(to_xml(Div(Icon("sun"))))


def test_calls_are_independent():
    Icon("sun", cls="custom", size=48)
    svg = ET.fromstring(str(Icon("sun")))
    assert svg.get("width") == "24"
    assert "custom" not in svg.get("class", "")


@pytest.mark.parametrize(
    "name", ["../sun", "/sun", "Sun", "", "not-an-existing-lucide-icon"]
)
def test_invalid_and_missing_names(name):
    with pytest.raises(ValueError):
        Icon(name)


def test_attributes_are_escaped():
    cls = 'a" onload="bad<&'
    svg = ET.fromstring(str(Icon("sun", cls=cls)))
    assert svg.get("onload") is None
    assert svg.get("class", "").endswith(cls)
