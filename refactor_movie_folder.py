""" Module for refactoring a directory of movie files. """

# Pylint not recognizing tmdb's member variables
# pylint: disable=E0611
# Let's not care about exception types
# pylint: disable=W0702
# Pylint is acting like cv2 doesn't import?
# pylint: disable=E0401
# Pylint not recognizing CV2's member variables
# pylint: disable=E1101
# Pylint not allowing catch-all after specific check
# pylint: disable=W0718

# cSpell:disable

# Regular expression
import re

# File handling
import os

# To wait for API to have better connection
from time import sleep

# For handling read-timeout errors
import requests

# For checking movie runtime
import cv2

# A wrapper for interacting with https://www.themoviedb.org API
import tmdbsimple as tmdb


def main():
    """Main code to run."""

    # REPLACE YOUR OUTPUT FILE HERE
    # A file path to record changes of files to a text file.
    #  - Useful to overlook any possible mistaken changes.
    #  - Leave empty to not create an output file.
    # output_file_path = "J:/users/dave/log.txt"
    output_file_path = "___"

    # REPLACE YOUR API KEY HERE
    #  - Get one here: https://www.themoviedb.org/settings/api
    # api_key = "f073daaexxxxxxxxe3012d018bfexxxxx"
    api_key = "___"

    # Movies with run times smaller than this will be deleted.
    #  - Cleans false movies and corrupt movies.
    #  - Change, if wanting to allow for low run time movies.
    smallest_run_time = 20

    try:
        path_str = input("Enter Directory Path: ")
    except:
        print("Error: Needs valid destination path.")
        return
    RefactorMovieFolder().refactor_movie_directory(
        path_str, output_file_path, smallest_run_time, api_key
    )


