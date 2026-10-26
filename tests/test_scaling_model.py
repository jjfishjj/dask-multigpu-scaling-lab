import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from scaling_model import evaluate


class ScalingModelTest(unittest.TestCase):
    def test_healthy_scaling(self):
        result = evaluate(4, 100, 30)
        self.assertEqual(result.speedup, 3.333)
        self.assertEqual(result.diagnosis, "healthy")

    def test_detects_scheduler_bound(self):
        self.assertIn("scheduler", evaluate(8, 100, 50).diagnosis)

    def test_rejects_invalid_timing(self):
        with self.assertRaises(ValueError):
            evaluate(0, 1, 1)


if __name__ == "__main__":
    unittest.main()
