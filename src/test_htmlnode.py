import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_empty_dict_props(self):
        node = HTMLNode(props={})
        result = node.props_to_html()
        self.assertEqual(result, "")
    
    def test_none_props(self):
        node = HTMLNode(props=None)
        result = node.props_to_html()
        self.assertEqual(result, "")

    def test_props_to_html_with_attributes(self):
        node = HTMLNode(props={
            "href": "https://www.google.com",
            "target": "_blank",
        })
        result = node.props_to_html()
        # Order of dict items matters here; assume stable order
        self.assertEqual(
            result,
            ' href="https://www.google.com" target="_blank"',
        )
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_properties(self):
        node = LeafNode("a", "Click me!", {"href":"https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

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
    
    def test_to_html_multiple_children(self):
        node_list = [
            LeafNode("b", "bold"),
            LeafNode("i", "italic"),
            LeafNode(None, "plain")
        ]
        parent_node = ParentNode("p", node_list)
        self.assertEqual(parent_node.to_html(), "<p><b>bold</b><i>italic</i>plain</p>")

    def test_to_html_deep_nesting(self):
        great_grandchild = LeafNode(None, "Sample text")
        grandchild = ParentNode("b", [great_grandchild])
        child = ParentNode("i", [grandchild])
        node = ParentNode("p", [child])
        self.assertEqual(node.to_html(), "<p><i><b>Sample text</b></i></p>")

if __name__ == "__main__":
    unittest.main()