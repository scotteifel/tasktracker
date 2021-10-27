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

# Colors have 2 values each,
# 3 values are for Rectangle objects,
# 4 are for label objects

# 'Rich Black FOGRA'
BLACK = (2,2,10,255)
BLACK_3 = (2,2,10)


BLUE = (91, 115, 239, 255)
CHRISTMAS_GREEN = (0,135,62,255)
DODGER_BLUE = (30,144,255,255)
GREEN = (0,123,0,255)
GREY_3 = (206, 212, 218, 255)
LIGHTSABER_GREEN = (47,249,36,255)
ORANGE = (252,194,0,255)
WHITE = (255,255,255,255)

BLUE_3 = (91, 115, 239)
CHRISTMAS_GREEN_3 = (0,135,62)
DODGER_BLUE_3 = (30,144,255)
GREEN_3 = (0,123,0)
GREY_3 = (206, 212, 218)
LIGHTSABER_GREEN_3 = (47,249,36)
ORANGE_3 = (252,194,0)
PALE_GREEN_3 = (152,251,152)
RED_3 = (224, 49, 49)
WHITE_3 = (255,255,255)


# COLOR PALLETE
CREAM = '#FAF1E6'
CREAM = (250, 241, 230, 255)
CREAM = (15, 76, 117, 255)

BLUE4 = (255, 67, 1, 255)


ICON_BOX_COLOR = CHRISTMAS_GREEN_3
TASK_BTN_COLOR = PALE_GREEN_3

GREEN_HOVER = LIGHTSABER_GREEN_3
RED_HOVER = RED_3
COMPLETED_HOVER = LIGHTSABER_GREEN_3

# Adjustments
TASK_BTN_COLOR = ((0, 38, 59))
ICON_BOX_COLOR = (165,200,130)

COMPLETED_HOVER = LIGHTSABER_GREEN_3
ORANGE_3 = (255, 82, 0)

DODGER_BLUE_3 = (0, 161, 171)


##### Updating projects colors
TEXT_COLOR = (2,2,10,255)

PROJECT_TITLE_COLOR = (2, 32, 74, 255) #Oxford Blue

TASK_LABELS_COLOR = (255, 161, 10, 255)
TASK_LABELS_BG_COLOR = (5, 32, 74) #Oxford Blue

FINISH_PROJECT_BG_COLOR = (51,215,209)
COMPLETED_BG_COLOR = (51,215,209)


###  Sizes ###

WNDW_WIDTH = 600
WNDW_HEIGHT = 550

TASK_BX_LIST = []
TASK_BX_HEIGHT = 50
TASK_BX_WIDTH = 100

##The 'Add Task' button size and screen location information
ADD_ICON_SIZE = 40
ADD_ICON_COORDS = [WNDW_WIDTH//2-(ADD_ICON_SIZE//2),WNDW_HEIGHT-120]
