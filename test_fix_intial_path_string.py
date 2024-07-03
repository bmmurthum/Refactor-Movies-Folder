"""Testing `RefactorMovieFolder.fix_initial_path_string()`"""

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
TEST_1_INPUT = "C:\\Movies"
TEST_1_CORRECT = "C:/Movies/"
TEST_1_INFO = "Standard Windows input, without trailing end slash."

TEST_2_INPUT = "C:\\users\\david\\movies\\"
TEST_2_CORRECT = "C:/users/david/movies/"
TEST_2_INFO = "Standard Windows input, with trailing end slash."

TEST_3_INPUT = "B:/Movies/"
TEST_3_CORRECT = "B:/Movies/"
TEST_3_INFO = "Already in desired format, with trailing end slash."

TEST_4_INPUT = "D:/Movies"
TEST_4_CORRECT = "D:/Movies/"
TEST_4_INFO = "Already in desired format, without trailing end slash."

TEST_5_INPUT = "D:/Files\\Movies\\"
TEST_5_CORRECT = "D:/Files/Movies/"
TEST_5_INFO = "Catching backslashes."


class Testing(unittest.TestCase):
    """
    Testing `RefactorMovieFolder.fix_initial_path_string()`
    """

    def __init__(self, method_name: str = "runTest") -> None:
        super().__init__(method_name)

    def test_1(self):
        """
        Standard Windows input, without trailing end slash.
        """
        result = obj.fix_initial_path_string(TEST_1_INPUT)
        self.assertEqual(
            result,
            TEST_1_CORRECT,
            "Error: " + TEST_1_INFO,
        )

    def test_2(self):
        """
        Standard Windows input, with trailing end slash.
        """
        result = obj.fix_initial_path_string(TEST_2_INPUT)
        self.assertEqual(
            result,
            TEST_2_CORRECT,
            "Error: " + TEST_2_INFO,
        )

    def test_3(self):
        """
        Already in desired format, with trailing end slash.
        """
        result = obj.fix_initial_path_string(TEST_3_INPUT)
        self.assertEqual(
            result,
            TEST_3_CORRECT,
            "Error: " + TEST_3_INFO,
        )

    def test_4(self):
        """
        Already in desired format, without trailing end slash.
        """
        result = obj.fix_initial_path_string(TEST_4_INPUT)
        self.assertEqual(
            result,
            TEST_4_CORRECT,
            "Error: " + TEST_4_INFO,
        )

    def test_5(self):
        """
        Catching backslashes.
        """
        result = obj.fix_initial_path_string(TEST_5_INPUT)
        self.assertEqual(
            result,
            TEST_5_CORRECT,
            "Error: " + TEST_5_INFO,
        )


if __name__ == "__main__":
    unittest.main()
