import os

# SETTINGS PANEL NAME (Displayed on sidebar of settings in app)
PRESET_NAME = 'Configuration'

# Settings Panel Defaults
JSON_SETTINGS_PATH = "/Users/sachitnagpal/upenn/image_replays/settings.json"
DEFAULT_IDX = 0
DEFAULT_DF_PATH = os.getcwd()
DEFAULT_FOR_KEY = "ProblemId,StepNumber"
DEFAULT_PRIMARY_KEY = "problemid,stepnumber"
DEFAULT_PIC_URL = "PicUrl"
DEFAULT_QUES_TEXT = "clean_questiontext"
DEFAULT_PROB_ID = "problemid"
DEFAULT_STEP_NUM = "stepnumber"
DEFAULT_USER_NAME = "admin"

# KEYCODES
KEYCODE_NEXT = 40  # 40 - Enter key pressed

# TEXT

INITIAL_MESSAGE = "Please set the configuration from settings"
UNABLE_TO_LOAD_MESSAGE = "Please select the correct dataset path from settings"
COMPLETED_MESSAGE = "Reached end of file"
INC_POPUP_TITLE = 'Answer Required'
INC_POPUP_MSG = 'Please Answer all Questions'

