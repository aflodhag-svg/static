import unittest

from htmlnode import HTMLNode

props1 = {"meat": "pork"}
props2 = {
        "meat": "pork",
        "horse": "carriage",
        "fruit": "banana"}
children1 = ["some_child_node"]
children2 = ["some_child_node", "some_child_node_two"]

class TestHTMLNode(unittest.TestCase):
    def test_eq_empty(self):
        node1 = HTMLNode()
        node2 = HTMLNode()
        self.assertEqual(node1, node2)

    def test_not_eq_empty(self):
        node3 = HTMLNode()
        node4 = HTMLNode("hello")
        self.assertNotEqual(node3, node4)

    def test_eq_full(self):
        node5 = HTMLNode("test", "1", children1, props2)
        node6 = HTMLNode("test", "1", children1, props2)
        self.assertEqual(node5, node6)

    def test_not_eq_full(self):
        node7 = HTMLNode("test", "1", children1, props2)
        node8 = HTMLNode("test", "1", children1, props1)
        self.assertNotEqual(node7, node8)

    def test_props_to_html1(self):
        node9 = HTMLNode("test", "1", children1, props1)
        self.assertEqual(node9.props_to_html(), ' meat="pork"')

    def test_props_to_html2(self):
        node10 = HTMLNode("test", "1", children1, props2)
        self.assertEqual(node10.props_to_html(), ' meat="pork" horse="carriage" fruit="banana"')
