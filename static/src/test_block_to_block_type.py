import unittest
from split_delimiter import block_to_block_type
from textnode import BlockType


class TestBlockToBlockType(unittest.TestCase):

    # --- Heading Tests ---

    def test_headings_h1_to_h6(self):
        for i in range(1, 7):
            prefix = "#" * i + " "
            block = f"{prefix}This is a heading {i}"
            self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_not_enough_space(self):
        # Missing space after '#' should fall back to PARAGRAPH
        block = "#This is not a valid heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_too_many_hashes(self):
        # 7 hashes is not a markdown heading
        block = "####### Too many hashes"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # --- Code Block Tests ---

    def test_code_block_valid(self):
        block = "```python\nprint('hello world')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_block_single_line_fails(self):
        # Current implementation requires len(split_block) > 1
        block = "```print('hello')```"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_code_block_missing_closing(self):
        block = "```python\nprint('hello world')"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # --- Quote Block Tests ---

    def test_quote_block_single_line(self):
        block = "> A simple quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_block_multiline_valid(self):
        block = "> Line 1\n> Line 2\n> Line 3"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_block_multiline_invalid(self):
        # One line is missing the leading '>'
        block = "> Line 1\nLine 2 without quote\n> Line 3"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # --- Unordered List Tests ---

    def test_unordered_list_valid(self):
        block = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_invalid_prefix(self):
        # Item 2 misses the trailing space after '-'
        block = "- Item 1\n-Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # --- Ordered List Tests ---

    def test_ordered_list_valid(self):
        block = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_wrong_sequence(self):
        # Numbers are out of sequence (1 -> 3)
        block = "1. First\n3. Second"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_does_not_start_at_one(self):
        block = "2. Second\n3. Third"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # --- Paragraph Tests ---

    def test_paragraph_standard_text(self):
        block = "Just a standard paragraph with regular text."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph_multiline_text(self):
        block = "Line 1 of a standard paragraph.\nLine 2 of the paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
