# This file is fetch_transcript.py

# pip install youtube-transcript-api
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import VideoUnavailable
from youtube_transcript_api._errors import TranscriptsDisabled
from configs import (
    CURRENTLY_SELECTED_SUBFOLDER,
    VIDEO_UNAVAILABLE,
    SUBTITLES_DISABLED,
)
from utils import (
    initialize_directory,
    read_video_ids_from_default_file,
    write_list_as_file,
    construct_transcript_output_file_destination,
    parse_out_video_id_if_its_in_url_format,
    video_exists,
    file_exists,
)


def get_transcript_object(video_id: str) -> list:
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
    return YouTubeTranscriptApi.get_transcript(video_id, preserve_formatting=True) # Add preserve_formatting=True if you'd like to keep HTML formatting elements such as <i> (italics) and <b> (bold).


def obtain_subtitles_via_transcript_object(video_id: str) -> list[str]:
    """ Returns a list of each subtitle for the specified video_id """
    try:
        transcript_obj = get_transcript_object(video_id)
        subtitle_lst = []
        for element in transcript_obj:
            subtitle = element['text']
            subtitle_lst.append(subtitle)
        return subtitle_lst
    except VideoUnavailable:
        return [VIDEO_UNAVAILABLE]
    except TranscriptsDisabled:
        return [SUBTITLES_DISABLED]


def build_transcript_dict(video_ids: list[str]) -> dict[str,list[str]]:
    """ Takes a list of video urls or ids and returns a dict containing
        the video_id and a list of its subtitles as the key/value pair """
    transcript_dict = {}
    for i, video_id in enumerate(video_ids):
        subtitles = obtain_subtitles_via_transcript_object(video_id)
        transcript_dict[video_id] = subtitles
        print(f"{i+1} of {len(video_ids)}: Transcript of video_id '{video_id}' fetched successfully.")
        if subtitles == VIDEO_UNAVAILABLE:
            print(f"Error when requesting transcript for video_id {video_id}: {VIDEO_UNAVAILABLE}")
    return transcript_dict


def fetch_transcript_for_all(filepath: str) -> None:
    """ Reads list of videos from specified file, then fetches the transcript for each video
        and writes its subtitles to disk as a new file with the video_id as the file name """
    videos = read_video_ids_from_default_file(filepath)
    transcript_dict = build_transcript_dict(videos)
    for video_id, subtitles in transcript_dict.items():
        output_destination = construct_transcript_output_file_destination(filepath, video_id)
        write_list_as_file(output_destination, subtitles)
        if subtitles == VIDEO_UNAVAILABLE:
            print(f"Error when requesting transcript for video_id {video_id}: {VIDEO_UNAVAILABLE}")
        if subtitles == SUBTITLES_DISABLED:
            print(f"Error when requesting transcript for video_id {video_id}: {SUBTITLES_DISABLED}")
    print(f"Done! {len(videos)} transcripts successfully fetched and saved!")


def fetch_transcript(filepath: str, video_url_or_id: str) -> None:
    if video_exists(filepath, video_url_or_id):
        video_id = parse_out_video_id_if_its_in_url_format(video_url_or_id)
        output_destination = construct_transcript_output_file_destination(filepath, video_id)
        if not file_exists(output_destination):
            subtitles = obtain_subtitles_via_transcript_object(video_id)
            write_list_as_file(output_destination, subtitles)
            if subtitles == VIDEO_UNAVAILABLE:
                print(f"Error when requesting transcript for video_id {video_id}: {VIDEO_UNAVAILABLE}")
            if subtitles == SUBTITLES_DISABLED:
                print(f"Error when requesting transcript for video_id {video_id}: {SUBTITLES_DISABLED}")
            print(f"Transcript of video_id '{video_id}' fetched successfully.")
        else:
            print(f"Transcript of video_id '{video_id}' has previously been fetched.")


if __name__ == "__main__":
    initialize_directory()
    my_filepath = CURRENTLY_SELECTED_SUBFOLDER
    fetch_transcript_for_all(my_filepath)