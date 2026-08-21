import unittest
import re
from extract_markdown_images import extract_markdown_images, extract_markdown_links


class TestMarkdownParser(unittest.TestCase):

    def test_extract_markdown_images_single(self):
        text = "This is an image ![alt text](https://example.com/image.png)"
        expected = [("alt text", "https://example.com/image.png")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_images_multiple(self):
        text = "![one](https://img1.png) and ![two](https://img2.png)"
        expected = [
            ("one", "https://img1.png"),
            ("two", "https://img2.png")
        ]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_images_empty_alt_text(self):
        text = "![](https://example.com/image.png)"
        expected = [("", "https://example.com/image.png")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_images_no_matches(self):
        text = "There are no images here, only text."
        self.assertEqual(extract_markdown_images(text), [])

    def test_extract_markdown_links_single(self):
        text = "This is a [link](https://example.com)"
        expected = [("link", "https://example.com")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extract_markdown_links_multiple(self):
        text = "[Google](https://google.com) and [GitHub](https://github.com)"
        expected = [
            ("Google", "https://google.com"),
            ("GitHub", "https://github.com")
        ]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extract_markdown_links_ignores_images(self):
        text = "A link [to site](https://site.com) and an image ![alt](https://img.png)"
        expected = [("to site", "https://site.com")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extract_markdown_links_no_matches(self):
        text = "Just plain text without links."
        self.assertEqual(extract_markdown_links(text), [])
