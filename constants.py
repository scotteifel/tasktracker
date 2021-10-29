from win32api import GetSystemMetrics

# Screen dimensions
S_WIDTH = GetSystemMetrics(0)
S_HEIGHT = GetSystemMetrics(1)

global description_window_open
global add_task_window_open
global completed_window_open
global notes_window_open

# Helps prevent multiple windows of same type from opening
description_window_open = False
add_task_window_open = False
completed_window_open = False
notes_window_open = False


# Center an app window on the monitor
def window_placer():

    width = S_WIDTH//2
    height = S_HEIGHT//2
    return width, height


# Font

PROJ_FONT = 'Open Sans'

###########
#  Sizes 
##########

# TASK_BX_LIST = []
# TASK_BX_HEIGHT = 50
# TASK_BX_WIDTH = 100

WNDW_WIDTH = 600
WNDW_HEIGHT = 550

# The 'Add Task' button size and screen location information
ADD_ICON_SIZE = 40
ADD_ICON_COORDS = [WNDW_WIDTH//2-(ADD_ICON_SIZE//2), WNDW_HEIGHT-120]

#######################
#        Colors 
######################

RED = (250, 82, 82)
DARK_BLUE = (0, 38, 59)  

GREEN = (105, 219, 124)  # Like Pistachio Green
LIGHT_GREEN = (140, 233, 154)
LIGHTSABER_GREEN = (47, 249, 36)

ORANGE_ALPHA = (255, 161, 10, 255)  # Dark Orange

OXFORD_BLUE_ALPHA = (5, 32, 74, 255)
OXFORD_BLUE = (5, 32, 74)  # Oxford Blue

MOUNTAIN_MEADOW = (2, 195, 154) # Shade of green
BLACK_ALPHA = (2, 2, 10, 255)  # 'Rich Black FOGRA'

#_________________________

TASK_LABELS_COLOR = ORANGE_ALPHA
TASK_LABELS_BG_COLOR = OXFORD_BLUE
TEXT_COLOR = BLACK_ALPHA
PROJECT_TITLE_COLOR = OXFORD_BLUE_ALPHA

TASK_BTN_COLOR = DARK_BLUE
ADD_TASK_BTN_COLOR = GREEN

RED_HOVER = RED
COMPLETED_HOVER = LIGHTSABER_GREEN
BRIGHT_GREEN_HOVER = LIGHTSABER_GREEN

ALERT_COLOR = (240,62,62,255) # Shade of Red

FINISH_PROJECT_BG_COLOR = LIGHT_GREEN
# Might want to not highlight the completed tab if it's empty.
COMPLETED_BG_COLOR = LIGHT_GREEN

# Colors used directly in gui.py
GREY = (206, 212, 218)
BLUE = (165, 216, 255)
####