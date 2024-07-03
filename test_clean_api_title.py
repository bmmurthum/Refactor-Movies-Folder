"""Testing `MovieQueries.clean_api_title()`"""

# Unit Testing
import unittest

# # For quick allowance of pulling module from above.
# import sys

# # For quick allowance of pulling module from above.
# import pathlib

# PARENT_PATH = str(pathlib.Path().resolve().parent)
# sys.path.append(PARENT_PATH)

from refactor_movie_folder import MovieQueries as MQ

mq = MQ()

"""
TESTS
"""
TEST_1_INPUT = "Monty Python & the Holy Grail"
TEST_1_CORRECT = "montypythonholygrail"
TEST_1_INFO = "Removing ampersand, and 'the'."

TEST_2_INPUT = "Monty Python And The Holy Grail"
TEST_2_CORRECT = "montypythonholygrail"
TEST_2_INFO = "Removing 'and', and making lowercase."

TEST_3_INPUT = "The King's Speech"
TEST_3_CORRECT = "kingsspeech"
TEST_3_INFO = "Remove apostrophe. Remove 'the'."

TEST_4_INPUT = "The Loft"
TEST_4_CORRECT = "theloft"
TEST_4_INFO = "If two words, remove no words."

TEST_5_INPUT = "Toy Story 2"
TEST_5_CORRECT = "toystory2"
TEST_5_INFO = "Keep numbers in titles."

TEST_6_INPUT = "World War Z"
TEST_6_CORRECT = "worldwar"
TEST_6_INFO = "Remove single letters, unless allowed."

TEST_7_INPUT = "1917"
TEST_7_CORRECT = "1917"
TEST_7_INFO = "If one word, don't do any removal of words."


class Testing(unittest.TestCase):
    """
    Testing `MovieQueries.clean_api_title()`
    """

    def __init__(self, method_name: str = "runTest") -> None:
        super().__init__(method_name)

    def test_1(self):
        """
        Removing ampersand, and 'the'.
        """
        result = mq.clean_api_title(TEST_1_INPUT)
        self.assertEqual(
            result,
            TEST_1_CORRECT,
            "Error: " + TEST_1_INFO,
        )

    def test_2(self):
        """
        Removing 'and', and making lowercase.
        """
        result = mq.clean_api_title(TEST_2_INPUT)
        self.assertEqual(
            result,
            TEST_2_CORRECT,
            "Error: " + TEST_2_INFO,
        )

    def test_3(self):
        """
        Remove apostrophe. Remove 'the'.
        """
        result = mq.clean_api_title(TEST_3_INPUT)
        self.assertEqual(
            result,
            TEST_3_CORRECT,
            "Error: " + TEST_3_INFO,
        )

    def test_4(self):
        """
        If two words, remove no words.
        """
        result = mq.clean_api_title(TEST_4_INPUT)
        self.assertEqual(
            result,
            TEST_4_CORRECT,
            "Error: " + TEST_4_INFO,
        )

    def test_5(self):
        """
        Keep numbers in titles.
        """
        result = mq.clean_api_title(TEST_5_INPUT)
        self.assertEqual(
            result,
            TEST_5_CORRECT,
            "Error: " + TEST_5_INFO,
        )

    def test_6(self):
        """
        Remove single letters, unless allowed.
        """
        result = mq.clean_api_title(TEST_6_INPUT)
        self.assertEqual(
            result,
            TEST_6_CORRECT,
            "Error: " + TEST_6_INFO,
        )

    def test_7(self):
        """
        If one word, don't do any removal of words.
        """
        result = mq.clean_api_title(TEST_7_INPUT)
        self.assertEqual(
            result,
            TEST_7_CORRECT,
            "Error: " + TEST_7_INFO,
        )


if __name__ == "__main__":
    unittest.main()
