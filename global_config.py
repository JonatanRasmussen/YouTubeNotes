import os

# Error messagse
VIDEO_UNAVAILABLE = "Error: This video is no longer available."

# STATIC_FOLDERS
TOPLEVEL_FOLDER = "data"
FILENAME_VIDEOS = "videos.txt"
FOLDERNAME_TRANSCRIPTS = "transcripts"
OPENAI_API_KEY_DESTINATION = "api_key.txt"



# (Step 1 of 2) Choose one
devin_nash_patreon = "devin_nash_patreon"


# (Step 2 of 2) INSERT BELOW
MY_FILEPATH = devin_nash_patreon
GLOBALLY_CONFIGURED_FILEPATH = f"{TOPLEVEL_FOLDER}/{MY_FILEPATH}"


def initialize_directory():
    create_directory()
    create_transcripts_subfolder()


def create_directory():
    """ Create folder for 'MY_FILEPATH' if it does not exist """
    directory = os.path.dirname(GLOBALLY_CONFIGURED_FILEPATH)
    if not os.path.exists(directory):
        os.makedirs(directory)

def create_transcripts_subfolder():
    """ Create transcripts subfolder inside 'MY_FILEPATH' """
    create_directory()
    transcripts_subfolder = f"{GLOBALLY_CONFIGURED_FILEPATH}/{FOLDERNAME_TRANSCRIPTS}"
    if not os.path.exists(transcripts_subfolder):
        os.makedirs(transcripts_subfolder)