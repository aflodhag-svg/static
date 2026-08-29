import unittest

from textnode import TextNode, TextType
from split_delimiter import text_to_textnodes


class TestTextToTextnodes(unittest.TestCase):


    def test_all(self):
        input = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        list = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        list1 = text_to_textnodes(input)
        self.assertListEqual(list, list1)



    def test_plain_text(self):
        text = "Hello I'm John Johnson the third, used car salesman and Fortnite lover."
        self.assertEqual(text_to_textnodes(text), [TextNode("Hello I'm John Johnson the third, used car salesman and Fortnite lover.", TextType.TEXT)])


    def test_only_image(self):
        text = "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(text_to_textnodes(text), [TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")])



    def test_only_link(self):
        text = "[link](https://boot.dev)"
        self.assertEqual(text_to_textnodes(text), [TextNode("link", TextType.LINK, "https://boot.dev")])
