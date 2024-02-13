# This file is generate_ai_summary.py

import os
from openai import OpenAI
from global_config import (
    GLOBALLY_CONFIGURED_FILEPATH,
    OPENAI_API_KEY_DESTINATION,
)
from utils import (
    initialize_directory,
    construct_video_input_file_destination,
    construct_transcript_output_file_destination,
    read_lines_from_file,
    read_video_ids_from_default_file,
    parse_out_video_id_if_in_url_format,
    construct_ai_summaries_output_file_destination,
    write_list_as_file,
    video_exists,
    file_exists,
)

def read_openai_api_key() -> str:
    """ Read OpenAI API Key from text file that is not public on github """
    try:
        with open(f"{OPENAI_API_KEY_DESTINATION}", 'r', encoding='utf-8') as file:
            for line in file:
                return line
    except FileNotFoundError:
        print(f"The file {OPENAI_API_KEY_DESTINATION}.txt does not exist!")
        return ""


def estimate_prompt_token_length(prompt: str) -> float:
    # Define constants
    characters_per_word = 4.7
    tokens_per_word = 1.33  # Approximately 750 words per 1000 tokens
    words_per_output = 200
    # Calculations
    input_token_count = (len(prompt) / characters_per_word) * tokens_per_word
    output_token_count = words_per_output * tokens_per_word
    total_token_count = input_token_count + output_token_count
    return total_token_count


def estimate_cost(prompt: str) -> str:
    """ Returns an estimate of the cost of sending a prompt to ChatGPT's API"""
    # Define constants
    input_cost_per_1000_tokens = 0.0005  # $0.0005 per 1000 tokens
    output_cost_per_1000_tokens = 0.0015  # $0.0015 per 1000 tokens
    # Calculations
    total_token_count = estimate_prompt_token_length(prompt)
    total_cost = (total_token_count / 1000) * (input_cost_per_1000_tokens + output_cost_per_1000_tokens)
    cost_str = "{:.2f}$".format(total_cost) # Format cost as string with 2 decimal places
    return cost_str


def shorten_prompt_if_too_long(prompt: str, max_tokens: str) -> str:
    prompt_token_count = estimate_prompt_token_length(prompt)
    if prompt_token_count > max_tokens:
        characters_per_word = 4.7 # Average characters per word in the english language
        tokens_per_word = 1.33  # Approximately 750 words per 1000 tokens
        limit = int((max_tokens / tokens_per_word) * characters_per_word)
        return prompt[0:limit] # Shorten prompt to not hit token limit
    return prompt

def chat_with_gpt(prompt: str) -> list[str]:
    """ Send prompt to ChatGPT """
    maximum_tokens_for_model = 16000
    prompt = shorten_prompt_if_too_long(prompt, maximum_tokens_for_model)
    api_key = read_openai_api_key()
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", api_key))
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
    )
    response_list = [choice.message.content for choice in response.choices]
    return response_list


def read_transcript_from_file(filepath: str, video_id: str) -> str:
    """ Open file containg subtitles and return all the subtitles joined together """
    transcript_destination = construct_transcript_output_file_destination(filepath, video_id)
    subtitles = read_lines_from_file(transcript_destination)
    transcript = ' '.join(subtitles)
    return transcript


def build_prompt_from_transcript(transcript: str) -> str:
    """ Builds and returns the prompt needed to obtain a video summary from ChatGPT """
    parts = []
    parts.append("The following is a transcript from a video that I need you to summarize for me.")
    parts.append("At the very top, add a video title suggestion that accurately describes the video content.")
    parts.append("The formatting of the video title suggestion should be: **Video Title:** your_title_goes_here .")
    parts.append("The next non-blank line should be a few key words covering what the video is about, separated by comma.")
    parts.append("The formatting of the key words should be: **Key Topics:** your_comma_separated_keywords_goes_here .")
    parts.append("The remaining lines should consist of 5-15 short and concise bullet points that summarizes the content.")
    parts.append("The formatting of these lines should be a hyphen-minus followed by a space followed by your bullet point.")
    parts.append("Avoid using unnecessary words and verbose phrasing. Be direct and to-the-point in your communication.")
    parts.append("I will take all of this and copy it into my notebook for personal use.")
    parts.append("The purpose of my notebook is being able to remember key takeaways from the video.")
    parts.append("Don't include small insignificant details, the overall message of the video is what's important.")
    parts.append("However, do include details that helps me remember or recall the video content.")
    parts.append("Here's the video transcript:")
    parts.append(transcript)
    full_prompt = ' '.join(parts)
    return full_prompt


def generate_bullet_points(filepath: str, video_id: str) -> list[str]:
    """ Build a prompt based on video_id and send it to ChatGPT. Return its response """
    transcript = read_transcript_from_file(filepath, video_id)
    full_prompt = build_prompt_from_transcript(transcript)
    cost_str = estimate_cost(full_prompt)
    print(f"AI Summary for video_id {video_id} is being generated. Estimated cost: {cost_str}")
    response_bullet_points = chat_with_gpt(full_prompt)
    return response_bullet_points


def generate_ai_summary(filepath: str, video_url_or_id: str) -> None:
    """ Reads list of videos from specified file, then fetches the transcript for each video
        and writes its subtitles to disk as a new file with the video_id as the file name """
    video_id = parse_out_video_id_if_in_url_format(video_url_or_id)
    output_destination = construct_ai_summaries_output_file_destination(filepath, video_id)
    if video_exists(filepath, video_url_or_id):
        if not file_exists(output_destination):
            summary_bullet_points = generate_bullet_points(filepath, video_id)
            write_list_as_file(output_destination, summary_bullet_points)
        else:
            print(f"AI summary for video_id {video_id} already exists. A new one was not generated.")


if __name__ == "__main__":
    initialize_directory()
    my_filepath = GLOBALLY_CONFIGURED_FILEPATH
    my_video_url_or_id = "Krz-WX82gHo"
    generate_ai_summary(my_filepath, my_video_url_or_id)