import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_url(self):
        node = TextNode("This is a test node", TextType.BOLD, "https://www.url1.com")
        node2 = TextNode("This is a test node", TextType.BOLD, "https://www.url2.com")
        self.assertNotEqual(node, node2)

    def test_texttype(self):
        node = TextNode("This is a test node", TextType.BOLD, "https://www.url.com")
        node2 = TextNode("This is a test node", TextType.ITALIC, "https://www.url.com")
        self.assertNotEqual(node, node2)

    def test_url2(self):
        node = TextNode("This is a test node", TextType.TEXT, "https://www.url.com")
        node2 = TextNode("This is a test node", TextType.TEXT,)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a test node", TextType.TEXT, "https://www.url.com")
        node2 = TextNode("This is not a test node", TextType.TEXT, "https://www.url.com")
        self.assertNotEqual(node, node2)
    
    def test_text2(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")


if __name__ == "__main__":
    unittest.main()