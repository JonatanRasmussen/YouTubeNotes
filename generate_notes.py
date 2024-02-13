# This file is generate_ai_summary.py

import os
from openai import OpenAI
from global_config import (
    GLOBALLY_CONFIGURED_FILEPATH,
)
from utils import (
    initialize_directory,
    parse_out_video_id_if_in_url_format,
    construct_final_notes_output_file_destination,
    write_list_as_file,
    read_ai_summary_from_file,
    video_exists,
    get_name_for_notes,
    create_youtube_url_from_video_id,
    remove_empty_lines_and_comments,
)


def build_top_of_notes(filepath: str, video_id: str) -> list[str]:
    output_file_initial_lines = []
    title = get_name_for_notes(filepath)
    formatted_title = f"[[{title}]]"
    output_file_initial_lines.append(formatted_title)
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


def generate_notes(filepath: str, video_url_or_id: str) -> None:
    """ Reads list of videos from specified file, then fetches the transcript for each video
        and writes its subtitles to disk as a new file with the video_id as the file name """
    video_id = parse_out_video_id_if_in_url_format(video_url_or_id)
    notes = build_top_of_notes(filepath, video_id)
    if video_exists(filepath, video_url_or_id):
        ai_summary_as_list = read_ai_summary_from_file(filepath, video_id)
        for bullet_point in ai_summary_as_list:
            notes.append(bullet_point)
        modified_notes = modify_line_breaks(notes)
        output_destination = construct_final_notes_output_file_destination(filepath, video_id)
        write_list_as_file(output_destination, modified_notes)
        print(f"Notes for video_id {video_id} has been created.")


if __name__ == "__main__":
    initialize_directory()
    my_filepath = GLOBALLY_CONFIGURED_FILEPATH
    my_video_url_or_id = "Krz-WX82gHo"
    generate_notes(my_filepath, my_video_url_or_id)