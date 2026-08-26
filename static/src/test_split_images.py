import re
import unittest

from split_delimiter import split_nodes_image
from textnode import TextNode, TextType



class TestSplitNodesImage(unittest.TestCase):

    def test_single_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode(
                    "image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"
                ),
            ],
        )

    def test_multiple_images(self):
        node = TextNode(
            "Here is ![img1](https://example.com/1.png) and ![img2](https://example.com/2.png) end.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("Here is ", TextType.TEXT),
                TextNode("img1", TextType.IMAGE, "https://example.com/1.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("img2", TextType.IMAGE, "https://example.com/2.png"),
                TextNode(" end.", TextType.TEXT),
            ],
        )

    def test_image_at_start_and_end(self):
        node = TextNode(
            "![start](https://example.com/start.png) middle text ![end](https://example.com/end.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("start", TextType.IMAGE, "https://example.com/start.png"),
                TextNode(" middle text ", TextType.TEXT),
                TextNode("end", TextType.IMAGE, "https://example.com/end.png"),
            ],
        )

    def test_empty_alt_text(self):
        node = TextNode(
            "An image with no alt: ![](https://example.com/empty.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("An image with no alt: ", TextType.TEXT),
                TextNode("", TextType.IMAGE, "https://example.com/empty.png"),
            ],
        )

    def test_no_images(self):
        node = TextNode("Just plain text with no images.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [node])

    def test_non_text_type_node(self):
        node = TextNode("![alt](https://example.com/pic.png)", TextType.BOLD)
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [node])


if __name__ == "__main__":
    unittest.main()
