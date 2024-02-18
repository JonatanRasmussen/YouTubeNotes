import shutil
import os
import sqlite3
from datetime import datetime

from configs import (
    FILE_CONTAINING_OBSIDIAN_DESTINATION,
    FILENAME_START_NOTES,
)
from utils import (
    read_lines_from_file,
    read_single_line_from_file,
    parse_out_video_id_if_its_in_url_format,
    video_exists,
    construct_full_path,
    construct_final_notes_output_file_destination,
    construct_obsidian_notes_full_path,
    construct_obsidian_collection_of_notes_full_path,
    add_line_to_file,
)


def file_containing_obsidian_notes_directory_exists_and_isnt_empty() -> bool:
    chrome_history_directory = read_lines_from_file(FILE_CONTAINING_OBSIDIAN_DESTINATION)
    if len(chrome_history_directory) != 0:
        return True
    # If file is missing or is empty, alert user and create an empty placeholder file
    print(f"Error: The file {FILE_CONTAINING_OBSIDIAN_DESTINATION} did not exist!")
    print(f"       An empty file {FILE_CONTAINING_OBSIDIAN_DESTINATION} has been generated for you.")
    print(f"       Open {FILE_CONTAINING_OBSIDIAN_DESTINATION} and insert the path to your browsing history.")
    with open(FILE_CONTAINING_OBSIDIAN_DESTINATION, 'w', encoding='utf-8') as file:
        file.write("")
    return False


def move_notes_to_obsidian(filepath: str, video_id) -> str:
    if file_containing_obsidian_notes_directory_exists_and_isnt_empty():
        obsidian_notes_directory = read_single_line_from_file(FILE_CONTAINING_OBSIDIAN_DESTINATION)
        video_notes_path = construct_final_notes_output_file_destination(filepath, video_id)
        video_notes_full_destination = construct_full_path(video_notes_path)
        shutil.copy(video_notes_full_destination, obsidian_notes_directory)
        return obsidian_notes_directory
    print(f"The file {FILE_CONTAINING_OBSIDIAN_DESTINATION} is empty.")
    return ""


def get_video_title_from_notes(filepath: str, video_id: str) -> str:
    output_destination = construct_final_notes_output_file_destination(filepath, video_id)
    lines = read_lines_from_file(output_destination)
    for line in lines:
        if "**Video Title:**" in line:
            return line
    return "**Video Title:** -"


def update_obsidian_collection_of_notes(filepath: str, video_id: str) -> None:
    if file_containing_obsidian_notes_directory_exists_and_isnt_empty():
        obsidian_notes_directory = read_single_line_from_file(FILE_CONTAINING_OBSIDIAN_DESTINATION)
        collection_of_notes_fullpath = construct_obsidian_collection_of_notes_full_path(obsidian_notes_directory, filepath)
        video_title = get_video_title_from_notes(filepath, video_id)
        new_line = f"{video_title} ([[{FILENAME_START_NOTES}{video_id}]])\n"
        add_line_to_file(collection_of_notes_fullpath, new_line)


def generate_obsidian_notes(filepath: str, video_url_or_id: str, auto_open_note: bool) -> None:
    """ Copy notes for specified video to obsidian directory """
    video_id = parse_out_video_id_if_its_in_url_format(video_url_or_id)
    if video_exists(filepath, video_id):
        obsidian_notes_directory = move_notes_to_obsidian(filepath, video_id)
        update_obsidian_collection_of_notes(filepath, video_id)
        if obsidian_notes_directory != "" and auto_open_note:
            obsidian_notes_fullpath = construct_obsidian_notes_full_path(obsidian_notes_directory, video_id)
            os.startfile(obsidian_notes_fullpath)