"""Testing `RefactorMovieFolder.confirm_as_absolute_path()`"""

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
TEST_1_INPUT = "C:/users/"
TEST_1_CORRECT = True
TEST_1_INFO = "Correct format, with trailing end slash."

TEST_2_INPUT = "C:\\users\\"
TEST_2_CORRECT = False
TEST_2_INFO = "Incorrect format, using backslashes."

TEST_3_INPUT = "C:/users"
TEST_3_CORRECT = True
TEST_3_INFO = "Correct format, without trailing end slash."

TEST_4_INPUT = "D:/users"
TEST_4_CORRECT = True
TEST_4_INFO = "Correct format, different drive letter."

TEST_5_INPUT = "D:/users\\pictures\\"
TEST_5_CORRECT = False
TEST_5_INFO = "Incorrect format, contains backslashes."

TEST_6_INPUT = "D:/users/dave/../frank/"
TEST_6_CORRECT = False
TEST_6_INFO = "Incorrect format, contains double period."

TEST_7_INPUT = "2:/users/"
TEST_7_CORRECT = False
TEST_7_INFO = "Incorrect format, non-alpha in first position."

TEST_8_INPUT = "/home/users/jim"
TEST_8_CORRECT = False
TEST_8_INFO = "Incorrect format, is Linux format."

TEST_9_INPUT = "D:users"
TEST_9_CORRECT = False
TEST_9_INFO = "Badly written file path."

TEST_10_INPUT = "C:/users/david*was*here/"
TEST_10_CORRECT = False
TEST_10_INFO = "Incorrect. Cannot include banned characters."


class Testing(unittest.TestCase):
    """
    Testing `RefactorMovieFolder.confirm_as_absolute_path()`
    """

    def __init__(self, method_name: str = "runTest") -> None:
        super().__init__(method_name)

    def test_1(self):
        """
        A valid case.
        """
        result = obj.confirm_as_absolute_path(TEST_1_INPUT)
        self.assertEqual(
            result,
            TEST_1_CORRECT,
            "Error: " + TEST_1_INFO,
        )

    def test_2(self):
        """
        Tests the common Windows file path.
        """
        result = obj.confirm_as_absolute_path(TEST_2_INPUT)
        self.assertEqual(
            result,
            TEST_2_CORRECT,
            "Error: " + TEST_2_INFO,
        )

    def test_3(self):
        """
        Tests a valid case, without the optional last trailing forward-slash.
        """
        result = obj.confirm_as_absolute_path(TEST_3_INPUT)
        self.assertEqual(
            result,
            TEST_3_CORRECT,
            "Error: " + TEST_3_INFO,
        )

    def test_4(self):
        """
        Tests a valid case, with a different drive letter.
        """
        result = obj.confirm_as_absolute_path(TEST_4_INPUT)
        self.assertEqual(
            result,
            TEST_4_CORRECT,
            "Error: " + TEST_4_INFO,
        )

    def test_5(self):
        """
        Tests an incorrect case. Containing backslashes.
        """
        result = obj.confirm_as_absolute_path(TEST_5_INPUT)
        self.assertEqual(
            result,
            TEST_5_CORRECT,
            "Error: " + TEST_5_INFO,
        )

    def test_6(self):
        """
        Tests an incorrect case. Containing double periods.
        """
        result = obj.confirm_as_absolute_path(TEST_6_INPUT)
        self.assertEqual(
            result,
            TEST_6_CORRECT,
            "Error: " + TEST_6_INFO,
        )

    def test_7(self):
        """
        Tests an incorrect case. Containing backslashes.
        """
        result = obj.confirm_as_absolute_path(TEST_7_INPUT)
        self.assertEqual(
            result,
            TEST_7_CORRECT,
            "Error: " + TEST_7_INFO,
        )

    def test_8(self):
        """
        Tests an incorrect case. Containing backslashes.
        """
        result = obj.confirm_as_absolute_path(TEST_8_INPUT)
        self.assertEqual(
            result,
            TEST_8_CORRECT,
            "Error: " + TEST_8_INFO,
        )

    def test_9(self):
        """
        Tests an incorrect case. Containing backslashes.
        """
        result = obj.confirm_as_absolute_path(TEST_9_INPUT)
        self.assertEqual(
            result,
            TEST_9_CORRECT,
            "Error: " + TEST_9_INFO,
        )

    def test_10(self):
        """
        Tests an incorrect case. Containing backslashes.
        """
        result = obj.confirm_as_absolute_path(TEST_10_INPUT)
        self.assertEqual(
            result,
            TEST_10_CORRECT,
            "Error: " + TEST_10_INFO,
        )


if __name__ == "__main__":
    unittest.main()
