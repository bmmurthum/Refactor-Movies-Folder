"""Testing `MovieQueries.get_percent_word_match()`"""

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

Getting above a 0.5 threshold, with only one title found on a query allows for 
auto-confirmation on a title.
"""

TEST_1_INPUT_A = "Wallace & Gromit: The Curse of the Were-Rabbit"
# -> "wallace gromit curse were rabbit"
TEST_1_INPUT_B = "wallace gromit curse of were rabbit"
TEST_1_CORRECT = 1.0
TEST_1_INFO = (
    "Removing ampersand, ':', '-', 'the', 'of', makes lowercase. Then compares."
)

TEST_2_INPUT_A = "The Making of Wallace & Gromit: The Curse of the Were-Rabbit"
# -> "making wallace gromit curse were rabbit"
TEST_2_INPUT_B = "wallace gromit curse of were rabbit"
# -> "wallace gromit curse were rabbit"
TEST_2_CORRECT = 5 / 6
TEST_2_INFO = "Would allow for auto-confirmation."

TEST_3_INPUT_A = "Birdman or (The Unexpected Virtue of Ignorance)"
# -> "birdman or unexpected virtue ignorance"
TEST_3_INPUT_B = "birdman"
TEST_3_CORRECT = 0.2
TEST_3_INFO = "Removing 'the', 'of', parentheses, makes lowercase. Our desired title, but not a good enough match for auto-confirmation."

TEST_4_INPUT_A = "The Amazing Spider-Man 2"
# -> "amazing spider man 2"
TEST_4_INPUT_B = "amazing spider man 2"
TEST_4_CORRECT = 1.0
TEST_4_INFO = "That's a solid match."

TEST_5_INPUT_A = "Swap Meet at the Love Shack"
# -> "swap meet at love shack"
TEST_5_INPUT_B = "shack"
TEST_5_CORRECT = 0.2
TEST_5_INFO = "Our title is within the found title, but not enough for confirmation."

TEST_6_INPUT_A = "Batman V Superman: Dawn of Justice"
# -> "batman superman dawn justice" & "batman superman"
TEST_6_INPUT_B = "batman v superman"
TEST_6_CORRECT = 2 / 4
TEST_6_INFO = "Omitting the 'v' in our consideration."

TEST_7_INPUT_A = "Harry Potter and the Philosopher's Stone"
# -> "harry potter philosophers stone"
TEST_7_INPUT_B = "harry potter philosophers stone"
TEST_7_CORRECT = 1.0
TEST_7_INFO = "Removing the apostrophe."


class Testing(unittest.TestCase):
    """
    Testing `MovieQueries.get_percent_word_match()`
    """

    def __init__(self, method_name: str = "runTest") -> None:
        super().__init__(method_name)

    def test_1(self):
        """
        Removing ampersand, ':', '-', 'the', 'of', makes lowercase. Then
        compares.
        """
        result = mq.get_percent_word_match(TEST_1_INPUT_A, TEST_1_INPUT_B)
        self.assertEqual(
            result,
            TEST_1_CORRECT,
            "Error: " + TEST_1_INFO,
        )

    def test_2(self):
        """
        Would allow for auto-confirmation.
        """
        result = mq.get_percent_word_match(TEST_2_INPUT_A, TEST_2_INPUT_B)
        self.assertEqual(
            result,
            TEST_2_CORRECT,
            "Error: " + TEST_2_INFO,
        )

    def test_3(self):
        """
        Removing 'the', 'of', parentheses, makes lowercase. Our desired title,
        but not a good enough match for auto-confirmation.
        """
        result = mq.get_percent_word_match(TEST_3_INPUT_A, TEST_3_INPUT_B)
        self.assertEqual(
            result,
            TEST_3_CORRECT,
            "Error: " + TEST_3_INFO,
        )

    def test_4(self):
        """
        That's a solid match.
        """
        result = mq.get_percent_word_match(TEST_4_INPUT_A, TEST_4_INPUT_B)
        self.assertEqual(
            result,
            TEST_4_CORRECT,
            "Error: " + TEST_4_INFO,
        )

    def test_5(self):
        """
        Our title is within the found title, but not enough for confirmation.
        """
        result = mq.get_percent_word_match(TEST_5_INPUT_A, TEST_5_INPUT_B)
        self.assertEqual(
            result,
            TEST_5_CORRECT,
            "Error: " + TEST_5_INFO,
        )

    def test_6(self):
        """
        Omitting the 'v' in our consideration.
        """
        result = mq.get_percent_word_match(TEST_6_INPUT_A, TEST_6_INPUT_B)
        self.assertEqual(
            result,
            TEST_6_CORRECT,
            "Error: " + TEST_6_INFO,
        )

    def test_7(self):
        """
        Removing the apostrophe.
        """
        result = mq.get_percent_word_match(TEST_7_INPUT_A, TEST_7_INPUT_B)
        self.assertEqual(
            result,
            TEST_7_CORRECT,
            "Error: " + TEST_7_INFO,
        )


if __name__ == "__main__":
    unittest.main()
