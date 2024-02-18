# This file is global_config.py

import os

# Error messagse
VIDEO_UNAVAILABLE = "Error: This video is no longer available."

# STATIC_FOLDERS
TOPLEVEL_FOLDER = "data"
FILENAME_VIDEOS = "videos.txt"
FOLDERNAME_TRANSCRIPTS = "transcripts"
FOLDERNAME_AI_SUMMARIES = "ai_summaries"
FOLDERNAME_NOTES = "notes"
FILE_CONTAINING_OPENAI_API_KEY = "api_key.txt"
FILENAME_COPY_OF_BROWSING_HISTORY = "browsing_history"
FILE_CONTAINING_BROWSING_HISTORY_DIRECTORY = "browsing_history_destination.txt"


# (Step 1 of 2) Choose one
devin_nash_patreon = "devin_nash_patreon"


# (Step 2 of 2) INSERT BELOW
MY_FILEPATH = devin_nash_patreon
CURRENTLY_SELECTED_SUBFOLDER = f"{TOPLEVEL_FOLDER}/{MY_FILEPATH}"



notes_name_devin_nash_patreon = "Devin Nash"
FILEPATH_MAPPING = {devin_nash_patreon: notes_name_devin_nash_patreon,
                    'test_key': 'test_value',
                    }