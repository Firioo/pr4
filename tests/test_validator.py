import unittest
from report import generate_report

class TestReport(unittest.TestCase):
    def test_empty_report_has_zero_count(self):
        self.assertEqual(generate_report([]), {"count": 0, "average": 0})
    
    # Дополнительные тесты (чтобы было не менее 10)
    def test_single_element(self): self.assertEqual(generate_report([5]), {"count": 1, "average": 5})
    def test_two_elements(self): self.assertEqual(generate_report([2, 4]), {"count": 2, "average": 3})
    def test_negative(self): self.assertEqual(generate_report([-2, -4]), {"count": 2, "average": -3})
    def test_zero(self): self.assertEqual(generate_report([-1, 1]), {"count": 2, "average": 0})
    def test_large(self): self.assertEqual(generate_report(list(range(100)))["count"], 100)
    def test_float(self): self.assertAlmostEqual(generate_report([1, 2])["average"], 1.5)
    def test_count(self): self.assertEqual(generate_report([10, 20, 30])["count"], 3)
    def test_type(self): self.assertIsInstance(generate_report([1, 2])["average"], float)
    def test_no_side_effects(self):
        data = [1, 2, 3]
        generate_report(data)
        self.assertEqual(data, [1, 2, 3])

if __name__ == '__main__':
    unittest.main()