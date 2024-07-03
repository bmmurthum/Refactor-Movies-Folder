"""Testing `MovieQueries.return_new_movie_filename()`"""

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

# id=602
TEST_1_TITLE_LIST = ["independence day"]
TEST_1_YEAR = "1996"
TEST_1_RUNTIME = 143
TEST_1_WITH_ENGLISH = True
TEST_1_CORRECT = ("Independence Day (1996)", "1996")
TEST_1_INFO = "Two word title, with given year."

# id=16859
TEST_2_TITLE_LIST = (
    "kikis delivery service majo no takkyubin",
    "kikis delivery service",
    "majo no takkyubin",
)
TEST_2_YEAR = "1989"
TEST_2_RUNTIME = 103
TEST_2_WITH_ENGLISH = False
TEST_2_CORRECT = ("Kiki's Delivery Service (1989)", "1989")
TEST_2_INFO = "Not in english, might need the split title for good search."

# id=858
TEST_3_TITLE_LIST = ["sleepless in seattle"]
TEST_3_YEAR = "-1"
TEST_3_RUNTIME = 105
TEST_3_WITH_ENGLISH = True
TEST_3_CORRECT = ("Sleepless in Seattle (1993)", "1993")
TEST_3_INFO = "No given year."

# id=335984
TEST_4_TITLE_LIST = ["blade runner"]
TEST_4_YEAR = "2049"
TEST_4_RUNTIME = 160
TEST_4_WITH_ENGLISH = True
TEST_4_CORRECT = ("Blade Runner 2049 (2017)", "2017")
TEST_4_INFO = "Year accidentally pulled from title."

# id=205
TEST_5_TITLE_LIST = ["hotel rawanda"]
TEST_5_YEAR = "2008"
TEST_5_RUNTIME = 121
TEST_5_WITH_ENGLISH = True
TEST_5_CORRECT = ("NOT FOUND", "-1")
TEST_5_INFO = "Mistype in title, leads to not confirmed."

# id=2011
TEST_6_TITLE_LIST = ["persepolis"]
TEST_6_YEAR = "-1"
TEST_6_RUNTIME = 90
TEST_6_WITH_ENGLISH = True
TEST_6_CORRECT = ("NOT FOUND", "-1")
TEST_6_INFO = "No titles in English, leads to not confirmed."

# id=2011
TEST_7_TITLE_LIST = ["persepolis"]
TEST_7_YEAR = "-1"
TEST_7_RUNTIME = 90
TEST_7_WITH_ENGLISH = False
TEST_7_CORRECT = ("Persepolis (2007)", "2007")
TEST_7_INFO = "Searching without English, leads to confirmed."


class Testing(unittest.TestCase):
    """
    Testing `MovieQueries.return_movie_runtime()`
    """

    def __init__(self, method_name: str = "runTest") -> None:
        super().__init__(method_name)

    def test_1(self):
        """
        Two word title, with given year.
        """
        success = False
        result = None
        while success is False:
            try:
                result = mq.return_new_movie_filename(
                    TEST_1_TITLE_LIST, TEST_1_YEAR, TEST_1_RUNTIME, TEST_1_WITH_ENGLISH
                )
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
        Not in english, might need the split title for good search.
        """
        success = False
        result = None
        while success is False:
            try:
                result = mq.return_new_movie_filename(
                    TEST_2_TITLE_LIST, TEST_2_YEAR, TEST_2_RUNTIME, TEST_2_WITH_ENGLISH
                )
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
        No given year.
        """
        success = False
        result = None
        while success is False:
            try:
                result = mq.return_new_movie_filename(
                    TEST_3_TITLE_LIST, TEST_3_YEAR, TEST_3_RUNTIME, TEST_3_WITH_ENGLISH
                )
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

    def test_4(self):
        """
        Year accidentally pulled from title.
        """
        success = False
        result = None
        while success is False:
            try:
                result = mq.return_new_movie_filename(
                    TEST_4_TITLE_LIST, TEST_4_YEAR, TEST_4_RUNTIME, TEST_4_WITH_ENGLISH
                )
                success = True
            except requests.exceptions.ReadTimeout as inst:
                print("Error: " + str(type(inst)))
                sleep(2)
            except Exception as inst:
                print("Error: " + str(type(inst)))
                sleep(2)
        self.assertEqual(
            result,
            TEST_4_CORRECT,
            "Error: " + TEST_4_INFO,
        )

    def test_5(self):
        """
        Mistype in title, leads to not confirmed.
        """
        success = False
        result = None
        while success is False:
            try:
                result = mq.return_new_movie_filename(
                    TEST_5_TITLE_LIST, TEST_5_YEAR, TEST_5_RUNTIME, TEST_5_WITH_ENGLISH
                )
                success = True
            except requests.exceptions.ReadTimeout as inst:
                print("Error: " + str(type(inst)))
                sleep(2)
            except Exception as inst:
                print("Error: " + str(type(inst)))
                sleep(2)
        self.assertEqual(
            result,
            TEST_5_CORRECT,
            "Error: " + TEST_5_INFO,
        )

    def test_6(self):
        """
        No titles in English, leads to not confirmed.
        """
        success = False
        result = None
        while success is False:
            try:
                result = mq.return_new_movie_filename(
                    TEST_6_TITLE_LIST, TEST_6_YEAR, TEST_6_RUNTIME, TEST_6_WITH_ENGLISH
                )
                success = True
            except requests.exceptions.ReadTimeout as inst:
                print("Error: " + str(type(inst)))
                sleep(2)
            except Exception as inst:
                print("Error: " + str(type(inst)))
                sleep(2)
        self.assertEqual(
            result,
            TEST_6_CORRECT,
            "Error: " + TEST_6_INFO,
        )

    def test_7(self):
        """
        Too many similar titles, leads to not confirmed.
        """
        success = False
        result = None
        while success is False:
            try:
                result = mq.return_new_movie_filename(
                    TEST_7_TITLE_LIST, TEST_7_YEAR, TEST_7_RUNTIME, TEST_7_WITH_ENGLISH
                )
                success = True
            except requests.exceptions.ReadTimeout as inst:
                print("Error: " + str(type(inst)))
                sleep(2)
            except Exception as inst:
                print("Error: " + str(type(inst)))
                sleep(2)
        self.assertEqual(
            result,
            TEST_7_CORRECT,
            "Error: " + TEST_7_INFO,
        )


if __name__ == "__main__":
    unittest.main()
