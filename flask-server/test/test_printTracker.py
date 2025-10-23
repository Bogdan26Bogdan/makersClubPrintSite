import unittest
from db import db


class TestprintTracker(unittest.TestCase):
    def test_validate_GramsUsed(self):
        """Test the validate_GramsUsed function."""
        from db.print_tracker import validate_GramsUsed

        valid_cases = {
            "1500": (True, 1500),
            "15.5": (True, 1550),
            "0.75": (True, 75),
            "200g": (True, 200),
            "3.2g": (True, 320),
            "7.00": (True, 700),
            "100g": (True, 100),
            "0g": (True, 0),
        }

        invalid_cases = [
            "abc",
            "12.34.56",
            "12.a3",
            "",
            "   ",
            "12..34",
            "12.345",
        ]

        for input_value, expected in valid_cases.items():
            result = validate_GramsUsed(input_value)
            self.assertEqual(
                result,
                expected,
                f"Failed for input: {input_value}. Expected {expected}, got {result}",
            )

        for input_value in invalid_cases:
            result = validate_GramsUsed(input_value)
            self.assertEqual(
                result,
                (False, 0),
                f"Failed for input: {input_value}. Expected (False, 0), got {result}",
            )