class RefactorMovieFolder:
    """
    Contains methods to refactor a directory full of movies.

    Requires:
        - `pip tmdbsimple` to interact with a movie database.
        - An API access key with https://www.themoviedb.org/.
        - `pip opencv-python` to read movie-file duration.
        - `pip requests` to handle errors.
        - `pip regex` to pull the year from a file name.
    """

    def confirm_as_absolute_path(self, path: str) -> bool:
        """
        Confirms the path is a valid absolute path. And in our desired format
        without backslashes.

        Args:
            `path`: Given path string.
        Returns:
            `True/False`: Whether is valid absolute path.
        """
        banned_characters = ["<", ">", ":", "\\", "|", "?", "*", ".."]
        if path[0].isalpha() and path[1] == ":" and path[2] == "/":
            for i in banned_characters:
                if i in path[2:]:
                    return False
            return True
        else:
            return False

    def fix_initial_path_string(self, path: str) -> str:
        """
        Fixes Window's version of file path. If the user pastes from folder
        path. Backslashes are made to forward slashes. Forward slash is added
        to end if not found.

        Does not validate. Does not correct other erant file paths.

        Ex: "C:\\Users" -> "C:/Users/"

        Args:
            `path`: Given path string.
        Returns:
            `new_path`: The fixed path string.
        """
        new_path = path
        while "\\" in new_path:
            new_path = new_path.replace("\\", "/")
        if new_path[-1] != "/":
            new_path += "/"
        return new_path

    def find_title_and_year(self, filename: str) -> list[str, str]:
        """
        Looks at a given dir/file name to return a simple title and year. Uses
        Regex and formatting to find a basic title-year to search on a database.

        Args:
            `filename`: The filename being looked at.
        Returns:
            `title_list`: lowercase string of words in title, and possibly
                first and last half of this string separately.
            `year`: release year of the movie
        """
        title = ""
        title_first_half = ""
        title_last_half = ""
        year = ""

        # Clean up the filename
        filename = str.lower(filename)
        remove_list = [
            "1080p",
            "1080",
            "720p",
            "720",
            "480p",
            "480",
            "web-dl",
            "(",
            ")",
            "[",
            "]",
            "{",
            "}",
            "&",
            ".",
            ",",
            "-",
            "_",
            "=",
            "~",
        ]
        for item in remove_list:
            while item in filename:
                filename = filename.replace(item, " ")
        while "  " in filename:
            filename = filename.replace("  ", " ")
        while "'" in filename:
            filename = filename.replace("'", "")
        filename += " "

        # Try to retrieve some words and a year
        # Find year by looking for four numbers with spaces adjacent " 1234 "
        # temp = re.findall(r"((\s)([\d]{4})(\s))", filename)
        temp = re.findall(r"\d{4}\s", filename)
        if len(temp) == 0:
            year = "-1"
        elif len(temp) == 1:
            year = temp[0]
        else:
            year = temp[1]
        year = year.strip()

        # Build title, consider by word.
        # - Disallow single letter words: "g i joe, "u s a", "2"
        # - Disallow common words that are mistaken: "and", "the"
        # - Remove information words: "dc", "version", "edition"
        forbidden_words = [
            "and",
            "the",
            "part",
            "aka",
            "directors",
            "cut",
            "dc",
            "version",
            "remastered",
            "uncut",
            "unrated",
            "extended",
            "usabit",
            "torrenting",
            "usabit",
            "www",
            "com",
            "org",
            "dvdrip",
            "xvid",
            "x264",
            "264",
            "aac",
            "etrg",
            "hdrip",
            "x26",
            "webrip",
            "brrip",
            "bluray",
            "special",
            "edition",
            "extended",
            "se",
            "avi",
            "mp4",
            "mpg",
            "mov",
            "mkv",
            "aac2",
            "sci",
            "fi",
        ]
        allowed_single_letters = ["a", "e", "i", "o", "x"]
        # Get title up to year
        words = filename.split(" ")
        for i, w in enumerate(words):
            if w == year:
                break
            title += w + " "
        title = title.strip()
        # Remove particular words from title
        words = title.split(" ")
        if len(words) == 2:
            title = words[0] + " " + words[1]
        elif len(words) == 1:
            pass
        else:
            title = ""
            for i, w in enumerate(words):
                if w in forbidden_words:
                    continue
                if len(w) == 1 and i != 0:
                    if not (w.isnumeric() or w in allowed_single_letters):
                        continue
                title += w + " "
        title = title.strip()
        # Create variations of the title to search with
        words = title.split(" ")
        if len(words) < 4:
            title_list = [title]
            return [title_list, year]
        else:
            words = title.split(" ")
            a = len(words) // 2
            for w in range(0, a):
                title_first_half += words[w] + " "
            for w in range(a, len(words)):
                title_last_half += words[w] + " "
            title_first_half = title_first_half.strip()
            title_last_half = title_last_half.strip()

            title_list = [title, title_first_half, title_last_half]
            return [title_list, year]

    def get_filetype(self, path: str) -> str:
        """
        Return's a file's filetype. In lowercase, with its period.

        Args:
            `path`: A string of the path of the item looked at.
        Returns:
            `file_type`: A string of the file's filetype ".txt"
        """
        file_type = ""
        i = len(path) - 1
        count = 0
        while True:
            if path[i] == ".":
                file_type = "." + path[-count:]
                file_type = file_type.lower()
                break
            count += 1
            i -= 1
            if count > 5:
                break
        return file_type

    def clean_file_name(self, title_file_name: str) -> str:
        """
        Cleans the title file name to avoid Window's invalid characters.

        Args:
            `title_file_name`: File name based on movie title and year.
        Returns:
            `new_file_name`: Cleaned file name.
        """
        new_file_name = str(title_file_name)
        windows_invalid_chars = ["<", ">", ":", '"', "/", "\\", "|", "?", "*"]
        for char in windows_invalid_chars:
            while char in new_file_name:
                new_file_name = new_file_name.replace(char, "")
        return new_file_name

    def get_directory_size(self, path: str) -> str:
        """
        Given a directory, returns a string of the size of total files inside.

        Args:
            `path`: The absolute path of the directory to look at.
        Returns:
            `return_str`: The formatted string of the foldersize.
        """
        size = 0
        for path, _, files in os.walk(path):
            for f in files:
                fp = os.path.join(path, f)
                size += os.stat(fp).st_size
        total_GB = size / 1000000000
        total_TB = None
        return_str = None
        if total_GB > 1000:
            total_TB = round(total_GB / 1000, 2)
            return_str = str(total_TB) + "TB"
        else:
            total_GB = round(total_GB, 2)
            return_str = str(total_GB) + "GB"
        return return_str

    def get_filesize(self, path: str, entry_item) -> int:
        """
        Return the filesize of the movie. Involved with an item from the `os.scandir(path)` iterable.

        Args:
            `path`: Path to this directory/file
            `entry_item`: Object of directory search enumeration. Folder/File.
        Returns:
            `file_size`: The number of bytes of the largest item in this
                directory, or the size of this file.
        """
        file_size = 0
        try:
            if entry_item.is_dir():
                movie_file_path, _ = self.find_largest_in_folder(
                    path + entry_item.name + "/"
                )
                file_size = os.path.getsize(movie_file_path)
            elif entry_item.is_file():
                movie_file_path = path + entry_item.name
                file_size = os.path.getsize(movie_file_path)
        except:
            file_size = 0
        return file_size

    def find_runtime(self, path: str, entry_item) -> list[int, bool]:
        """
        Find the runtime of a file in minutes. This will help in identifying
        the correct movie in the database.

        Args:
            `path`: The file path to the folder this is inside.
            `entry_item`: Object of directory search enumeration. Folder/File.
        Returns:
            `minutes`: Found runtime of movie file. Given as int.
            `is_empty_folder`: True if there was not an item in this directory.
        """
        minutes = 0
        is_empty_folder = True
        try:
            if entry_item.is_dir():
                movie_file_path, _ = self.find_largest_in_folder(
                    path + entry_item.name + "/"
                )
                if movie_file_path != "":
                    is_empty_folder = False
                data = cv2.VideoCapture(movie_file_path)
                frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
                fps = data.get(cv2.CAP_PROP_FPS)
                minutes = int(round(frames / (fps * 60)))
            elif entry_item.is_file():
                movie_file_path = path + entry_item.name
                data = cv2.VideoCapture(movie_file_path)
                frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
                fps = data.get(cv2.CAP_PROP_FPS)
                minutes = int(round(frames / (fps * 60)))
                is_empty_folder = False
        except:
            minutes = -1
        if minutes < 0:
            minutes = -1
        return [minutes, is_empty_folder]

    def refactor_movie_directory(
        self, path: str, output_file_path: str, smallest_run_time: int, api_key: str
    ) -> None:
        """
        This method restructures and renames file and folders of movies to
        better match their titles and years of release.

        It requires some user input as it runs, to choose correct movies in the
        case of duplicates of titles, or missing titles.

        If it doesn't find a match, it leaves the file/folder alone, to later
        be handled with user.

        If duplicate, we remove the file that is lower filesize.

        There is some chance of false-positives in bad renames. Found to be
        less than 0.01% in test case.

        Args:
            `path`: Path to the directory to edit. Ex: "I:/Movies/"
            `output_file_path`: Path to the text file of changes record.
            `smallest_run_time`: Files smaller than this are deleted.
            `api_key`: API key for the movie database.
        """

        # Fix path string if in Window's format
        path = self.fix_initial_path_string(path)
        # Confirm as absolute path
        if not self.confirm_as_absolute_path(path):
            print("Error: Not absolute path.")
            return

        # Confirm correct directory with user
        directories = os.scandir(path)
        print("Directory: " + path)
        i = 0
        for entry in directories:
            print(" - " + entry.name)
            i += 1
            if i > 4:
                break
        print(" - ...")
        print("This is the selected directory.")
        confirm = input("Continue? y/n: ")
        if confirm != "y":
            return

        # Fix path string if in Window's format
        if output_file_path == "___":
            output_file_path = ""
        else:
            output_file_path = self.fix_initial_path_string(output_file_path)
            output_file_path = output_file_path[:-1]
        if output_file_path == "":
            print("There is no given output file.")
            confirm = input("Continue? y/n: ")
            if confirm != "y":
                return
        elif self.confirm_as_absolute_path(output_file_path) is False:
            print("The output file path is invalid.")
            confirm = input("Continue without output file? y/n: ")
            if confirm != "y":
                return

        # Count number of items in directory
        directories = os.scandir(path)
        total_items_in_directory_beginning = 0
        for entry in directories:
            total_items_in_directory_beginning += 1

        # Grab the size of the directory before any processing.
        total_directory_size_beginning = self.get_directory_size(path)

        # Write to output file.
        if output_file_path != "":
            try:
                with open(output_file_path, mode="a", encoding="utf-8") as o:
                    o.write("Looking at files:\n\n")
            except:
                print("Error: Problem with openning output file.")
                print("Output file:" + output_file_path)
                return

        # Build a paired list of dir/file names and their new corrected version
        old_list = []
        new_list = []
        handled_list = []
        parsed_list = []
        runtime_list = []
        filesize_list = []
        old_year_list = []
        new_year_list = []
        is_empty_folder_list = []
        missed_count = 0
        all_file_types_beginning = self.grab_all_filetypes(path)
        directories = os.scandir(path)
        mq = MovieQueries(api_key)
        current_count = 0
        is_empty_folder = None
        for entry in directories:
            current_count += 1
            new_year = "-1"
            runtime, is_empty_folder = self.find_runtime(path, entry)
            filesize = self.get_filesize(path, entry)
            title_list, year = self.find_title_and_year(entry.name)
            print("  Old File: " + entry.name)

            # Query the API
            # - If our file's runtime is valid
            # - Check with english, then without
            if runtime > smallest_run_time:
                success = False
                while success is False:
                    try:
                        new_file_name, new_year = mq.return_new_movie_filename(
                            title_list, year, runtime, True
                        )
                        success = True
                    except requests.exceptions.ReadTimeout:
                        print("  ..")
                        sleep(2)
                    except Exception as inst:
                        if inst is not None:
                            if inst.response.status_code == 401:
                                print("Error: Invalid API Key.")
                                return
                        print(type(inst))
                        print("  ..")
                        sleep(2)
                if new_file_name == "NOT FOUND":
                    success = False
                    while success is False:
                        try:
                            new_file_name, new_year = mq.return_new_movie_filename(
                                title_list, year, runtime, False
                            )
                            success = True
                        except requests.exceptions.ReadTimeout:
                            # print("Error: READTIMEOUT")
                            print("  ..")
                            sleep(2)
                        except Exception as inst:
                            # print(type(inst))
                            print("  ..")
                            sleep(2)
                new_file_name = self.clean_file_name(new_file_name)
            else:
                new_file_name = "NOT FOUND"
            print("       -> : " + new_file_name)

            old_year_list.append(year)
            new_year_list.append(new_year)
            old_list.append(entry.name)
            new_list.append(new_file_name)
            runtime_list.append(runtime)
            filesize_list.append(filesize)
            parsed_list.append(title_list[0])
            is_empty_folder_list.append(is_empty_folder)

            if new_file_name == "NOT FOUND":
                missed_count += 1
                if missed_count > 1:
                    sleep(2)
                    missed_count = 0
            else:
                if output_file_path != "":
                    with open(output_file_path, mode="a", encoding="utf-8") as o:
                        o.write("Old File: " + entry.name + "\n")
                        o.write("     -> : " + new_file_name + "\n")

            if current_count % 10 == 0:
                print(
                    "\n"
                    + "("
                    + str(current_count)
                    + "/"
                    + str(total_items_in_directory_beginning)
                    + ") files looked at."
                    + "\n"
                )

        # Write number of files without new names.
        count = 0
        total_count = 0
        if output_file_path != "":
            with open(output_file_path, mode="a", encoding="utf-8") as o:
                o.write("\n")
                o.write("List of items that weren't confirmed: " + "\n\n")
        directories = os.scandir(path)
        for entry in directories:
            i = old_list.index(entry.name)
            total_count += 1
            if new_list[i] == "NOT FOUND" and runtime_list[i] > 20:
                count += 1
                if output_file_path != "":
                    with open(output_file_path, mode="a", encoding="utf-8") as o:
                        o.write("  Old File: " + old_list[i] + "\n")
        # Write a list of invalid files.
        if output_file_path != "":
            with open(output_file_path, mode="a", encoding="utf-8") as o:
                o.write("\n")
                o.write("List of items that are invalid (to delete): " + "\n\n")
            directories = os.scandir(path)
            for entry in directories:
                i = old_list.index(entry.name)
                if new_list[i] == "NOT FOUND" and runtime_list[i] <= 20:
                    with open(output_file_path, mode="a", encoding="utf-8") as o:
                        o.write("  Old File: " + old_list[i] + "\n")

        # Write to output log file.
        if output_file_path != "":
            with open(output_file_path, mode="a", encoding="utf-8") as o:
                o.write("\n")
                o.write(
                    "("
                    + str(count)
                    + "/"
                    + str(total_count)
                    + ") files without found names.\n"
                )
                o.write("\n")
        print(
            "(" + str(count) + "/" + str(total_count) + ") files without found names.\n"
        )

        if count > 0:
            confirm = input("Manually look for names? y/n: ")
            print("\n")
            if confirm != "y":
                return

            if output_file_path != "":
                with open(output_file_path, mode="a", encoding="utf-8") as o:
                    o.write("User choosing file names: \n\n")

            # Recheck items with new_file_name == "NOT FOUND"
            directories = os.scandir(path)
            for entry in directories:
                i = old_list.index(entry.name)
                if new_list[i] == "NOT FOUND" and runtime_list[i] > smallest_run_time:
                    runtime, _ = self.find_runtime(path, entry)
                    title_list, year = self.find_title_and_year(entry.name)
                    success = False
                    while success is False:
                        try:
                            print("  Old File: " + entry.name)
                            new_file_name = ""

                            new_file_name = mq.return_new_movie_filename_with_user(
                                title_list[0], year, runtime
                            )
                            success = True
                        except requests.exceptions.ReadTimeout:
                            print("  .. connection failure. Try again.")
                            sleep(2)
                        except Exception:
                            print("  .. connection failure. Try again.")
                            sleep(2)
                    new_file_name = self.clean_file_name(new_file_name)
                    new_list[i] = new_file_name
                    print("  New File: " + new_file_name + "\n")
                    if output_file_path != "":
                        with open(output_file_path, mode="a", encoding="utf-8") as o:
                            o.write("  Old File: " + entry.name + "\n")
                            o.write("       -> : " + new_file_name + "\n")

        # Count changed years
        total_changed_years = 0
        for i, item in enumerate(old_year_list):
            if item != new_year_list[i] and new_list[i] != "###":
                total_changed_years += 1

        # Ask to continue before changes are applied.
        print("Files will now be moved and renamed.")
        confirm = input("Continue? y/n: ")
        if confirm != "y":
            return
        if output_file_path != "":
            with open(output_file_path, mode="a", encoding="utf-8") as o:
                o.write("\n")
                o.write("Starting renaming folders and deleting files.\n")
                o.write("..\n")

        # Go through lists, mark duplicates if smaller in filesize
        for i, item in enumerate(new_list):
            if item != "***" and item != "NOT FOUND" and new_list.count(item) > 1:
                duplicates = []
                for j, inner_item in enumerate(new_list):
                    if item == inner_item:
                        duplicates.append([j, filesize_list[j]])
                max_filesize_index = -1
                for d in duplicates:
                    if d[1] > max_filesize_index:
                        max_filesize_index = d[0]
                for e in duplicates:
                    if e[0] != max_filesize_index:
                        new_list[e[0]] = "***"

        # Delete files:
        # - duplicates
        # - manual-deletes
        # - files below run-time threshold
        total_error_count = 0
        total_deleted_bytes = 0
        total_deleted_duplicates = 0
        total_deleted_manually = 0
        total_deleted_small = 0
        total_deleted_corrupt = 0
        total_deleted_empty_folders = 0
        total_deleted_files = 0

        directories = os.scandir(path)
        for entry in directories:
            try:
                old_path = path + entry.name
                # Match initial names to new names.
                i = old_list.index(entry.name)
                entry_bytes = filesize_list[i]
                new = new_list[i]
                # Delete files that are duplicates.
                if new == "***":
                    total_deleted_bytes += entry_bytes
                    total_deleted_duplicates += 1
                    if entry.is_dir():
                        num_files_deleted = self.delete_folder_and_contents(old_path)
                        total_deleted_files += num_files_deleted
                    elif entry.is_file():
                        os.chmod(old_path, 0o666)
                        os.remove(old_path)
                        total_deleted_files += 1
                    continue
                # Delete files manually marked to delete.
                if new == "###":
                    total_deleted_bytes += entry_bytes
                    total_deleted_manually += 1
                    if entry.is_dir():
                        num_files_deleted = self.delete_folder_and_contents(old_path)
                        total_deleted_files += num_files_deleted
                    elif entry.is_file():
                        os.chmod(old_path, 0o666)
                        os.remove(old_path)
                        total_deleted_files += 1
                    continue
                # Delete file below runtime desire.
                if runtime_list[i] < smallest_run_time:
                    if is_empty_folder_list[i] is True:
                        total_deleted_empty_folders += 1
                    elif is_empty_folder_list[i] is False and runtime_list[i] == -1:
                        total_deleted_corrupt += 1
                    else:
                        total_deleted_small += 1

                    total_deleted_bytes += entry_bytes
                    if entry.is_dir():
                        num_files_deleted = self.delete_folder_and_contents(old_path)
                        total_deleted_files += num_files_deleted
                    elif entry.is_file():
                        os.chmod(old_path, 0o666)
                        os.remove(old_path)
                        total_deleted_files += 1
                    continue
            except Exception as inst:
                print("Error with: " + old_path + " - " + str(type(inst)) + "\n")
                with open(output_file_path, mode="a", encoding="utf-8") as o:
                    o.write("Error with: " + old_path + " - " + str(type(inst)) + "\n")
                    total_error_count += 1

        # Rename folders and create folders
        directories = os.scandir(path)
        for entry in directories:
            try:
                # If bumping into a file that has already been renamed/handled, skip. There is guaranteed to be no duplicates in new_list.
                if entry.name in handled_list:
                    continue

                # Match initial names to new names
                i = old_list.index(entry.name)
                new = new_list[i]
                old_path = path + entry.name
                new_path = path + new

                # If the movie was not found in the API call, don't change anything.
                if new == "NOT FOUND":
                    continue
                # If folder exists:
                # - rename it
                # - delete all files but largest
                # - rename that file the same as folder
                if entry.is_dir():
                    os.rename(old_path, new_path)
                    largest_inside_path, _ = self.find_largest_in_folder(new_path + "/")
                    file_type = self.get_filetype(largest_inside_path)
                    os.rename(largest_inside_path, new_path + "/" + new + file_type)
                    num_errors, num_files_deleted = (
                        self.delete_all_but_largest_file_in_folder(new_path + "/")
                    )
                    total_error_count += num_errors
                    total_deleted_files += num_files_deleted
                # If file:
                # - create folder
                # - put it into the folder
                elif entry.is_file():
                    os.mkdir(new_path)
                    file_type = self.get_filetype(old_path)
                    move_path = new_path + "/" + new + file_type
                    os.chmod(old_path, 0o666)
                    os.rename(old_path, move_path)
                # Consider this file "handled".
                handled_list.append(new)
            except Exception as inst:
                print("Error with: " + old_path + " - " + str(type(inst)) + "\n")
                with open(output_file_path, mode="a", encoding="utf-8") as o:
                    o.write("Error with: " + old_path + " - " + str(type(inst)) + "\n")
                    total_error_count += 1

        # Grab the size of the directory after processing.
        total_directory_size_end = self.get_directory_size(path)

        all_file_types_end = self.grab_all_filetypes(path)
        total_deleted_misc = (
            total_deleted_files
            - total_deleted_manually
            - total_deleted_duplicates
            - total_deleted_small
            - total_deleted_corrupt
        )
        # Display to user updates of freed memory
        print("Total Updated Release Years: " + str(total_changed_years))
        print("Total Movies Deleted Corrupt/Unusable: " + str(total_deleted_corrupt))
        print("Total Movies Deleted Small: " + str(total_deleted_small))
        print("Total Movies Deleted Manually: " + str(total_deleted_manually))
        print("Total Movies Deleted Duplicates: " + str(total_deleted_duplicates))
        print("Total Error Count: " + str(total_error_count))
        print("Diff Filetypes Before: " + all_file_types_beginning)
        print("Diff Filetypes After: " + all_file_types_end)
        print("Folder Size Before: " + total_directory_size_beginning)
        print("Folder Size After: " + total_directory_size_end)
        print("Total Deleted Misc Files: " + str(total_deleted_misc))
        print("Total Deleted Empty Folders: " + str(total_deleted_empty_folders))
        if output_file_path != "":
            with open(output_file_path, mode="a", encoding="utf-8") as o:
                o.write("Finished renaming folders and deleting files.\n\n")

                o.write(
                    "Total Updated Release Years: " + str(total_changed_years) + "\n"
                )
                o.write(
                    "Total Movies Deleted Corrupt/Unusable: "
                    + str(total_deleted_corrupt)
                    + "\n"
                )
                o.write(
                    "Total Movies Deleted Manually: "
                    + str(total_deleted_manually)
                    + "\n"
                )
                o.write(
                    "Total Movies Deleted Small: " + str(total_deleted_small) + "\n"
                )
                o.write(
                    "Total Movies Deleted Duplicates: "
                    + str(total_deleted_duplicates)
                    + "\n"
                )
                o.write("Total Error Count: " + str(total_error_count) + "\n")
                o.write("Diff Filetypes Before: " + all_file_types_beginning + "\n")
                o.write("Diff Filetypes After: " + all_file_types_end + "\n")
                o.write("Folder Size Before: " + total_directory_size_beginning + "\n")
                o.write("Folder Size After: " + total_directory_size_end + "\n")
                o.write("Total Deleted Misc Files: " + str(total_deleted_misc) + "\n")
                o.write(
                    "Total Deleted Empty Folders: "
                    + str(total_deleted_empty_folders)
                    + "\n"
                )

    def grab_all_filetypes(self, path: str) -> str:
        """
        Builds a string of all filetypes within a given directory.

        Args:
            `path`: The parent folder to search "C:/user/"
        Returns:
            `return_str`: A string filetypes seen. ".txt .mov .mp4"
        """

        def grab_all_filetypes_recursion(path: str) -> list:
            """
            Return a list of all filetypes within this directory and any lower directories.

            Args:
                `path`: The parent folder to search "C:/user/"
            Returns:
                `filetype_set`: A set of filetypes seen. (".txt", ".mov", ".mp4")
            """
            filetype_list = []
            directories = os.scandir(path)
            for entry in directories:
                # If folder exists, look into that recursively
                if entry.is_dir():
                    found_filetype_list = grab_all_filetypes_recursion(
                        path + entry.name + "/"
                    )
                    for item in found_filetype_list:
                        filetype_list.append(item)
                # If file, grab its filetype for the set
                elif entry.is_file():
                    file_type = self.get_filetype(path + entry.name)
                    filetype_list.append(file_type)
                filetype_list = list(set(filetype_list))

            filetype_set = list(set(filetype_list))
            return filetype_set

        filetype_set = grab_all_filetypes_recursion(path)
        return_str = ""
        for item in filetype_set:
            return_str += item + " "
        return_str = return_str.strip()
        return return_str

    def find_largest_in_folder(self, path: str) -> list[str, str]:
        """
        Return the path string of the largest file within a directory.

        Args:
            `path`: The parent folder to search "C:/user/"
        Returns:
            `largest_file`: The largest filepath. "C:/user/movies/matrix.mp4"
            `largest_file_name`: The largest file name. "matrix.mp4"
        """

        largest_path = ""
        largest_file_size = 0
        largest_file_name = ""

        directories = os.scandir(path)
        for entry in directories:
            temp_largest_path = ""
            temp_largest_size = 0
            temp_largest_file_name = ""
            # If folder:
            # - look inside for largest
            if entry.is_dir():
                temp_largest_path, temp_largest_file_name = self.find_largest_in_folder(
                    path + entry.name + "/"
                )
                # If nothing in a folder
                if temp_largest_path != "":
                    temp_largest_size = os.path.getsize(temp_largest_path)
            # If file:
            # - look at size
            elif entry.is_file():
                temp_largest_size = os.path.getsize(path + entry.name)
                temp_largest_file_name = entry.name
                temp_largest_path = path + entry.name

            # Check if largest
            if temp_largest_size > largest_file_size:
                largest_path = temp_largest_path
                largest_file_size = temp_largest_size
                largest_file_name = temp_largest_file_name

        return [largest_path, largest_file_name]

    def remove_items_from_folder(self, path: str) -> int:
        """
        Removes all files and folders within a directory.

        Args:
            `path`: The directory to remove.
        Returns:
            `num_deleted`: Number of files deleted in folder.
        """
        num_deleted = 0
        directories = os.scandir(path)
        for entry in directories:
            num_inside = 0
            # If folder, remove
            if entry.is_dir():
                num_inside = self.remove_items_from_folder(path + entry.name + "/")
                num_deleted += num_inside
                os.chmod(path + entry.name, 0o666)
                os.rmdir(path + entry.name)
            # If file and not largest, remove
            elif entry.is_file():
                os.chmod(path + entry.name, 0o666)
                os.remove(path + entry.name)
                num_deleted += 1
        return num_deleted

    def delete_folder_and_contents(self, path: str) -> int:
        """
        Deletes all files within this folder and this folder.

        Args:
            `path`: The path to this folder.
        Returns:
            `num_files_deleted`: Number of files deleted inside.
        """
        num_files_deleted = 0
        directories = os.scandir(path + "/")
        for entry in directories:
            if entry.is_dir():
                num_inside = self.remove_items_from_folder(
                    path + "/" + entry.name + "/"
                )
                num_files_deleted += num_inside
                os.chmod(path + "/" + entry.name, 0o666)
                os.rmdir(path + "/" + entry.name)
            elif entry.is_file():
                os.chmod(path + "/" + entry.name, 0o666)
                os.remove(path + "/" + entry.name)
                num_files_deleted += 1
        os.rmdir(path)
        return num_files_deleted

    def delete_all_but_largest_file_in_folder(self, path: str) -> list[int, int]:
        """
        Delete all files and folders within this folder besides the largest file,
        and bring largest to the top.

        Args:
            `path`: The parent folder to search. Ex: "C:/user/"
        """
        num_of_errors = 0
        num_files_deleted = 0

        # Find largest item and bring to top of folder.
        largest_path, largest_name = self.find_largest_in_folder(path)
        os.rename(largest_path, path + largest_name)
        # Delete all items without this name.
        directories = os.scandir(path)
        for entry in directories:
            try:
                # If folder, remove
                if entry.is_dir():
                    num_inside = self.remove_items_from_folder(path + entry.name + "/")
                    num_files_deleted += num_inside
                    os.chmod(path + entry.name, 0o666)
                    os.rmdir(path + entry.name)
                # If file and not largest, remove
                elif entry.is_file() and entry.name != largest_name:
                    os.chmod(path + entry.name, 0o666)
                    os.remove(path + entry.name)
                    num_files_deleted += 1
            except Exception as inst:
                num_of_errors += 1
                print(
                    "Error with: " + path + entry.name + " - " + str(type(inst) + "\n")
                )
        return num_of_errors, num_files_deleted


