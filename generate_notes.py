# This file is generate_ai_summary.py

import os
from openai import OpenAI
from configs import (
    CURRENTLY_SELECTED_SUBFOLDER,
    FILENAME_START_COLLECTION_OF_NOTES,
)
from utils import (
    initialize_directory,
    parse_out_video_id_if_its_in_url_format,
    construct_final_notes_output_file_destination,
    write_list_as_file,
    read_ai_summary_from_file,
    video_exists,
    get_name_for_notes,
    create_youtube_url_from_video_id,
    remove_empty_lines_and_comments,
)


def build_top_of_notes(filepath: str, video_id: str, video_title: str) -> list[str]:
    output_file_initial_lines = []
    output_file_initial_lines.append(video_title)
    unofficial_title = get_name_for_notes(filepath)
    formatted_unofficial_title = f"[[{FILENAME_START_COLLECTION_OF_NOTES}{unofficial_title}]]"
    output_file_initial_lines.append(formatted_unofficial_title)
    url = create_youtube_url_from_video_id(video_id)
    output_file_initial_lines.append(url)
    output_file_initial_lines.append("")
    return output_file_initial_lines


def modify_line_breaks(notes: list[str]) -> list[str]:
    modified_notes = remove_empty_lines_and_comments(notes)
    if len(modified_notes) >= 4:
        modified_notes.insert(3, "")
        modified_notes.insert(2, "")
    for i, modified_note in enumerate(modified_notes):
        modified_notes[i] = modified_note.replace("- **", "**")
    return modified_notes


def generate_notes(filepath: str, video_url_or_id: str, video_title: str) -> str:
    """ Reads list of videos from specified file, then fetches the transcript for each video
        and writes its subtitles to disk as a new file with the video_id as the file name """
    video_id = parse_out_video_id_if_its_in_url_format(video_url_or_id)
    notes = build_top_of_notes(filepath, video_id, video_title)
    if video_exists(filepath, video_url_or_id):
        ai_summary_as_list = read_ai_summary_from_file(filepath, video_id)
        for bullet_point in ai_summary_as_list:
            notes.append(bullet_point)
        modified_notes = modify_line_breaks(notes)
        output_destination = construct_final_notes_output_file_destination(filepath, video_id)
        write_list_as_file(output_destination, modified_notes)
        print(f"Notes for video_id {video_id} has been created.")
        return output_destination
    return ""


if __name__ == "__main__":
    initialize_directory()
    my_filepath = CURRENTLY_SELECTED_SUBFOLDER
    my_video_url_or_id = "Krz-WX82gHo"
    title = ""
    generate_notes(my_filepath, my_video_url_or_id, title)