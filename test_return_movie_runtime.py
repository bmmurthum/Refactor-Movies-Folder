"""Testing `MovieQueries.return_movie_runtime()`"""

# Unit Testing
import unittest

# # For quick allowance of pulling module from above.
# import sys

# # For quick allowance of pulling module from above.
# import pathlib

# To wait for API to have better connection
from time import sleep

# For handling read-timeout errors
import requests

# PARENT_PATH = str(pathlib.Path().resolve().parent)
# sys.path.append(PARENT_PATH)

# For storing my personal API key. In .gitignore.
from api_key import MyAPIKey

from refactor_movie_folder import MovieQueries as MQ

api_key = MyAPIKey.key
mq = MQ(api_key)

"""
TESTS
"""

# Monty Python and the Holy Grail id==762
TEST_1_INPUT = 762
TEST_1_CORRECT = 91
TEST_1_INFO = "Runtime in minutes. Monty Python and the Holy Grail."

# The Matrix id==603
TEST_2_INPUT = 603
TEST_2_CORRECT = 136
TEST_2_INFO = "Runtime in minutes. The Matrix."

# The Incredibles id=9806
TEST_3_INPUT = 9806
TEST_3_CORRECT = 115
TEST_3_INFO = "Runtime in minutes. The Incredibles."


class Testing(unittest.TestCase):
    """
    Testing `MovieQueries.return_movie_runtime()`
    """

    def __init__(self, method_name: str = "runTest") -> None:
        super().__init__(method_name)

    def test_1(self):
        """
        Runtime in minutes. Monty Python and the Holy Grail.
        """
        success = False
        result = None
        while success is False:
            try:
                result = mq.return_movie_runtime(TEST_1_INPUT)
                success = True
            except requests.exceptions.ReadTimeout as inst:
                print("Error: " + str(type(inst)))
                sleep(2)
            except Exception as inst:
                print("Error: " + str(type(inst)))
                sleep(2)
        self.assertEqual(
            result,
            TEST_1_CORRECT,
            "Error: " + TEST_1_INFO,
        )

    def test_2(self):
        """
        Runtime in minutes. The Matrix.
        """
        success = False
        result = None
        while success is False:
            try:
                result = mq.return_movie_runtime(TEST_2_INPUT)
                success = True
            except requests.exceptions.ReadTimeout as inst:
                print("Error: " + str(type(inst)))
                sleep(2)
            except Exception as inst:
                print("Error: " + str(type(inst)))
                sleep(2)
        self.assertEqual(
            result,
            TEST_2_CORRECT,
            "Error: " + TEST_2_INFO,
        )

    def test_3(self):
        """
        Runtime in minutes. The Incredibles.
        """
        success = False
        result = None
        while success is False:
            try:
                result = mq.return_movie_runtime(TEST_3_INPUT)
                success = True
            except requests.exceptions.ReadTimeout as inst:
                print("Error: " + str(type(inst)))
                sleep(2)
            except Exception as inst:
                print("Error: " + str(type(inst)))
                sleep(2)
        self.assertEqual(
            result,
            TEST_3_CORRECT,
            "Error: " + TEST_3_INFO,
        )


if __name__ == "__main__":
    unittest.main()
