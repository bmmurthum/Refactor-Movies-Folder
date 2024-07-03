# Refactoring a Directory of Movies

**Contents:**

- [Important Notes](https://github.com/bmmurthum/Refactor-Movies-Folder/tree/main?tab=readme-ov-file#important-notes)
- [Requirements](https://github.com/bmmurthum/Refactor-Movies-Folder/tree/main?tab=readme-ov-file#requirements)
- [Example](https://github.com/bmmurthum/Refactor-Movies-Folder/tree/main?tab=readme-ov-file#example)
- [Overview](https://github.com/bmmurthum/Refactor-Movies-Folder/tree/main?tab=readme-ov-file#overview)
- [Tests](https://github.com/bmmurthum/Refactor-Movies-Folder/tree/main?tab=readme-ov-file#tests)
  - [Unit Testing](https://github.com/bmmurthum/Refactor-Movies-Folder/tree/main?tab=readme-ov-file#unit-testing)
  - [Code Coverage](https://github.com/bmmurthum/Refactor-Movies-Folder/tree/main?tab=readme-ov-file#code-coverage)
- [Reflections](https://github.com/bmmurthum/Refactor-Movies-Folder/tree/main?tab=readme-ov-file#reflections)
- [Work Log](https://github.com/bmmurthum/Refactor-Movies-Folder/tree/main?tab=readme-ov-file#work-log)

**Description:**

With a directory full of movies, this script cleans up the title names and removes unneeded files. It attempts to do it automatically, if unsure, leaves item for user guidance at end of search.

```PowerShell
py refactor_movie_folder.py
```

The script handles the following:

- Finds and adds year, if none.
- Replaces with correct year, if incorrect.
- Removes duplicates of movies, keeping the larger file sized.
- Removes corrupt files and otherwise unwatchable.
- Removes any misc files: images, subtitle text, README.txt.

With user guidance, allows for:

- Deletion of titles without found titles.
- Manual choice of file title and year.
- Leaving file as is.

After file manipulation, displays:

- Total updated release-years.
- Total freed memory.
- Total deleted corrupt/unusable movies.
- Total manually deleted.
- Total deleted duplicates.
- Total errors in file handling.

Records changes to an output log file, for oversight:

- Total directory size on disk, before and after.
- Total # of updated release-years.
- Total # of deleted corrupt/unusable movies.
- Total # of manually deleted.
- Total # of duplicates deleted.
- Total # of misc files deleted.
- Total # of empty folders deleted.
- Total # of errors in file handling.
- Different filetypes before & after

## Important Notes

I encourage running this on a sample selection before full use. I take no responsibility for accidentally lost files. This should only be used with movies, in a structure of directories as sampled below. **Use at your own risk.**

- It will remove all files, except for movies (largest files) within the selected directory.
- The selected directory must be initially set up such that each folder inside contains a single movie, and any amount of movie files are outside a containing folder.
- I found it to have **0 false-positives** of incorrectly naming movies, pushing for more user interaction when it is unsure of the correct title. The possibility still exists. The recorded output of changes-made, allows for looking over this, after the changes.
- I found it to have a **97% success rate** of finding correct titles automatically, without user input.

## Requirements

- You'll need to register with the [The Movie Database](https://www.themoviedb.org/settings/api) for an API key to enter into our `refactor_movie_folder.py`.
  - Replace `api_key = "___"` with your key. **Line 48**.
- Write in an absolute path to an output log file, if desired.
  - Replace `output_file_path = "___"` with a path to a text file. **Line 43**.
- Install necessary Python packages.

There's some possibility that you need to install packages with a terminal with admin privileges, and it's important that you're applying the installs to the same version of Python that you're running, if you have multiple.

A API-wrapper by [Celiao](https://github.com/celiao/tmdbsimple) for interacting with the [https://www.themoviedb.org/](https://www.themoviedb.org/) database API.

```text
pip install tmdbsimple
```

For reading movie run-times of our files. Can be found at [https://pypi.org/](https://pypi.org/project/opencv-python/).

```text
pip install opencv-python
```

For identifying the movie release year of our files.

```text
pip install regex
```

For handling timeout-errors in connecting with the API.

```text
pip install requests
```

## Example

Running the program shows something like this.

```text
C:\Users\Bob>py refactor_movie_folder.py 
Enter Directory Path: C:/Movies/
Directory: C:/Movies/
 - Aliens.Vs.Predator.Requiem.2007.1080p.BluRay.H264
 - Blade.Runner.2049.2017.720p.BluRay.x264
 - Rango [2009] [720]
 - Roma (2018) [1080p] [BluRay] [5.1]
 - Roma.2018.REPACK.720p.NF.ws.mkv
 - ...
This is the selected directory.
Continue? y/n:
```

`Beginning file structure` :

```text
C:/Movies/
  Aliens.Vs.Predator.Requiem.2007.1080p.BluRay.H264/
    Aliens.Vs.Predator.Requiem.2007.1080p.BluRay.H264.mp4
    README.txt
    /SUBS/
      English.srt
      Spanish.srt
  Blade.Runner.2049.2017.720p.BluRay.x264/
    Blade.Runner.2049.2017.720p.BluRay.x264.avi
    misc.txt
    sample.mp4
  Rango [2009] [720]
    Rango [2009] [720].avi
    Rango [2009] [720] Spanish.srt
  Roma (2018) [1080p] [BluRay] [5.1]/
    Roma (2018) [1080p] [BluRay] [5.1].mp4
  Roma.2018.REPACK.720p.NF.ws.mkv
  Sleepless in Seattle DIRECTORS CUT.mkv
  The Lego Movie (2014) [1080p].mp4
```

`Final file structure` :

```text
C:/Movies/
  Aliens v Predator Requiem (2007)/
    Aliens v Predator Requiem (2007).mp4
  Blade Runner 2049 (2017)/
    Blade Runner 2049 (2017).avi
  Rango (2011)/
    Rango (2011).avi
  Roma (2018)/
    Roma (2018).mp4
  Sleepless in Seattle (1993)/
    Sleepless in Seattle (1993).mkv
  The Lego Movie (2014)/
    The Lego Movie (2014).mp4
```

`Output log file` :

```text
...
Finished renaming folders and deleting files.

Total Updated Release Years: 9
Total Movies Deleted Corrupt/Unusable: 1
Total Movies Deleted Manually: 2
Total Movies Deleted Small: 5
Total Movies Deleted Duplicates: 1
Total Error Count: 0
Diff Filetypes Before: .srt .mp4 .nfo .mp3 .txt .wmv .mkv .jpg .mpg
Diff Filetypes After: .srt .mp4 .mkv .jpg
Folder Size Before: 27.78GB
Folder Size After: 24.35GB
Total Deleted Misc Files: 44
Total Deleted Empty Folders: 1
```

## Overview

When we run the program, it goes in the following order, with pauses for confirmation of continuing.

1. Asks for a path to the directory that contains the files/folders of movies.
2. Looks at all the files, building an internal list of our files and correct titles.
    - Parses our file names for title and year.
    - Reads our file's run-time for better search.
    - Calls on API of [https://www.themoviedb.org/](https://www.themoviedb.org/) for better title name.
3. For any titles with less confidence, it then asks us for our input on choosing a title from a selection.
4. Then it deletes and renames files, creating folders for movies without folders.

It creates an output log file while in process to help in the case of errors in renaming.

## Tests

### Unit Testing

We implemented unit-tests for my methods unrelated to file-manipulation. We designed them for code-coverage and range of possibilities.

```PowerShell
py -m unittest
```

`clean_api_title(movie_title: str) -> str` :

- Returns a simplified version of the API-returned title to compare with our file's title. If it matches perfectly, along with run-time match, and year match, we can confirm this is a correct match immediately.
- We tested this with the following:
  - Removing special characters and particular single letters.
  - Removing "and", "the" general words, if title is long enough to consider.
  - Keeping numbers.
  - On case of title being one or two words, keeping all words.

`clean_file_name(title_file_name: str) -> str` :

- Returns a string, a new file name, that is clean of any characters that are disallowed in Window's files. This is used after confirmation.
- We tested this with the following:
  - Remove `":"`, `"?"`.
  - Removing nothing.

`confirm_as_absolute_path(path: str) -> bool` :

- This checks a given path by the user to be an absolute path. With the output log file and the initial directory path being important to the process, this is checked early, and important. This is called in conjunction with `fix_initial_path_string()` to have it formatted before reaching this.
- We tested this with the following:
  - Valid case, with and without ending forward slash `"/"`
  - Valid case, with different drive letters.
  - Invalid case, with any backslashes `"\"`
  - Invalid case, using any double periods in relative path format `".."`
  - Invalid case, bad drive labelling with a number.
  - Invalid case, Linux formatting.
  - Invalid case, bad input with `"D:users"` not having a `"/"`
  - Invalid case, including Windows banned characters for file paths.

`find_title_and_year(filename: str) -> tuple[str,str]` :

- This method looks at a single string of a given file name to parse out a potential title and year. We use regular-expressions and some logic to grab the year, and figure that everything before the year is title material. This can return incorrect titles if a year is in the title, or the file doesn't have a year, which is unavoidable.
- The later splitting of this title into halves to search with either half accounts for this false-title issue. Any odd titles returned from the API call will be confirmed with the `get_percent_word_match` to catch odd API returns.
- We tested this with the following:
  - Longer filename that would return split titles.
  - Single word title & two word title.
  - A filename that would remove title characters before returning the title to search.
  - File name that would mistake a year in the title as the year of release.
  - File name with year in title that also has release year.
  - File name with additional info that gets caught in the title, to be handled with split title.
  - File name with a title name with misc words to be removed.
  - File name with no year found.
  - Title name with apostrophe to be removed.
  - Title name with a single letter to be removed.

`fix_initial_path_string(path: str) -> str` :

- This method looks at a given Windows formatted path and modifies it to a more comfortable format to work with. Replacing backslashes and affirming an ending forward-slash.
- We tested this with the following:
  - A simple common Windows path `"C:\\\\Movies".
  - A longer case.
  - A path that is already formatted the way we want.
  - A path without ending forward slash `"/"`.
  - A path with a mix of back and forward slashes.

`get_filetype(path: str) -> str` :

- This method grabs the file's type to later append, when moving a file. We also use it to check over removed file types as confirmation to user.
- This could be used in another pattern to specifically remove particular types, targeting video formats uniquely.
- We tested this with the following:
  - A file with periods in its filename.
  - A file with spaces between words.
  - A filetype that is 4 characters long.
  - A filetype that is 5 characters long.
  - A file without a filetype.
  - A file listed deeper within a directory.

`get_percent_word_match(api_title: str, our_title: str) -> float` :

- This method formats both titles to simpler words and characters, then counts how many words of our file's title are in the API-returned title to get a percentage of matched words to total words in API title.
- If this percentage is high enough, we can suggest that this title is a match. In our logic, we auto-confirm if after removing other search possibilities, one title remains and this title matches this method's percentage with 50% or higher.
- We tested this on the following:
  - A matching title and filename, in which the API-returned title needs to be simply formatted to find 100% match.
  - A "making of" title in which the initial movie would give a 83% match.
  - An API-returned title being a much longer title than the file gives, returning a low not-passing 20% match.
  - A file-title that could be the match to an API-returned title, but the 20% match suggests it is not.
  - Various exercises of the simplifying process.

`return_new_movie_filename(title_list, year, runtime, with_english) -> list[str,str]` :

- This method takes a collection of title, year, found file runtime, and a choice in filtering to English, and returns a new file name formatted with the API-returned title and a year. Returns: `["Blade Runner 2049 (2017)", "2017"]`. If it cannot have confidence in a single title with its filtering, it returns `["NOT FOUND","-1"]`.
- It also accepts a list of three titles, to search each for a successful auto-confirmation.
- We tested this with the following:
  - Two word title with a given year.
  - Six word title, that is split, with first half that would give a successful search.
  - Title with no year.
  - Title with year in title that got mistaken as release year.
  - Title with misspelling and correct year.
  - Title without year, that requires searching a second search without english to confirm.

`return_movie_runtime(movie_id: int) -> int` :

- This grabs a known movie's runtime from the API to have it be compared with our currently looked at movie's runtime. This works inside of `return_new_movie_filename()`, which has grabbed the movie's ID from the DB API.
- These returns are entirely on the responsibility of the API.
- We tested this with the following:
  - Monty Python and the Holy Grail `id = 762`
  - The Matrix `id = 603`
  - The Incredibles `id = 9806`

### Code Coverage

We received 99% code coverage by running over the following cases, using the `coverage.py` tool:

Our last 1% is in lines that I couldn't get `coverage.py` to exclude, which I would have to change a line in the code to test `output_file_path = "___"` being different.

- Unit tests
- Larger set of files
- Smaller set of files
- User gives a non-absolute-path to search
- User searches again, after manually typing search title
- Manual forcing of a title
- Manual deletion of a file & file in folder
- Keeping a file as is, "give up" in search.
- Enter valid choice on first search-title menu pop
- Enter "0" on second search-title menu pop after disregarding the first.

```PowerShell
> coverage run -m unittest
> coverage run refactor_movie_folder.py
> coverage combine -a
> coverage html
> coverage report
> coverage report --format=markdown > test.md

Name                                Stmts   Miss  Cover   Missing
-----------------------------------------------------------------
refactor_movie_folder.py              739      2    99%   454-455
test_clean_api_title.py                49      0   100%
test_clean_file_name.py                25      0   100%
test_confirm_as_absolute_path.py       67      0   100%
test_find_title_and_year.py            61      0   100%
test_fix_intial_path_string.py         37      0   100%
test_get_filetype.py                   37      0   100%
test_get_percent_word_match.py         56      0   100%
test_return_movie_runtime.py           44      0   100%
test_return_new_movie_filename.py     109      0   100%
-----------------------------------------------------------------
TOTAL                                1224      2    99%
```

## Reflections

**Avoiding False Positives:**

Hunting for false-positives in renaming files to wrong titles was a high-priority. I considered ways of having high-confidence in API-returned titles being the correct title, to minimize user involvement.

We use a mix of (1) boiling down filename title to basic parts, removing odd characters to allow for a broader search, to then be boiled down with consideration of runtime and release-year, (2) breaking filename title into halves to search with each half, in the case of odd formatted titles of a franchise, (3) searching with a priority of english-language releases first allows for a quicker boiling down, (4) confirming similar words in API-returned title and our filename title to confirm a single case after a boiling down over runtime.

There are some cases where user involvement feels necessary.

- "Making of ..." titles often are released the same year, with same title words and runtime.
- Titles with one or two words end up giving large search results, that can be hard to boil down.
- Titles with alternate titles can be hard to confirm.
- Titles with 1/2 as a character, or superscript, not returning from initial query.
- Titles with "III" as 3, not being recognized.
- Movies with a large franchise that have similar run-times and titles.
- Some movies are unregistered with the database that we're calling on.

**Considerations of Libraries:**

The used `openvc-python` library feels loosely used, and throws some errors on odd files. The run-time of a movie file is written to only add efficiency in auto-selection, and ultimately doesn't destroy function. This library may be deprecated. It could be that newer file types and encodings are less than supported.

My use of `requests` is, most importantly, to target the issue of when program loses network connection with the API calls midway through an important search, to pause before starting that call over again. If the API decides to throw another sort of error, we also pause. On a false API key, we catch this and terminate the program. On a file-permissions issue, in deleting or renaming, we note this and continue on. There's room to add more detail for unique responses being handled differently.

`tmdbsimple` is an API wrapper. Nice documentation and tests. [https://github.com/celiao/tmdbsimple](https://github.com/celiao/tmdbsimple)

The `os.scandir(path)` seems to have more utility that I've exercised. The item in it's return iterable has values to access that return its path, among other things. I could have used this differently if I noticed earlier.

**Using Coverage.py:**

I used the [coverage.py](https://coverage.readthedocs.io/en/7.5.4/index.html) tool over multiple cases to ensure exercise of different situations and combined them for a more complete coverage view. Considerations on what to exclude in coverage percent is a fuzzy situation. Excluding error-catch blocks that often don't get thrown in runtime, like the "lost connection to API" call, feels acceptable. Some other cases feel like they could be included.

I could do a development of quality-assurance, of programmatically creating situations for the program to run over to generate coverage tests.

I had some trouble in running coverage tests from different directories and combining them. The documentation suggests that where the `.coverage` was generated from has some binding to its current relative paths. So we started to try with all the unittests in the general development space, instead of within a separate directory. This worked better.

**Further On:**

If was to add more to this, it'd be:

1. Refactoring and compartmentalization of methods.
2. Consideration of reading file's resolution for noting that information.
3. Keeping a track on number of calls to API per second to write a limiter on that, beyond slowing down when induced to slow down.
4. More attention to catching user-error and ease of use.

I'd like to see what unit-testing/coverage practices are for methods that call on file manipulation. Are we to create a group of files/directories and then call our methods on them manually? Is that reasonable in this case of problem?

## Work Log

6/28 12pm: 93% auto-found. 8 false-positives.

  - if initial title is two words, don't remove "the"
  - If file runtime is less than 10min, remove file/directory later
    - Currently "NOT FOUND", without API query
  - Looking at "NOT FOUND" better
  - Removes invalid choices by vote count < 20
  - After main pass, look without english filter
  - Fixed first-half last-half
  - Fixed false-positives

6/28 2pm: 99.9% auto-found. 3+ False Positives.

  - Catch connection time-out error to try again.
  - Doesn't add small/corrupt files to our NOTFOUND count.

6/28 7pm: 99.9% auto-found.

  - Deletes duplicates and corrupt files
  - Counts deleted memory and files
  - Tests against names better

6/29 11am: 99.9% auto-found. 4 false-positives.

  - Fixed an error in deleting, permissions issue
  - Reports count of deleted empty folders
  - Reports count of errors, duplicates
  - List of items not confirmed, shouldn't include low-runtime

6/29 2pm: 99.9% auto-found. 4 false-positives.
  - Allow for folder's with read-only to be deleted.
    - "Leon the professional"
    - "Avengers Endgame"
    - "U.S vs John Lennon"
    - "Transformers Revenge of the Fallen"
  - At least 50% of the words have to be in the new title to auto-choose.
  - More allowance of choice
  - Allow for custom typed in name
  
6/30 7am: 97% auto-found. 0 false-positives.

  - Count corrected release year, added release year
  - Count files at beginning to show current count done.
  - Have try-except on user-choice be wider, to try again if connection fail.
  - Auto-generate list, before user-search
  - Changed print() formatting
  - Allow for user to choose to delete a missing search

6/30 9am: 97% auto-found. 0 false-positives.

  - Fixing choice option
  - Writing unit-tests.
  - Writing README.md.
  - Program all in one file.
  - Looked into "Enter Number Choice:" Case 0 not behaving
  - Fixed issue with `entry` renaming throwing errors.
  - Show list of filetypes, before and after.
  - Look at directory memory size, before and after for change.
  - Total deleted misc files
  - Directories that are already correct format, doesn't rename internal file
  - Running unit-tests.
  
7/1 11am: Code Coverage 83%, Unit-Tests 100%.

  - With unit-tests and small sample 83% total.
  - With unit-tests and large sample 98% total.
  - Perfect match in search, when looking at searching without runtime-shrink. Won't happen because it would've already bumped into it.
  - Add print-language for not-choosing a given title from a list. "Choose 0 to try again"
  - Fix filetype mass of string.
  - Missing case of user giving a non-valid output file?
    - To ignore in coverage.
  - Write descriptions for unit-tests.
  - Fixed count of deleted small files.
  - Fixed count of deleted empty folders.
  - Fixed count of deleted corrupt.

7/2 4pm: Code Coverage 99%, Unit-Tests 100%.

  - Coverage Run:
      1. Unit Tests
      2. Smaller directory
      3. Entering non-valid directory path
      4. Searching again, after manually typing title
      5. Manually force a title
      6. "Give up," keep a file as is
      7. Large directory
      8. Manually deleting a title
      9. Manually delete a file not in folder
      10. Enter choice on first menu
      11. Enter 0 on second menu
  - Checking on delete_if_empty_folder() not needed.
  - Checking on rename_file_inside() not needed.
  - Testing coverage.py working better if all in one directory, without changing where the .coverage file is.
  - A new handle for error of looking-for-runtime on ID that isn't valid.
