import unittest
from htmlnode import LeafNode

props1 = {"meat": "pork"}
props2 = {
        "meat": "pork",
        "horse": "carriage",
        "fruit": "banana"}
props3 = {"href": "https://www.google.com"}
children1 = ["some_child_node"]
children2 = ["some_child_node", "some_child_node_two"]

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_not_eq(self):
        node1 = LeafNode("p", "Hi!")
        node2 = LeafNode("a", "Goodbye!")
        self.assertNotEqual(node1, node2)

    def test_no_tag(self):
        node = LeafNode(None, "Hello!")
        self.assertEqual(node.to_html(), "Hello!")

    def test_leaf_to_html_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()




    def test_leaf_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"}).to_html()
        self.assertEqual(node, '<a href="https://www.google.com">Click me!</a>')
