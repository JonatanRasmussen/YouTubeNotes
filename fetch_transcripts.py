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
    """ Create a text file where each line is a subtitle from the subtitles list """
    with open(f"{filepath}.txt", 'w', encoding='utf-8') as file:
        for subtitle in subtitles:
            file.write(subtitle + '\n')


def read_lines_from_file(filepath: str) -> list[str]:
    """ Read a file with a youtube_url or video_id
        on each line and return them as a list of strings.
        Please NOTE that empty lines and lines starting with # are ignored
        If two or more videos in the list are identical, print a warning in console """
    lines = []
    try:
        with open(f"{filepath}/{FILENAME_VIDEOS}", 'r', encoding='utf-8') as file:
            for line in file:
                if len(line.strip()) != 0 and not line.startswith(("#", " ")):
                    lines.append(line.strip())
    except FileNotFoundError:
        print(f"The file {filepath}.txt does not exist!")
    if contains_identical_videos(lines):
        print("Warning: Two or more videos in the list are identical!")
    return lines


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


def build_transcript_dict(videos: list[str]) -> dict[str,list[str]]:
    """ Takes a list of video urls or ids and returns a dict containing
        the video_id and a list of its subtitles as the key/value pair """
    transcript_dict = {}
    for i, video in enumerate(videos):
        video_id = parse_out_video_id_if_in_url_format(video)
        subtitles = get_list_of_subtitles(video_id)
        transcript_dict[video_id] = subtitles
        print(f"{i+1} of {len(videos)}: Transcript of video_id '{video_id}' fetched.")
    return transcript_dict


def execute(filepath: str) -> None:
    """ Reads list of videos from specified file, then fetches the transcript for each video
        and writes its subtitles to disk as a new file with the video_id as the file name """
    videos = read_lines_from_file(filepath)
    transcript_dict = build_transcript_dict(videos)
    for video_id, subtitles in transcript_dict:
        output_destination = f"{filepath}/{FOLDERNAME_TRANSCRIPTS}/{video_id}"
        write_subtitles_as_file(output_destination, subtitles)
        if VIDEO_UNAVAILABLE in subtitles:
            print("\n"+f"The video with video_id {video_id} received: {VIDEO_UNAVAILABLE}")
    print("\n"+f"Done! {len(videos)} transcripts successfully fetched and saved!")


if __name__ == "__main__":
    initialize_directory()
    execute(GLOBALLY_CONFIGURED_FILEPATH)