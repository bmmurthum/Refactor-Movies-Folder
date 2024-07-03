"""Testing `RefactorMovieFolder.find_title_and_year()`"""

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
TEST_1_INPUT = "Eternal.Sunshine.of.the.Spotless.Mind.2004.1080p.BluRay.x264.anoXmous"
TEST_1_CORRECT = [
    ["eternal sunshine of spotless mind", "eternal sunshine", "of spotless mind"],
    "2004",
]
TEST_1_INFO = "Common title case. Longer and split. Separated with periods."

TEST_2_INPUT = "21 & Over (2013)"
TEST_2_CORRECT = [["21 over"], "2013"]
TEST_2_INFO = "Numbers in title to keep, and ampersand to remove."

TEST_3_INPUT = "Blade Runner 2049.HDRip.XviD.AC3-EVO"
TEST_3_CORRECT = [["blade runner"], "2049"]
TEST_3_INFO = "Year in title, no given release year."

TEST_4_INPUT = "Blade.Runner.2049.2017.720p.BluRay.x264-NeZu"
TEST_4_CORRECT = [["blade runner 2049"], "2017"]
TEST_4_INFO = "Year in title, with given release year."

TEST_5_INPUT = "Dark Star - John Carpenter Sci-Fi 1974 Eng Subs 1080p [H264-mp4]"
TEST_5_CORRECT = [
    ["dark star john carpenter", "dark star", "john carpenter"],
    "1974",
]
TEST_5_INFO = "First half, last half, being important. Removing some misc words."

TEST_6_INPUT = "Gladiator EXTENDED REMASTERED (2000)"
TEST_6_CORRECT = [
    ["gladiator"],
    "2000",
]
TEST_6_INFO = "Removing some misc words."

TEST_7_INPUT = "Howl's Moving Castle"
TEST_7_CORRECT = [
    ["howls moving castle"],
    "-1",
]
TEST_7_INFO = "No year, with apostrophe."

TEST_8_INPUT = "Borat 2011"
TEST_8_CORRECT = [
    ["borat"],
    "2011",
]
TEST_8_INFO = "One word title."

TEST_9_INPUT = "Batman V Superman 2012"
TEST_9_CORRECT = [
    ["batman superman"],
    "2012",
]
TEST_9_INFO = "Single letter omitted."


class Testing(unittest.TestCase):
    """
    Testing `RefactorMovieFolder.find_title_and_year()`
    """

    def __init__(self, method_name: str = "runTest") -> None:
        super().__init__(method_name)

    def test_1(self):
        """
        Common title case. Longer and split. Separated with periods.
        """
        result = obj.find_title_and_year(TEST_1_INPUT)
        self.assertEqual(
            result,
            TEST_1_CORRECT,
            "Error: " + TEST_1_INFO,
        )

    def test_2(self):
        """
        Year in title, no given release year.
        """
        result = obj.find_title_and_year(TEST_2_INPUT)
        self.assertEqual(
            result,
            TEST_2_CORRECT,
            "Error: " + TEST_2_INFO,
        )

    def test_3(self):
        """
        Year in title, no given release year.
        """
        result = obj.find_title_and_year(TEST_3_INPUT)
        self.assertEqual(
            result,
            TEST_3_CORRECT,
            "Error: " + TEST_3_INFO,
        )

    def test_4(self):
        """
        Year in title, with given release year.
        """
        result = obj.find_title_and_year(TEST_4_INPUT)
        self.assertEqual(
            result,
            TEST_4_CORRECT,
            "Error: " + TEST_4_INFO,
        )

    def test_5(self):
        """
        First half, last half, being important. Removing some misc words.
        """
        result = obj.find_title_and_year(TEST_5_INPUT)
        self.assertEqual(
            result,
            TEST_5_CORRECT,
            "Error: " + TEST_5_INFO,
        )

    def test_6(self):
        """
        Removing some misc words.
        """
        result = obj.find_title_and_year(TEST_6_INPUT)
        self.assertEqual(
            result,
            TEST_6_CORRECT,
            "Error: " + TEST_6_INFO,
        )

    def test_7(self):
        """
        No year, with apostrophe.
        """
        result = obj.find_title_and_year(TEST_7_INPUT)
        self.assertEqual(
            result,
            TEST_7_CORRECT,
            "Error: " + TEST_7_INFO,
        )

    def test_8(self):
        """
        One word title.
        """
        result = obj.find_title_and_year(TEST_8_INPUT)
        self.assertEqual(
            result,
            TEST_8_CORRECT,
            "Error: " + TEST_8_INFO,
        )

    def test_9(self):
        """
        Single letter omitted.
        """
        result = obj.find_title_and_year(TEST_9_INPUT)
        self.assertEqual(
            result,
            TEST_9_CORRECT,
            "Error: " + TEST_9_INFO,
        )


if __name__ == "__main__":
    unittest.main()
