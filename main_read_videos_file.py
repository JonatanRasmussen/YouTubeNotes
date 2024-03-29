# This file is main.py

# pip install youtube-transcript-api
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import VideoUnavailable
from configs import (
    CURRENTLY_SELECTED_SUBFOLDER,
    FILENAME_VIDEOS,
)
from utils import (
    read_video_ids_from_custom_file,
    parse_out_video_id_if_its_in_url_format,
    initialize_directory,
)
from fetch_transcript import fetch_transcript
from generate_ai_summary import generate_ai_summary
from generate_notes import generate_notes
from generate_obsidian_notes import generate_obsidian_notes


def main_read_videos_file(filepath: str, videos_filename: str) -> None:
    """ Use AI to generate notes for a YouTube video """
    video_urls_or_ids = read_video_ids_from_custom_file(filepath, videos_filename)
    for i, video_url_or_id in enumerate(video_urls_or_ids):
        video_id = parse_out_video_id_if_its_in_url_format(video_url_or_id)
        fetch_transcript(filepath, video_id)
        generate_ai_summary(filepath, video_id)
        video_title = ""
        output_destination = generate_notes(filepath, video_id, video_title)
        if output_destination != "":
            generate_obsidian_notes(filepath, video_id, False)
        print(f"{i+1} of {len(video_urls_or_ids)}: video_id {video_id} processed."+"\n")


if __name__ == "__main__":
    initialize_directory()
    my_filepath = CURRENTLY_SELECTED_SUBFOLDER
    my_filename = FILENAME_VIDEOS
    main_read_videos_file(my_filepath, my_filename)