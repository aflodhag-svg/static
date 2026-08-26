import re
import unittest

from split_delimiter import split_nodes_link
from textnode import TextNode, TextType





class TestSplitNodesLink(unittest.TestCase):

    def test_single_link(self):
        node = TextNode(
            "This is text with a [link](https://www.google.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.google.com"),
            ],
        )

    def test_multiple_links(self):
        node = TextNode(
            "Read [link1](https://example.com/1) or [link2](https://example.com/2) for info.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("Read ", TextType.TEXT),
                TextNode("link1", TextType.LINK, "https://example.com/1"),
                TextNode(" or ", TextType.TEXT),
                TextNode("link2", TextType.LINK, "https://example.com/2"),
                TextNode(" for info.", TextType.TEXT),
            ],
        )

    def test_link_at_start_and_end(self):
        node = TextNode(
            "[first](https://example.com/1) middle [last](https://example.com/2)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("first", TextType.LINK, "https://example.com/1"),
                TextNode(" middle ", TextType.TEXT),
                TextNode("last", TextType.LINK, "https://example.com/2"),
            ],
        )

    def test_no_links(self):
        node = TextNode("Just plain text with no links.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [node])

    def test_non_text_node_ignored(self):
        node = TextNode("[link](https://example.com)", TextType.CODE)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [node])

    def test_empty_anchor_text(self):
        node = TextNode(
            "Click [] (https://example.com) here",
            TextType.TEXT,
        )
        node_clean = TextNode(
            "Click [](https://example.com) here",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node_clean])
        self.assertEqual(
            new_nodes,
            [
                TextNode("Click ", TextType.TEXT),
                TextNode("", TextType.LINK, "https://example.com"),
                TextNode(" here", TextType.TEXT),
            ],
        )


if __name__ == "__main__":
    unittest.main()
