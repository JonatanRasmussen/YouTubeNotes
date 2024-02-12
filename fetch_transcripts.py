# pip install youtube-transcript-api
import re
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import VideoUnavailable
from global_config import (
    GLOBALLY_CONFIGURED_FILEPATH,
    FILENAME_VIDEOS,
    FOLDERNAME_TRANSCRIPTS,
    VIDEO_UNAVAILABLE,
    initialize_directory
)

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


def get_transcript_object(video_url_or_id: str) -> list:
    """ Returns a list of dictionaries looking like this:
    [
        {
            'text': 'Hey there',
            'start': 7.58,
            'duration': 6.13
        },
        {
            'text': 'how are you',
            'start': 14.08,
            'duration': 7.58
        },
        # ...
    ]"""
    video_id = parse_out_video_id_if_in_url_format(video_url_or_id)
    return YouTubeTranscriptApi.get_transcript(video_id, preserve_formatting=True) # Add preserve_formatting=True if you'd like to keep HTML formatting elements such as <i> (italics) and <b> (bold).


def get_list_of_subtitles(video_url_or_id: str) -> list[str]:
    """ Returns a list of each subtitle for the specified video_id """
    video_id = parse_out_video_id_if_in_url_format(video_url_or_id)
    try:
        transcript_obj = get_transcript_object(video_id)
        subtitle_lst = []
        for element in transcript_obj:
            subtitle = element['text']
            subtitle_lst.append(subtitle)
        return subtitle_lst
    except VideoUnavailable:
        return [VIDEO_UNAVAILABLE]


def write_subtitles_as_file(filepath: str, subtitles: list[str]) -> None:
    with open(filepath, 'w', encoding='utf-8') as file:
        for subtitle in subtitles:
            file.write(subtitle + '\n')


def read_lines_from_file(filepath: str) -> list[str]:
    """ Read a file with a youtube_url or video_id
        on each line and return them as a list of strings.
        Please NOTE that empty lines and lines starting with # are ignored """
    lines = []
    try:
        with open(f"{filepath}/{FILENAME_VIDEOS}", 'r', encoding='utf-8') as file:
            for line in file:
                if len(line.strip()) != 0 and not line.startswith(("#", " ")):
                    lines.append(line.strip())
    except FileNotFoundError:
        print(f"The file {filepath}.txt does not exist!")
    return lines


def execute(filepath: str) -> None:
    unavailable_video_ids = []
    youtube_urls_or_video_ids = read_lines_from_file(filepath)
    number_of_videos = len(youtube_urls_or_video_ids)
    i = 0
    for element in youtube_urls_or_video_ids:
        video_id = parse_out_video_id_if_in_url_format(element)
        output_destination = f"{filepath}/{FOLDERNAME_TRANSCRIPTS}/{video_id}"
        subtitles = get_list_of_subtitles(video_id)
        if len(subtitles) == 0 or subtitles[0] == VIDEO_UNAVAILABLE:
            unavailable_video_ids.append(video_id)
        write_subtitles_as_file(output_destination, subtitles)
        i = i+1
        print(f"{i} of {number_of_videos}: Transcript of video_id '{video_id}' saved to {filepath}")

    for video in unavailable_video_ids:
        print(f"The video with video_id {video} received: {VIDEO_UNAVAILABLE}")
    print()
    print(f"Done! {number_of_videos} transcripts fetched and saved.")


if __name__ == "__main__":
    initialize_directory()
    execute(GLOBALLY_CONFIGURED_FILEPATH)