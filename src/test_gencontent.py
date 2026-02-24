import unittest

from gencontent import extract_title

class TestGencontent(unittest.TestCase):
    def test_extract_title(self):
        markdown = "# Tolkien "
        header = extract_title(markdown)
        self.assertEqual(header, "Tolkien")

if __name__ == "__main__":
    unittest.main()