# This file is utils.py
import os
import re

from configs import (
    FILENAME_COPY_OF_BROWSING_HISTORY,
    FILENAME_VIDEOS,
    FOLDERNAME_TRANSCRIPTS,
    FOLDERNAME_AI_SUMMARIES,
    FOLDERNAME_NOTES,
    TOPLEVEL_FOLDER,
    FILEPATH_MAPPING,
    CURRENTLY_SELECTED_SUBFOLDER,
    FILENAME_START_NOTES,
    FILENAME_START_COLLECTION_OF_NOTES,
)


def construct_video_input_file_destination(filepath: str) -> str:
    return f"{filepath}/{FILENAME_VIDEOS}"


def construct_transcript_output_file_destination(filepath: str, video_id: str) -> str:
    return f"{filepath}/{FOLDERNAME_TRANSCRIPTS}/{video_id}.txt"


def construct_ai_summaries_output_file_destination(filepath: str, video_id: str) -> str:
    return f"{filepath}/{FOLDERNAME_AI_SUMMARIES}/{video_id}.txt"


def construct_final_notes_output_file_destination(filepath: str, video_id: str) -> str:
    file_name_and_extension = construct_final_notes_output_file_name_and_extension(video_id)
    return f"{filepath}/{FOLDERNAME_NOTES}/{file_name_and_extension}"


def construct_final_notes_output_file_name_and_extension(video_id: str) -> str:
    return f"{FILENAME_START_NOTES}{video_id}.md"


def construct_notes_collection_output_file_name_and_extension(my_filepath: str) -> str:
    return f"{FILENAME_START_COLLECTION_OF_NOTES}{my_filepath}.md"


def construct_obsidian_collection_of_notes_full_path(obsidian_notes_fullpath: str, filepath: str) -> str:
    my_filepath = get_filepath_with_toplevel_folder_removed(filepath)
    file_name_and_extension = construct_notes_collection_output_file_name_and_extension(my_filepath)
    return f"{obsidian_notes_fullpath}/{file_name_and_extension}"


def construct_obsidian_notes_full_path(obsidian_notes_fullpath: str, video_id: str) -> str:
    file_name_and_extension = construct_final_notes_output_file_name_and_extension(video_id)
    return f"{obsidian_notes_fullpath}/{file_name_and_extension}"


def construct_full_file_path_for_browsing_history_copy() -> str:
    return construct_full_path(FILENAME_COPY_OF_BROWSING_HISTORY)


def construct_full_path(filepath: str) -> str:
    return os.path.join(os.getcwd(), filepath)


def get_filepath_with_toplevel_folder_removed(filepath: str) -> str:
    return filepath.replace(f"{TOPLEVEL_FOLDER}/", "")


def parse_out_video_id_if_its_in_url_format(video_url_or_id: str):
    """ Get video id from YouTube url. They have this format:
        https://www.youtube.com/watch?v=dQw4w9WgXcQ, alternatively
        https://youtu.be/dQw4w9WgXcQ?si=TP24yLz9nyVTF_nL&t=90 """
    if len(video_url_or_id) == 11: # youtube_url is not a url but a video_id
        return video_url_or_id
    pattern = r"(?:v=|\/)([a-zA-Z0-9_-]{11})(?:&|$)"
    match = re.search(pattern, video_url_or_id)
    if match: # youtube_url has the expected format. We can parse its video_id
        video_id = match.group(1)
        return video_id
    print(f"Error: video url or id {video_url_or_id} could not be parsed!")
    return "" # youtube_url could not be parsed


def create_youtube_url_from_video_id(video_id: str) -> str:
    return f"https://www.youtube.com/watch?v={video_id}"


def contains_identical_videos(lst):
    """ Returns true if two or more videos are identical.
        If not, returns false. Has time complexity of O(n^2) """
    n = len(lst)
    for i in range(n):
        for k in range(i + 1, n):
            video_i = parse_out_video_id_if_its_in_url_format(lst[i])
            video_k = parse_out_video_id_if_its_in_url_format(lst[k])
            if video_i == video_k:
                return True
    return False


def add_line_to_file(filepath: str, new_line_to_be_added: str) -> None:
    with open(filepath, 'a') as file:
        file.write(new_line_to_be_added)


def read_single_line_from_file(file_destination: str) -> str:
    lines = read_lines_from_file(file_destination)
    if len(lines) != 1:
        print(f"Warning: {file_destination} contains more than a single line!")
    return ' '.join(lines)

