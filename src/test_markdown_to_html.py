import unittest

from htmlnode import LeafNode, ParentNode
from split_delimiter import (
    block_to_block_type,
    blocktype_to_html_node,
    markdown_to_blocks,
    markdown_to_html_node,
    text_to_children,
    text_to_textnodes,
)
from textnode import BlockType, TextNode, TextType


class TestMarkdownParser(unittest.TestCase):
    # ------------------------------------------------------------------
    # 1. Tests for markdown_to_blocks
    # ------------------------------------------------------------------
    def test_markdown_to_blocks(self) -> None:
        md = (
            "# Title\n\n"
            "This is a paragraph with **bold** text.\n\n"
            "* Line 1\n* Line 2"
        )
        blocks = markdown_to_blocks(md)
        expected = [
            "# Title",
            "This is a paragraph with **bold** text.",
            "* Line 1\n* Line 2",
        ]
        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_excess_newlines(self) -> None:
        md = "\n\n# Title\n\n\n\nParagraph 1\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["# Title", "Paragraph 1"])

    # ------------------------------------------------------------------
    # 2. Tests for block_to_block_type
    # ------------------------------------------------------------------
    def test_block_to_block_type_heading(self) -> None:
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Heading 3"), BlockType.HEADING)

    def test_block_to_block_type_code(self) -> None:
        block = "```\ncode block\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block_to_block_type_quote(self) -> None:
        block = "> Quote line 1\n> Quote line 2"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_block_to_block_type_unordered_list(self) -> None:
        block = "- item 1\n- item 2\n- item 3"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_ordered_list(self) -> None:
        block = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_block_to_block_type_paragraph(self) -> None:
        block = "Just a standard paragraph of text."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # ------------------------------------------------------------------
    # 3. Tests for text_to_textnodes & text_to_children
    # ------------------------------------------------------------------
    def test_text_to_textnodes(self) -> None:
        text = "Hello **bold** and _italic_ with `code`"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("Hello ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]
        self.assertEqual(nodes, expected)

    def test_text_to_children(self) -> None:
        text = "Text with **bold** leaf."
        children = text_to_children(text)
        expected = [
            LeafNode(None, "Text with "),
            LeafNode("b", "bold"),
            LeafNode(None, " leaf."),
        ]
        self.assertEqual(children, expected)

    # ------------------------------------------------------------------
    # 4. Tests for blocktype_to_html_node
    # ------------------------------------------------------------------
    def test_blocktype_to_html_node_paragraph(self) -> None:
        block = "Simple paragraph text"
        node = blocktype_to_html_node(block)
        expected = ParentNode("p", children=[LeafNode(None, "Simple paragraph text")])
        self.assertEqual(node, expected)

    def test_blocktype_to_html_node_heading(self) -> None:
        block = "## Header Level 2"
        node = blocktype_to_html_node(block)
        expected = ParentNode("h2", children=[LeafNode(None, "Header Level 2")])
        self.assertEqual(node, expected)

    def test_blocktype_to_html_node_code(self) -> None:
        block = "```\ndef hello():\n    return 'world'\n```"
        node = blocktype_to_html_node(block)
        expected = ParentNode(
            "pre",
            children=[LeafNode("code", "def hello():\n    return 'world'\n")],
        )
        self.assertEqual(node, expected)

    def test_blocktype_to_html_node_unordered_list(self) -> None:
        block = "- item 1\n- item 2"
        node = blocktype_to_html_node(block)
        expected = ParentNode(
            "ul",
            children=[
                ParentNode("li", children=[LeafNode(None, "item 1")]),
                ParentNode("li", children=[LeafNode(None, "item 2")]),
            ],
        )
        self.assertEqual(node, expected)

    # ------------------------------------------------------------------
    # 5. Full Integration Tests for markdown_to_html_node
    # ------------------------------------------------------------------
    def test_markdown_to_html_node_full_document(self) -> None:
        markdown = (
            "# Title\n\n"
            "This is a paragraph with **bold** text.\n\n"
            "- Item 1\n"
            "- Item 2"
        )
        node = markdown_to_html_node(markdown)
        expected = ParentNode(
            "div",
            children=[
                ParentNode("h1", children=[LeafNode(None, "Title")]),
                ParentNode(
                    "p",
                    children=[
                        LeafNode(None, "This is a paragraph with "),
                        LeafNode("b", "bold"),
                        LeafNode(None, " text."),
                    ],
                ),
                ParentNode(
                    "ul",
                    children=[
                        ParentNode("li", children=[LeafNode(None, "Item 1")]),
                        ParentNode("li", children=[LeafNode(None, "Item 2")]),
                    ],
                ),
            ],
        )
        self.assertEqual(node, expected)

    def test_markdown_to_html_node_output_rendering(self) -> None:
        markdown = (
            "# Header\n\n"
            "Paragraph with _italic_ and `code`.\n\n"
            "> A blockquote"
        )
        html_node = markdown_to_html_node(markdown)
        expected_html = (
            "<div>"
            "<h1>Header</h1>"
            "<p>Paragraph with <i>italic</i> and <code>code</code>.</p>"
            "<blockquote>A blockquote</blockquote>"
            "</div>"
        )
        self.assertEqual(html_node.to_html(), expected_html)


if __name__ == "__main__":
    unittest.main()
