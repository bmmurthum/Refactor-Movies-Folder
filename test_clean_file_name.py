"""Testing `RefactorMovieFolder.clean_file_name()`"""

# Unit Testing
import unittest

# # For quick allowance of pulling module from above.
# import sys

# # For quick allowance of pulling module from above.
# import pathlib

# PARENT_PATH = str(pathlib.Path().resolve().parent)
# sys.path.append(PARENT_PATH)

from refactor_movie_folder import RefactorMovieFolder as RMF

obj = RMF()

"""
TESTS
"""
TEST_1_INPUT = "Ace Ventura: When Nature Calls"
TEST_1_CORRECT = "Ace Ventura When Nature Calls"
TEST_1_INFO = "Removes colon."

TEST_2_INPUT = "What Do We Do Now?"
TEST_2_CORRECT = "What Do We Do Now"
TEST_2_INFO = "Removes question mark."

TEST_3_INPUT = "Whiplash"
TEST_3_CORRECT = "Whiplash"
TEST_3_INFO = "Removes nothing."


class Testing(unittest.TestCase):
    """
    Testing `RefactorMovieFolder.confirm_as_absolute_path()`
    """

    def __init__(self, method_name: str = "runTest") -> None:
        super().__init__(method_name)

    def test_1(self):
        """
        Removes colon.
        """
        result = obj.clean_file_name(TEST_1_INPUT)
        self.assertEqual(
            result,
            TEST_1_CORRECT,
            "Error: " + TEST_1_INFO,
        )

    def test_2(self):
        """
        Removes question mark.
        """
        result = obj.clean_file_name(TEST_2_INPUT)
        self.assertEqual(
            result,
            TEST_2_CORRECT,
            "Error: " + TEST_2_INFO,
        )

    def test_3(self):
        """
        Removes nothing.
        """
        result = obj.clean_file_name(TEST_3_INPUT)
        self.assertEqual(
            result,
            TEST_3_CORRECT,
            "Error: " + TEST_3_INFO,
        )


if __name__ == "__main__":
    unittest.main()