def read_lines_from_file(file_destination: str) -> list[str]:
    """ Read a file with a youtube_url or video_id
        on each line and return them as a list of strings.
        Please NOTE that empty lines and lines starting with # are ignored
        If two or more videos in the list are identical, print a warning in console """
    lines = []
    try:
        with open(file_destination, 'r', encoding='utf-8') as file:
            for line in file:
                lines.append(line.strip())
    except FileNotFoundError:
        print(f"File destination {file_destination} does not exist!")
    # Check if all elements in the list are empty strings
    if all(element == "" for element in lines):
        return []  # Return an empty list if all elements are empty strings
    else:
        return lines  # Return the list of non-empty strings


def remove_empty_lines_and_comments(lines: list[str]) -> list[str]:
    video_urls_or_ids = []
    for line in lines:
        if len(line.strip()) != 0 and not line.startswith(("#", " ")):
            video_urls_or_ids.append(line)
    return video_urls_or_ids


def convert_incorrect_video_id_formats(video_urls_or_ids: list[str]) -> list[str]:
    video_ids = []
    for video_url_or_id in video_urls_or_ids:
        video_id = parse_out_video_id_if_its_in_url_format(video_url_or_id)
        video_ids.append(video_id)
    return video_ids


def read_video_ids_from_file(file_destination: str) -> list[str]:
    lines = read_lines_from_file(file_destination)
    video_urls_or_ids = remove_empty_lines_and_comments(lines)
    video_ids = convert_incorrect_video_id_formats(video_urls_or_ids)
    return video_ids


def read_video_ids_from_default_file(filepath: str) -> list[str]:
    file_destination = construct_video_input_file_destination(filepath)
    return read_video_ids_from_file(file_destination)


def read_video_ids_from_custom_file(filepath: str, custom_filename: str) -> list[str]:
    file_destination = f"{filepath}/{custom_filename}"
    return read_video_ids_from_file(file_destination)


def write_list_as_file(filepath: str, lines: list[str]) -> None:
    """ Create a text file where each line is a subtitle from the subtitles list """
    with open(filepath, 'w', encoding='utf-8') as file:
        for line in lines:
            file.write(line + '\n')


def file_exists(filepath: str) -> str:
    return os.path.exists(filepath)


def open_transcript(filepath: str, video_id: str) -> str:
    file_destination = construct_transcript_output_file_destination(filepath, video_id)
    subtitles = read_lines_from_file(file_destination)
    transcript = ' '.join(subtitles)
    return transcript


def video_exists(filepath: str, video_url_or_id: str) -> bool:
    all_video_ids = read_video_ids_from_default_file(filepath)
    video_id = parse_out_video_id_if_its_in_url_format(video_url_or_id)
    if video_id in all_video_ids:
        return True
    file_destination = construct_video_input_file_destination(filepath)
    print(f"Error: video_id {video_id} does not exist in {file_destination}")
    return False

def read_ai_summary_from_file(filepath: str, video_id: str) -> list[str]:
    file_destination = construct_ai_summaries_output_file_destination(filepath, video_id)
    lines = read_lines_from_file(file_destination)
    return lines


def get_name_for_notes(filepath: str) -> str:
    no_toplevel = get_filepath_with_toplevel_folder_removed(filepath)
    if no_toplevel in FILEPATH_MAPPING:
        return FILEPATH_MAPPING[no_toplevel]
    return no_toplevel


def ensure_directory_exists() -> None:
    """ Create folder for 'MY_FILEPATH' if it does not exist """
    directory = os.path.dirname(CURRENTLY_SELECTED_SUBFOLDER)
    if not os.path.exists(directory):
        os.makedirs(directory)


def create_subfolder(subfolder: str) -> None:
    """ Create transcripts subfolder inside 'MY_FILEPATH' """
    ensure_directory_exists()
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)


def initialize_directory():
    ensure_directory_exists()
    transcripts_subfolder = f"{CURRENTLY_SELECTED_SUBFOLDER}/{FOLDERNAME_TRANSCRIPTS}"
    ai_summaries_subfolder = f"{CURRENTLY_SELECTED_SUBFOLDER}/{FOLDERNAME_AI_SUMMARIES}"
    notes_subfolder = f"{CURRENTLY_SELECTED_SUBFOLDER}/{FOLDERNAME_NOTES}"
    create_subfolder(transcripts_subfolder)
    create_subfolder(ai_summaries_subfolder)
    create_subfolder(notes_subfolder)


if __name__ == "__main__":
    # You are not supposed to run this script. See below.
    print("Error: This is a utils script that is providing helper functions for the other scripts!")