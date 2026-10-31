"""Contract tests for the dependency-free public landing page."""

from html.parser import HTMLParser
from pathlib import Path
import unittest
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.ids = []
        self.links = []
        self.images = []
        self.scripts = []
        self.stylesheets = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        self.tags.append((tag, attributes))
        if "id" in attributes:
            self.ids.append(attributes["id"])
        if tag == "a" and "href" in attributes:
            self.links.append(attributes["href"])
        if tag == "img":
            self.images.append(attributes)
        if tag == "script" and "src" in attributes:
            self.scripts.append(attributes["src"])
        if tag == "link" and attributes.get("rel") == "stylesheet":
            self.stylesheets.append(attributes.get("href", ""))


class LandingPageTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = INDEX.read_text(encoding="utf-8")
        cls.page = PageParser()
        cls.page.feed(cls.html)

    def test_semantic_page_structure(self):
        tag_names = [tag for tag, _ in self.page.tags]
        self.assertEqual(tag_names.count("main"), 1)
        self.assertEqual(tag_names.count("h1"), 1)
        self.assertEqual(tag_names.count("header"), 1)
        self.assertEqual(tag_names.count("footer"), 1)
        self.assertGreaterEqual(tag_names.count("section"), 5)
        self.assertIn("nav", tag_names)
        self.assertIn("figure", tag_names)
        self.assertIn("figcaption", tag_names)

    def test_ids_are_unique_and_local_anchors_resolve(self):
        self.assertEqual(len(self.page.ids), len(set(self.page.ids)))
        local_anchors = [href[1:] for href in self.page.links if href.startswith("#")]
        self.assertGreaterEqual(len(local_anchors), 4)
        for anchor in local_anchors:
            with self.subTest(anchor=anchor):
                self.assertIn(anchor, self.page.ids)

    def test_assets_are_local_relative_paths(self):
        assets = self.page.scripts + self.page.stylesheets + [
            image.get("src", "") for image in self.page.images
        ]
        self.assertGreaterEqual(len(assets), 4)
        for asset in assets:
            with self.subTest(asset=asset):
                parsed = urlparse(asset)
                self.assertFalse(parsed.scheme)
                self.assertFalse(parsed.netloc)
                self.assertFalse(parsed.path.startswith("/"))
                self.assertNotIn("..", Path(parsed.path).parts)

    def test_external_links_are_https(self):
        external = [href for href in self.page.links if not href.startswith("#")]
        self.assertGreaterEqual(len(external), 3)
        for href in external:
            with self.subTest(href=href):
                self.assertEqual(urlparse(href).scheme, "https")

    def test_images_and_copy_control_are_accessible(self):
        self.assertTrue(self.page.images)
        for image in self.page.images:
            with self.subTest(src=image.get("src")):
                self.assertIn("alt", image)
        copy_buttons = [
            attrs
            for tag, attrs in self.page.tags
            if tag == "button" and "data-copy-command" in attrs
        ]
        self.assertEqual(len(copy_buttons), 1)
        self.assertIn("aria-describedby", copy_buttons[0])
        status_nodes = [
            attrs
            for _, attrs in self.page.tags
            if attrs.get("id") == copy_buttons[0]["aria-describedby"]
        ]
        self.assertEqual(len(status_nodes), 1)
        self.assertEqual(status_nodes[0].get("aria-live"), "polite")

    def test_representative_demo_and_quick_start_contract(self):
        expected = (
            "Representative Paploo conversation",
            "git clone https://github.com/dagi377/paploo.git",
            "cd paploo",
            "scripts/install.sh",
            "mock model",
            "no API tokens",
            "http://localhost:48090",
            "Mara Okafor",
            "30 GiB",
        )
        for text in expected:
            with self.subTest(text=text):
                self.assertIn(text, self.html)


if __name__ == "__main__":
    unittest.main()
