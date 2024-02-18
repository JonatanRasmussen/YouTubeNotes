# This file is global_config.py

import os

# Error messagse
VIDEO_UNAVAILABLE = "Error: This video is no longer available."
SUBTITLES_DISABLED = "Error: Subtitles are disabled for this video."

# STATIC_FOLDERS
TOPLEVEL_FOLDER = "data"
FILENAME_VIDEOS = "videos.txt"
FOLDERNAME_TRANSCRIPTS = "transcripts"
FOLDERNAME_AI_SUMMARIES = "ai_summaries"
FOLDERNAME_NOTES = "notes"
FILENAME_START_NOTES = "yt+"
FILENAME_START_COLLECTION_OF_NOTES = "yt++"
FILE_CONTAINING_OPENAI_API_KEY = "api_key.txt"
FILENAME_COPY_OF_BROWSING_HISTORY = "browsing_history"
FILE_CONTAINING_BROWSING_HISTORY_DIRECTORY = "browsing_history_destination.txt"
FILE_CONTAINING_OBSIDIAN_DESTINATION = "b_obsidian_destination.txt"


# (Step 1 of 2) Choose one
devin_nash_patreon = "devin_nash_patreon"


# (Step 2 of 2) INSERT BELOW
MY_FILEPATH = devin_nash_patreon
CURRENTLY_SELECTED_SUBFOLDER = f"{TOPLEVEL_FOLDER}/{MY_FILEPATH}"