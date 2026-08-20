import unittest
from split_delimiter import split_nodes_delimiter
from textnode import TextNode, TextType



class TestSplitDelimiter(unittest.TestCase):


    def test_bold_text(self):
        to_test = [TextNode("This is some **bold** text", TextType.TEXT)]
        result = split_nodes_delimiter(to_test, "**", TextType.BOLD)
        expected = [
            TextNode("This is some ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)


    def test_italic_text(self):
        to_test = [TextNode("This is some __italic__ text", TextType.TEXT)]
        result = split_nodes_delimiter(to_test, "__", TextType.ITALIC)
        expected = [
            TextNode("This is some ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)



    def test_code_text(self):
        to_test = [TextNode("This is some `code` text", TextType.TEXT)]
        result = split_nodes_delimiter(to_test, "`", TextType.CODE)
        expected = [
            TextNode("This is some ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)


    def test_exception(self):
        to_test = [TextNode("This is some ``code` text", TextType.TEXT)]
        with self.assertRaises(Exception):
            split_nodes_delimiter(to_test, "`", TextType.CODE)
