import textwrap
import unittest

from split_delimiter import split_nodes_delimiter, markdown_to_html_node
from textnode import TextNode, TextType


class TestSplitDelimiter(unittest.TestCase):
    def test_paragraphs(self):
        md = textwrap.dedent("""
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """)

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )


    def test_codeblock(self):
        md = textwrap.dedent("""
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """)

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

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
        with self.assertRaises(ValueError):
            split_nodes_delimiter(to_test, "`", TextType.CODE)



class TestMarkdownToBlocks(unittest.TestCase):

    def test_paragraphs(self):
        md = "\nThis is **bolded** paragraph\ntext in a p\ntag here\n\nThis is another paragraph with _italic_ text and `code` here\n"

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    )


    def test_codeblock(self):
        md = "```\nThis is text that _should_ remain\nthe **same** even with inline stuff\n```"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )



if __name__ == "__main__":
    unittest.main()
