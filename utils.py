# This file is utils.py
import os
import re

from global_config import (
    FILENAME_VIDEOS,
    FOLDERNAME_TRANSCRIPTS,
    FOLDERNAME_AI_SUMMARIES,
    FOLDERNAME_NOTES,
    TOPLEVEL_FOLDER,
    FILEPATH_MAPPING,
    GLOBALLY_CONFIGURED_FILEPATH,
)


def construct_video_input_file_destination(filepath: str) -> str:
    return f"{filepath}/{FILENAME_VIDEOS}"


def construct_transcript_output_file_destination(filepath: str, video_id: str) -> str:
    return f"{filepath}/{FOLDERNAME_TRANSCRIPTS}/{video_id}.txt"


def construct_ai_summaries_output_file_destination(filepath: str, video_id: str) -> str:
    return f"{filepath}/{FOLDERNAME_AI_SUMMARIES}/{video_id}.txt"


def construct_final_notes_output_file_destination(filepath: str, video_id: str) -> str:
    return f"{filepath}/{FOLDERNAME_NOTES}/{video_id}.md"


def get_filepath_with_toplevel_folder_removed(filepath: str) -> str:
    return filepath.replace(f"{TOPLEVEL_FOLDER}/", "")


def parse_out_video_id_if_in_url_format(video_url_or_id: str):
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
            video_i = parse_out_video_id_if_in_url_format(lst[i])
            video_k = parse_out_video_id_if_in_url_format(lst[k])
            if video_i == video_k:
                return True
    return False


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
    return lines


def remove_empty_lines_and_comments(lines: list[str]) -> list[str]:
    video_urls_or_ids = []
    for line in lines:
        if len(line.strip()) != 0 and not line.startswith(("#", " ")):
            video_urls_or_ids.append(line)
    return video_urls_or_ids


def convert_incorrect_video_id_formats(video_urls_or_ids: list[str]) -> list[str]:
    video_ids = []
    for video_url_or_id in video_urls_or_ids:
        video_id = parse_out_video_id_if_in_url_format(video_url_or_id)
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
    video_id = parse_out_video_id_if_in_url_format(video_url_or_id)
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
    directory = os.path.dirname(GLOBALLY_CONFIGURED_FILEPATH)
    if not os.path.exists(directory):
        os.makedirs(directory)


def create_subfolder(subfolder: str) -> None:
    """ Create transcripts subfolder inside 'MY_FILEPATH' """
    ensure_directory_exists()
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)


def initialize_directory():
    ensure_directory_exists()
    transcripts_subfolder = f"{GLOBALLY_CONFIGURED_FILEPATH}/{FOLDERNAME_TRANSCRIPTS}"
    ai_summaries_subfolder = f"{GLOBALLY_CONFIGURED_FILEPATH}/{FOLDERNAME_AI_SUMMARIES}"
    notes_subfolder = f"{GLOBALLY_CONFIGURED_FILEPATH}/{FOLDERNAME_NOTES}"
    create_subfolder(transcripts_subfolder)
    create_subfolder(ai_summaries_subfolder)
    create_subfolder(notes_subfolder)


if __name__ == "__main__":
    # You are not supposed to run this script. See below.
    print("Error: This is a utils script that is providing helper functions for the other scripts!")