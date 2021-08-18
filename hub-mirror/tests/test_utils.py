import unittest
from utils import str2map


class TestUtils(unittest.TestCase):

    def test_str2map(self):
        self.assertEqual(str2map("a=>b, c=>d"), {'a': 'b', 'c': 'd'})
        self.assertEqual(str2map("a=>b,c=>d"), {'a': 'b', 'c': 'd'})
        # No transitivity
        self.assertEqual(str2map("cc=>c,c=>d"), {'cc': 'c', 'c': 'd'})


if __name__ == '__main__':
    unittest.main()
