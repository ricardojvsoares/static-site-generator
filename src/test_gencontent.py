import unittest

from gencontent import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extracts_simple_h1(self):
        markdown = "# Hello"
        self.assertEqual(extract_title(markdown), "Hello")

    def test_strips_surrounding_whitespace(self):
        markdown = "#   Tolkien Fan Club   "
        self.assertEqual(extract_title(markdown), "Tolkien Fan Club")

    def test_ignores_non_h1_headers(self):
        markdown = "## Subtitle\n### Smaller"
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_finds_h1_after_other_content(self):
        markdown = "Some intro\n## Subtitle\n# Real Title\n"
        self.assertEqual(extract_title(markdown), "Real Title")

    def test_raises_when_no_h1_exists(self):
        markdown = "Paragraph\n- list item"
        with self.assertRaises(Exception):
            extract_title(markdown)


if __name__ == "__main__":
    unittest.main()
