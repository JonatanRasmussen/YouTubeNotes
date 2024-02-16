import shutil
import os
import sqlite3
from datetime import datetime

from global_config import (
    GLOBALLY_CONFIGURED_FILEPATH,
    FILE_CONTAINING_BROWSING_HISTORY_DIRECTORY,
)
from utils import (
    construct_full_file_path_for_browsing_history_copy,
    read_lines_from_file,
    read_single_line_from_file,
    initialize_directory,
)


def file_containing_browsing_history_directory_exists_and_isnt_empty() -> bool:
    chrome_history_directory = read_lines_from_file(FILE_CONTAINING_BROWSING_HISTORY_DIRECTORY)
    if len(chrome_history_directory) != 0:
        return True
    # If file is missing or is empty, alert user and create an empty placeholder file
    print(f"Error: The file {FILE_CONTAINING_BROWSING_HISTORY_DIRECTORY} did not exist!")
    print(f"       An empty file {FILE_CONTAINING_BROWSING_HISTORY_DIRECTORY} has been generated for you.")
    print(f"       Open {FILE_CONTAINING_BROWSING_HISTORY_DIRECTORY} and insert the path to your browsing history.")
    print("       It is something like \\User\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\History")
    with open(FILE_CONTAINING_BROWSING_HISTORY_DIRECTORY, 'w', encoding='utf-8') as file:
        file.write("")
    return False


def attempt_to_make_copy_of_browsing_history() -> bool:
    """ Makes a copy of the browsing history. This is because the original browsing
        history file is 'locked' (cannot be opened) while google chrome is running """
    if file_containing_browsing_history_directory_exists_and_isnt_empty():
        chrome_history_directory = read_single_line_from_file(FILE_CONTAINING_BROWSING_HISTORY_DIRECTORY)
        copy_of_browsing_history = construct_full_file_path_for_browsing_history_copy()
        shutil.copy(chrome_history_directory, copy_of_browsing_history)
        return True
    print(f"The file {FILE_CONTAINING_BROWSING_HISTORY_DIRECTORY} is empty.")
    return False


def query_browsing_history_db_for_latest_video() -> list[str]:
    """ Opens a copy of your browsing history (which is a sql database) and
        queries it for the url, title and watch date of most recent YouTube-video """
    boolean_copying_was_successful = attempt_to_make_copy_of_browsing_history()
    if boolean_copying_was_successful:
        copy_of_browsing_history = construct_full_file_path_for_browsing_history_copy()
        conn = sqlite3.connect(copy_of_browsing_history) # Connect to browsing history db
        cursor = conn.cursor()
        query = """
            SELECT urls.url, urls.title
            FROM urls
            INNER JOIN visits ON urls.id = visits.url
            WHERE urls.url LIKE 'https://www.youtube.com/watch?v=%'
            ORDER BY visits.visit_time DESC
            LIMIT 100
        """ # Retrieve URL of latest YouTube video (checking the 100 last visited URLs)
        cursor.execute(query) # Execute the query
        result = cursor.fetchone() # Fetch the result
        conn.close() # Close the database connection
        # Print the result
        if result:
            url, title = result
            return [url, title]
        print("No recent YouTube video was found in browsing history.")
    return []


def fetch_latest_url(filepath: str) -> None:
    """ Reads your browsing history and finds your most recently watched YouTube video """
    latest_video_details = query_browsing_history_db_for_latest_video()
    if len(latest_video_details) == 0:
        print("error")
    else:
        print("URL:", latest_video_details[0])
        print("Title:", latest_video_details[1])


if __name__ == "__main__":
    initialize_directory()
    my_filepath = GLOBALLY_CONFIGURED_FILEPATH
    fetch_latest_url(my_filepath)