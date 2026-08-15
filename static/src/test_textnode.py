import unittest
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)

    def test_eq_url(self):
        node9 = TextNode("This is a text node", TextType.CODE, url="https://boot.dev")
        node10 = TextNode("This is a text node", TextType.CODE, url="https://boot.dev")
        self.assertEqual(node9, node10)

    def test_different_type(self):
        node3 = TextNode("This is a text node", TextType.TEXT)
        node4 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node3, node4)

    def test_different_url(self):
        node5 = TextNode("This is a text node", TextType.CODE, url="https://boot.dev")
        node6 = TextNode("This is a text node", TextType.CODE, url="https://boot.gov")
        self.assertNotEqual(node5, node6)

    def test_no_url(self):
        node7 = TextNode("This is a text node", TextType.LINK, url=None)
        node8 = TextNode("This is a text node", TextType.LINK, url="https://boot.dev")
        self.assertNotEqual(node7, node8)

    def test_same_text_dif_type(self):
        node11 = TextNode("This is a text node", TextType.BOLD)
        node12 = TextNode("This is not text", TextType.BOLD)
        self.assertNotEqual(node11, node12)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_link(self):
        node = TextNode("This is a text node", TextType.LINK, "https://boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, {'href': 'https://boot.dev'})

    def test_text_img(self):
        node = TextNode("This is a text node", TextType.IMAGE, "https://boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {'src': 'https://boot.dev', 'alt': 'This is a text node'})

    def test_wrong_text_type(self):
        with self.assertRaises(AttributeError):
            node = TextNode("This is all wrong", TextType.WRONG)

    def test_text_invalid_type(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node.text_type = "help"
        with self.assertRaises(Exception):
            text_node_to_html_node(node)



    if __name__ == "__main__":
        unittest.main()
