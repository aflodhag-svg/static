import unittest

from htmlnode import LeafNode, ParentNode

props1 = {"meat": "pork"}
props2 = {
        "meat": "pork",
        "horse": "carriage",
        "fruit": "banana"}
props3 = {"href": "https://www.google.com"}
children1 = ["some_child_node"]
children2 = ["some_child_node", "some_child_node_two"]

class TestParentNode(unittest.TestCase):

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")


    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_no_children(self):
        parent = ParentNode("span", None)
        with self.assertRaises(ValueError):
            parent.to_html()


    def test_to_html_nested_parents(self):
        grandchild_node = ParentNode("b", None)
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_leaf_with_props(self):
        child_node = LeafNode("b", "Click me!", {"href": "https://www.google.com"})
        parent_node = ParentNode("a", [child_node])
        self.assertEqual(parent_node.to_html(), '<a><b href="https://www.google.com">Click me!</b></a>')

    def test_nested_with_props(self):
        child_node = LeafNode("b", "Click me!", {"href": "https://www.google.com"})
        parent_node = ParentNode("a", [child_node])
        grandparent_node = ParentNode("c", [parent_node])
        self.assertEqual(grandparent_node.to_html(), '<c><a><b href="https://www.google.com">Click me!</b></a></c>')

    def test_parent_with_props(self):
        child = LeafNode("b", "Shark")
        parent = ParentNode("a", [child], props1)
        self.assertEqual(parent.to_html(), '<a meat="pork"><b>Shark</b></a>')

    def test_parent_empty_children(self):
        parent = ParentNode("a", [])
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_parent_no_tag(self):
        child = LeafNode("b", "Shark")
        parent = ParentNode(None, [child])
        with self.assertRaises(ValueError):
            parent.to_html()
