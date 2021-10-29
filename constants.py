from win32api import GetSystemMetrics

S_WIDTH = GetSystemMetrics(0)
S_HEIGHT = GetSystemMetrics(1)

global description_window_open
global add_task_window_open
global completed_window_open
global notes_window_open

description_window_open = False
add_task_window_open = False
completed_window_open = False
notes_window_open = False


def window_placer():

    width = S_WIDTH//2
    height = S_HEIGHT//2
    return width, height


# Font
PROJ_FONT = 'Open Sans'

###  Sizes ###

TASK_BX_LIST = []
TASK_BX_HEIGHT = 50
TASK_BX_WIDTH = 100

WNDW_WIDTH = 600
WNDW_HEIGHT = 550

# The 'Add Task' button size and screen location information
ADD_ICON_SIZE = 40
ADD_ICON_COORDS = [WNDW_WIDTH//2-(ADD_ICON_SIZE//2), WNDW_HEIGHT-120]


####### Colors ##########


BLACK_ALPHA = (2, 2, 10, 255)  # 'Rich Black FOGRA'
CHRISTMAS_GREEN = (0, 135, 62)
DODGER_BLUE = (30, 144, 255)
LIGHTSABER_GREEN = (47, 249, 36)
OXFORD_BLUE = (5, 32, 74)  # Oxford Blue
OXFORD_BLUE_ALPHA = (5, 32, 74, 255)
MOUNTAIN_MEADOW = (2, 195, 154)

GREY = (206, 212, 218)

RED = (250, 82, 82)


RED_HOVER = RED
COMPLETED_HOVER = LIGHTSABER_GREEN
BRIGHT_GREEN_HOVER = LIGHTSABER_GREEN

# Adjustments
TASK_BTN_COLOR = ((0, 38, 59))
ICON_BOX_COLOR = (165, 200, 130)
ICON_BOX_COLOR = (105, 219, 124)

ORANGE = (255, 82, 0)


# Updating projects colors
TEXT_COLOR = BLACK_ALPHA

PROJECT_TITLE_COLOR = OXFORD_BLUE_ALPHA

TASK_LABELS_COLOR = (255, 161, 10, 255)
TASK_LABELS_BG_COLOR = OXFORD_BLUE

FINISH_PROJECT_BG_COLOR = MOUNTAIN_MEADOW
COMPLETED_BG_COLOR = MOUNTAIN_MEADOW
