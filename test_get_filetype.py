"""Testing `RefactorMovieFolder.get_filetype()`"""

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
TEST_1_INPUT = "C:/Lion.2016.720p.WEB-DL.x264.avi"
TEST_1_CORRECT = ".avi"
TEST_1_INFO = "With periods in filename."

TEST_2_INPUT = "C:/Movies/The Little Prince 2015.mkv"
TEST_2_CORRECT = ".mkv"
TEST_2_INFO = "With spaces in filename."

TEST_3_INPUT = "D:/Whiplash.Webm"
TEST_3_CORRECT = ".webm"
TEST_3_INFO = "4 character long file type."

TEST_4_INPUT = "D:/Avatar.AVCHD"
TEST_4_CORRECT = ".avchd"
TEST_4_INFO = "5 character long file type."

TEST_5_INPUT = "D:/Matrix Reloaded 2005"
TEST_5_CORRECT = ""
TEST_5_INFO = "Did not find a file type."


class Testing(unittest.TestCase):
    """
    Testing `RefactorMovieFolder.get_filetype()`
    """

    def __init__(self, method_name: str = "runTest") -> None:
        super().__init__(method_name)

    def test_1(self):
        """
        With periods in filename.
        """
        result = obj.get_filetype(TEST_1_INPUT)
        self.assertEqual(
            result,
            TEST_1_CORRECT,
            "Error: " + TEST_1_INFO,
        )

    def test_2(self):
        """
        With spaces in filename.
        """
        result = obj.get_filetype(TEST_2_INPUT)
        self.assertEqual(
            result,
            TEST_2_CORRECT,
            "Error: " + TEST_2_INFO,
        )

    def test_3(self):
        """
        4 character long file type.
        """
        result = obj.get_filetype(TEST_3_INPUT)
        self.assertEqual(
            result,
            TEST_3_CORRECT,
            "Error: " + TEST_3_INFO,
        )

    def test_4(self):
        """
        5 character long file type.
        """
        result = obj.get_filetype(TEST_4_INPUT)
        self.assertEqual(
            result,
            TEST_4_CORRECT,
            "Error: " + TEST_4_INFO,
        )

    def test_5(self):
        """
        Did not find a file type.
        """
        result = obj.get_filetype(TEST_5_INPUT)
        self.assertEqual(
            result,
            TEST_5_CORRECT,
            "Error: " + TEST_5_INFO,
        )


if __name__ == "__main__":
    unittest.main()
