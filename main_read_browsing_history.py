# This file is main.py

# pip install youtube-transcript-api
import os
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import VideoUnavailable
from configs import (
    CURRENTLY_SELECTED_SUBFOLDER,
)
from utils import (
    parse_out_video_id_if_its_in_url_format,
    initialize_directory,
)
from fetch_latest_url import fetch_latest_url
from fetch_transcript import fetch_transcript
from generate_ai_summary import generate_ai_summary
from generate_notes import generate_notes
from generate_obsidian_notes import generate_obsidian_notes


def main_read_browsing_history(filepath: str) -> None:
    """ Use AI to generate notes for most recently watched YouTube video """
    video_url_and_title = fetch_latest_url(filepath)
    if len(video_url_and_title) != 0:
        url = video_url_and_title[0]
        title = video_url_and_title[1]
        print(f"Creating notes for {title}")
        video_id = parse_out_video_id_if_its_in_url_format(url)
        fetch_transcript(filepath, video_id)
        generate_ai_summary(filepath, video_id)
        output_destination = generate_notes(filepath, video_id, title)
        if output_destination != "":
            generate_obsidian_notes(filepath, video_id, True)


if __name__ == "__main__":
    initialize_directory()
    my_filepath = CURRENTLY_SELECTED_SUBFOLDER
    main_read_browsing_history(my_filepath)