import unittest

from split_delimiter import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):


    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        print(blocks)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )



    def test_excessive_newlines(self):
            markdown = """# Heading



    This paragraph is separated by extra newlines.


    * List item"""
            expected = [
                "# Heading",
                "This paragraph is separated by extra newlines.",
                "* List item",
            ]
            self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_leading_and_trailing_whitespace(self):
        markdown = """   \n\n# Heading with space\n\n  Paragraph with leading spaces.  \n\n"""
        expected = ["# Heading with space", "Paragraph with leading spaces."]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_empty_string(self):
        self.assertEqual(markdown_to_blocks(""), [])
        self.assertEqual(markdown_to_blocks("   \n\n  "), [])