class MovieQueries:
    """
    Methods for interacting with TheMovieDatabase.com API.
    """

    tmdb.API_KEY = ""
    tmdb.REQUESTS_TIMEOUT = 10

    def __init__(self, given_api_key: str = "") -> None:
        tmdb.API_KEY = given_api_key

    def clean_api_title(self, movie_title: str) -> str:
        """
        Cleans the API returned title to a simpler version for comparison with
        our file's title.

        "Monty Python and the Holy Grail" > "montypythonholygrail"

        Args:
            `movie_title`: The movie title given by the API.
        Returns:
            `new_movie_title`: The new formatted title.
        """
        new_movie_title = str.lower(movie_title)
        remove_list = [
            "(",
            ")",
            "[",
            "]",
            "{",
            "}",
            "&",
            ".",
            ",",
            "-",
            "_",
            "=",
            "~",
            "&",
            ":",
        ]
        for item in remove_list:
            while item in new_movie_title:
                new_movie_title = new_movie_title.replace(item, " ")
        while "  " in new_movie_title:
            new_movie_title = new_movie_title.replace("  ", " ")
        while "'" in new_movie_title:
            new_movie_title = new_movie_title.replace("'", "")
        new_movie_title = new_movie_title.strip()

        forbidden_words = ["and", "the", "part"]
        allowed_single_letters = ["a", "e", "i", "o", "x"]
        # Remove particular words from title
        words = new_movie_title.split(" ")
        if len(words) == 2:
            new_movie_title = words[0] + " " + words[1]
        elif len(words) == 1:
            pass
        else:
            new_movie_title = ""
            for i, w in enumerate(words):
                if w in forbidden_words:
                    continue
                if len(w) == 1 and i != 0:
                    if not (w.isnumeric() or w in allowed_single_letters):
                        continue
                new_movie_title += w + " "
            new_movie_title = new_movie_title.strip()
        while " " in new_movie_title:
            new_movie_title = new_movie_title.replace(" ", "")
        return new_movie_title

    def return_movie_runtime(self, movie_id: int) -> int:
        """
        Query the API for the runtime of the movie with this ID.

        Args:
            `movie_id`: The ID of the movie. This is found by a first query to
                the API.
        Returns:
            `runtime`: Movie run time in minutes.
        """
        movie = tmdb.Movies(movie_id)
        movie.info()
        runtime = int(movie.runtime)
        return runtime

    def get_percent_word_match(self, api_title: str, our_title: str) -> float:
        """
        Return a percent of words in our title are in the total of the
        API-received title. For consideration of if the API title is a quick
        valid match.

        Ex:
        `api_title` = "the help from the train people" > "help from train people"
        `our_title` = "help from trainspotters" > "help from trainspotters"

        "help" "from" : 2 matches
        4 processed words in `api_title`
        2/4 == 50% match

        Args:
            `api_title`: The title received from the DB API.
            `out_title`: The title parsed from the found file.
        Returns:
            `match_percent`: A percentage of the matched words.
        """
        new_api_title = str.lower(api_title)
        new_our_title = str.lower(our_title)
        remove_list = [
            "(",
            ")",
            "[",
            "]",
            "{",
            "}",
            "&",
            ".",
            ",",
            "-",
            "_",
            "=",
            "~",
            ":",
        ]
        for item in remove_list:
            while item in new_api_title:
                new_api_title = new_api_title.replace(item, " ")
        while "  " in new_api_title:
            new_api_title = new_api_title.replace("  ", " ")
        while "'" in new_api_title:
            new_api_title = new_api_title.replace("'", "")
        new_api_title = new_api_title.strip()
        new_our_title = new_our_title.strip()

        # Remove particular words from title
        forbidden_words = ["and", "the", "part", "of"]
        allowed_single_letters = ["a", "e", "i", "o", "x"]
        w_api_title = new_api_title.split(" ")
        w_our_title = new_our_title.split(" ")
        w_after_api_title = []
        w_after_our_title = []
        for i, w in enumerate(w_api_title):
            if w in forbidden_words:
                continue
            if len(w) == 1 and i != 0:
                if not (w.isnumeric() or w in allowed_single_letters):
                    continue
            w_after_api_title.append(w)
        for i, w in enumerate(w_our_title):
            if w in forbidden_words:
                continue
            if len(w) == 1 and i != 0:
                if not (w.isnumeric() or w in allowed_single_letters):
                    continue
            w_after_our_title.append(w)

        # See how many of our title's words are in the API-returned title
        our_words_in_api_title_count = 0
        for i, w in enumerate(w_after_our_title):
            if w in w_after_api_title:
                our_words_in_api_title_count += 1
        match_percent = our_words_in_api_title_count / len(w_after_api_title)

        return match_percent

    def return_new_movie_filename(
        self, title_list: list[str], year: str, runtime: str, with_english: bool
    ) -> list[str, str]:
        """
        Given a loose title and year, returns a formatted dir/file name by
        calling for a search on The Movie Database API.

        WITHOUT GUIDANCE FROM USER.

        Args:
            `title_list`: A loosely correct string of the title of a movie, and
                first half and last half of the title.
            `year`: A loosely correct string of the year of the movie.
            `runtime`: The found runtime of the movie file.
            `with_english`: If we want to limit the search to English.
        Returns:
            `new_file`: The new formatted filename. Returns "NOT FOUND" if
            couldn't find a correct movie.
            `new_year`: The API found release year. Returns "-1" if title not found.
        Example:
            `title_list`: ["the matrix","the","matrix"]
            `year`: "1999"
            `new_file`: "The Matrix (1999)"
        """
        runtime = int(runtime)
        search = tmdb.Search()
        new_file = "NOT FOUND"
        # Needed match between titles for auto-choose, in situation of one item
        # after removing possibilities.
        needed_match_percent = 0.5

        for title in title_list:
            # If any time-out from the API, skip this file.
            if year == "-1":
                search.movie(query=title)
            else:
                search.movie(query=title, year=year)
            potential_new_file_list = []
            # Find movies with this title (and year)
            for s in search.results:
                success = False
                broken = False
                while success is False and broken is False:
                    try:
                        runtime_api = self.return_movie_runtime(s["id"])
                        potential_new_file_list.append(
                            {
                                "title": s["title"],
                                "vote_count": s["vote_count"],
                                "runtime": runtime_api,
                                "year": s["release_date"][:4],
                                "lang": s["original_language"],
                            }
                        )
                        success = True
                    except requests.exceptions.ReadTimeout:
                        print("  ..")
                        sleep(2)
                    except Exception as inst:
                        if inst is not None:
                            if inst.response.status_code == 404:
                                print("Error: Couldn't find an ID. At: " + s["title"])
                                broken = True
            # Compare these items against the runtime to shrink list.
            # - A case of a extended edition movie might not be caught here
            # - Look for exact title match
            if len(potential_new_file_list) > 1:
                for i, item in enumerate(potential_new_file_list):
                    if (
                        self.clean_api_title(item["title"])
                        == self.clean_api_title(title)
                        and item["year"] == year
                    ):
                        new_file = item["title"] + " (" + item["year"] + ")"
                        return new_file, item["year"]
                    if item["runtime"] > runtime + 10 or item["runtime"] < runtime - 10:
                        potential_new_file_list[i] = "del"
                    elif item["lang"] != "en" and with_english:
                        potential_new_file_list[i] = "del"
                    elif item["vote_count"] < 20:
                        potential_new_file_list[i] = "del"
                while "del" in potential_new_file_list:
                    potential_new_file_list.remove("del")
            # If one case, return
            # Else, save for later with user input
            if (
                len(potential_new_file_list) == 1
                and self.get_percent_word_match(
                    potential_new_file_list[0]["title"], title
                )
                > needed_match_percent
            ):
                new_file = (
                    potential_new_file_list[0]["title"]
                    + " ("
                    + potential_new_file_list[0]["year"]
                    + ")"
                )
                return new_file, potential_new_file_list[0]["year"]
            else:
                new_file = "NOT FOUND"
                new_year = "-1"

            # Try searching WITHOUT a year input, if previously searched
            # with year.
            if year != "-1":
                search.movie(query=title)
                potential_new_file_list = []
                for s in search.results:
                    runtime_api = self.return_movie_runtime(s["id"])
                    potential_new_file_list.append(
                        {
                            "title": s["title"],
                            "vote_count": s["vote_count"],
                            "runtime": runtime_api,
                            "year": s["release_date"][:4],
                            "lang": s["original_language"],
                        }
                    )
                # Compare these items against the runtime to shrink list.
                for i, item in enumerate(potential_new_file_list):
                    if (
                        self.clean_api_title(item["title"])
                        == self.clean_api_title(title)
                        and item["runtime"] < runtime + 10
                        and item["runtime"] > runtime - 10
                        and item["vote_count"] > 20
                    ):
                        new_file = item["title"] + " (" + item["year"] + ")"
                        return new_file, item["year"]
                    if item["runtime"] > runtime + 10 or item["runtime"] < runtime - 10:
                        potential_new_file_list[i] = "del"
                    elif item["lang"] != "en" and with_english:
                        potential_new_file_list[i] = "del"
                    elif item["vote_count"] < 20:
                        potential_new_file_list[i] = "del"
                while "del" in potential_new_file_list:
                    potential_new_file_list.remove("del")
                if (
                    len(potential_new_file_list) == 1
                    and self.get_percent_word_match(
                        potential_new_file_list[0]["title"], title
                    )
                    > needed_match_percent
                ):
                    new_file = (
                        potential_new_file_list[0]["title"]
                        + " ("
                        + potential_new_file_list[0]["year"]
                        + ")"
                    )
                    return new_file, potential_new_file_list[0]["year"]

            # Try searching without the runtime shrink, with year
            if year == "-1":
                continue
            else:
                search.movie(query=title, year=year)
                potential_new_file_list = []
                for s in search.results:
                    potential_new_file_list.append(
                        {
                            "title": s["title"],
                            "vote_count": s["vote_count"],
                            "lang": s["original_language"],
                            "year": s["release_date"][:4],
                        }
                    )
                for i, item in enumerate(potential_new_file_list):
                    if item["lang"] != "en" and with_english:
                        potential_new_file_list[i] = "del"
                    elif item["vote_count"] < 20:
                        potential_new_file_list[i] = "del"
                while "del" in potential_new_file_list:
                    potential_new_file_list.remove("del")
                if (
                    len(potential_new_file_list) == 1
                    and self.get_percent_word_match(
                        potential_new_file_list[0]["title"], title
                    )
                    > needed_match_percent
                ):
                    new_file = (
                        potential_new_file_list[0]["title"]
                        + " ("
                        + potential_new_file_list[0]["year"]
                        + ")"
                    )
                    return new_file, potential_new_file_list[0]["year"]
            new_file = "NOT FOUND"
            new_year = "-1"
        return new_file, new_year

    def return_new_movie_filename_with_user(self, title: str, year: str, runtime: str):
        """
        Given a loose title and year, returns a formatted dir/file name by
        calling for a search on The Movie Database API.

        Checks for year being incorrect by one year and if more than one movie
        is under this title, will prompt user to confirm which movie.

        Args:
            `title`: A loosely correct string of the title of a movie.
            `year`: A loosely correct string of the year of the movie.
            `runtime`: The found runtime of the movie file.
        Returns:
            `new_file`: The new formatted filename. Returns "NOT FOUND" if
            couldn't find a correct movie.
        Example:
            `title`: "the matrix"
            `year`: "1999"
            `new_file`: "The Matrix (1999)"
        """
        runtime = int(runtime)
        search = tmdb.Search()
        if year == "-1":
            search.movie(query=title)
        else:
            search.movie(query=title, year=year)

        # Default to "NOT FOUND"
        new_file = "NOT FOUND"
        potential_new_file_list = []

        # Find movies with this title (and year)
        for s in search.results:
            runtime_api = self.return_movie_runtime(s["id"])
            potential_new_file_list.append(
                [
                    s["title"],
                    s["id"],
                    s["vote_count"],
                    runtime_api,
                    s["release_date"][:4],
                ]
            )
        # Compare these items against the runtime to shrink list.
        # - A case of a extended edition movie might not be caught here
        # - Look for exact title match
        for i, item in enumerate(potential_new_file_list):
            if item[3] > runtime + 20 or item[3] < runtime - 20:
                potential_new_file_list[i] = "del"
        while "del" in potential_new_file_list:
            potential_new_file_list.remove("del")

        # If any, ask for user help
        if len(potential_new_file_list) > 0:
            print("  ** Our File's Runtime **: " + str(runtime))
            print("  0: ** Skip and Seach Again **")
            for i, element in enumerate(potential_new_file_list):
                print(
                    "  "
                    + str(i + 1)
                    + ": "
                    + str(element[0])
                    + " ("
                    + str(element[4])
                    + ")"
                    + " - Votes: "
                    + str(element[2])
                    + " - Runtime: "
                    + str(element[3])
                    + "m"
                )
            choice = str(input("  Enter Number Choice: ")).strip()
            # Allow for skipping this selection
            if (
                choice.isnumeric() is False
                or int(choice) > len(potential_new_file_list)
                or int(choice) < 1
            ):
                pass
            else:
                choice = int(choice)
                new_file = (
                    potential_new_file_list[choice - 1][0]
                    + " ("
                    + potential_new_file_list[choice - 1][4]
                    + ")"
                )
                return new_file
        # If didn't find anything, query again with custom search
        # - "***" to leave file unchanged
        # - "###" to mark file for deletion
        # - "+++" to manually enforce a title and year
        title = ""
        while title != "***":
            print("  Enter '***' to give up.")
            print("  Enter '+++' to manually force a title and year.")
            print("  Enter '###' to force deletion of this file.")
            title = input("  Enter New Title Search: ")
            if title == "***":
                return "NOT FOUND"
            if title == "###":
                return "###"
            if title == "+++":
                title = input("  Enter New Title: ")
                title = title.strip()
                year = input("  Enter New Year: ")
                year = year.strip()
                new_file = title + " (" + year + ")"
                return new_file
            search.movie(query=title)
            potential_new_file_list = []
            for s in search.results:
                runtime_api = self.return_movie_runtime(s["id"])
                potential_new_file_list.append(
                    [
                        s["title"],
                        s["id"],
                        s["vote_count"],
                        runtime_api,
                        s["release_date"][:4],
                    ]
                )
            if len(potential_new_file_list) != 0:
                print("  ** Our File's Runtime **: " + str(runtime) + "\n")
                print("  0: ** Skip and Search Again **")
                for i, element in enumerate(potential_new_file_list):
                    print(
                        "  "
                        + str(i + 1)
                        + ": "
                        + str(element[0])
                        + " ("
                        + str(element[4])
                        + ")"
                        + " - Votes: "
                        + str(element[2])
                        + " - Runtime: "
                        + str(element[3])
                        + "m"
                    )
                print(" ")
                choice = str(input("  Enter Number Choice: ")).strip()
                # Allow for searching again.
                if (
                    choice.isnumeric() is False
                    or int(choice) > len(potential_new_file_list)
                    or int(choice) < 1
                ):
                    pass
                else:
                    choice = int(choice)
                    new_file = (
                        potential_new_file_list[choice - 1][0]
                        + " ("
                        + potential_new_file_list[choice - 1][4]
                        + ")"
                    )
                    return new_file
            else:
                print("  - No results found.\n")
        return new_file


if __name__ == "__main__":
    main()
