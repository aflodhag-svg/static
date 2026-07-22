import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

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






    if __name__ == "__main__":
        unittest.main()
