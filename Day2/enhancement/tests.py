import unittest
from feature import compute_ews

class TestEWS(unittest.TestCase):
    def test_basic(self):
        self.assertTrue(compute_ews(0, 750, 50000, 0) < 20)

    def test_high_risk(self):
        self.assertTrue(compute_ews(120, 500, 200000, 3) > 80)

if __name__ == '__main__':
    unittest.main()
