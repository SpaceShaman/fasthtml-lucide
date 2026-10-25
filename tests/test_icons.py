import unittest
from importlib.resources import files
from xml.etree import ElementTree as ET

from fasthtml.common import Div, to_xml

from fasthtml_lucide import Icon


class IconTests(unittest.TestCase):
    def test_rendering(self):
        svg = ET.fromstring(str(Icon("sun", cls="text-yellow-500", size=32)))
        self.assertEqual(svg.tag, "{http://www.w3.org/2000/svg}svg")
        self.assertEqual(svg.get("width"), "32")
        self.assertEqual(svg.get("height"), "32")
        self.assertEqual(svg.get("aria-hidden"), "true")
        self.assertIn("text-yellow-500", svg.get("class").split())
        original = ET.fromstring(
            files("fasthtml_lucide").joinpath("icons/sun.svg").read_text()
        )
        self.assertTrue(
            set(original.get("class", "").split()) <= set(svg.get("class").split())
        )
        self.assertIn("<svg", str(to_xml(Div(Icon("sun")))))

    def test_calls_are_independent(self):
        Icon("sun", cls="custom", size=48)
        svg = ET.fromstring(str(Icon("sun")))
        self.assertEqual(svg.get("width"), "24")
        self.assertNotIn("custom", svg.get("class"))

    def test_invalid_and_missing_names(self):
        for name in ("../sun", "/sun", "Sun", "", "not-an-existing-lucide-icon"):
            with self.subTest(name=name), self.assertRaises(ValueError):
                Icon(name)

    def test_attributes_are_escaped(self):
        svg = ET.fromstring(str(Icon("sun", cls='a" onload="bad', size='"<&')))
        self.assertIsNone(svg.get("onload"))
        self.assertEqual(svg.get("width"), '"<&')


if __name__ == "__main__":
    unittest.main()
