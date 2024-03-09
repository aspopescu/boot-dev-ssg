import unittest
from htmlnode import *


class TestHTMLNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_to_html_leaf_node_1(self):
        leaf_node_1 = LeafNode("p", "This is a paragraph of text.", None)
        expected_result_for_l_n_1 = "<p>This is a paragraph of text.</p>"
        self.assertEqual(leaf_node_1.to_html(), expected_result_for_l_n_1)

    def test_to_html_leaf_node_2(self):
        leaf_node_2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        expected_result_for_l_n_2 = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(leaf_node_2.to_html(), expected_result_for_l_n_2)

    def test_to_html_leaf_node_3(self):
        leaf_node_3 = LeafNode(None, None, None)
        with self.assertRaises(ValueError) as context:
            leaf_node_3.to_html()
        self.assertEqual(str(context.exception), "LeafNode: All leaf nodes require a value.")

    def test_to_html_leaf_node_4(self):
        leaf_node_4 = LeafNode(None, "This is the value only test.", None)
        self.assertEqual(leaf_node_4.to_html(), 'This is the value only test.')

    def test_to_html_parent_node_1(self):
        parent_node_1 = ParentNode(None, "est" , None)
        with self.assertRaises(ValueError) as context:
            parent_node_1.to_html()
        self.assertEqual(str(context.exception), "ParentNode: The tag is not provided.")

    def test_to_html_parent_node_2(self):
        parent_node_2 = ParentNode("p", None, None)
        with self.assertRaises(ValueError) as context:
            parent_node_2.to_html()
        self.assertEqual(str(context.exception), "ParentNode: There are no children.")

    def test_to_html_parent_node_3(self):
        l_f_1 = LeafNode("b", "Bold text01")
        l_f_2 = LeafNode(None, "Normal text01")
        l_f_3 = LeafNode("i", "italic text01")
        l_f_4 = LeafNode(None, "Normal text02")
        p_n_children = [l_f_1, l_f_2, l_f_3, l_f_4]
        expected_result_for_p_n_3 = '<p><b>Bold text01</b>Normal text01<i>italic text01</i>Normal text02</p>'
        parent_node_3 = ParentNode("p", p_n_children, None)
        self.assertEqual(parent_node_3.to_html(), expected_result_for_p_n_3)

    def test_to_html_parent_node_4(self):
        l_f_1 = LeafNode("b", "Bold text001")
        l_f_2 = LeafNode(None, "Normal text001")
        l_f_3 = LeafNode("i", "italic text001")
        leaf_node_1 = LeafNode("p", "This is a paragraph of text.", None)
        leaf_node_2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        l_f_4 = ParentNode("p", [leaf_node_1, leaf_node_2])
        l_f_5 = LeafNode(None, "Normal text002")
        p_n_children = [l_f_1, l_f_2, l_f_3, l_f_4, l_f_5]
        expected_result_for_p_n_3 = '<p><b>Bold text001</b>Normal text001<i>italic text001</i><p><p>This is a paragraph of text.</p><a href="https://www.google.com">Click me!</a></p>Normal text002</p>'
        parent_node_3 = ParentNode("p", p_n_children, None)
        self.assertEqual(parent_node_3.to_html(), expected_result_for_p_n_3)




if __name__ == "__main__":
    unittest.main()

