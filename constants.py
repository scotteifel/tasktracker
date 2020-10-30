from win32api import GetSystemMetrics

S_WIDTH = GetSystemMetrics(0)
S_HEIGHT = GetSystemMetrics(1)

def window_placer():

    width = S_WIDTH//2
    height = S_HEIGHT//2
    return width, height

# Colors have 2 values each,
# 3 values are for Rectangle objects,
# 4 are for label objects

BLACK = (0,0,0,255)
BLUE = (91, 115, 239, 255)
CHRISTMAS_GREEN = (0,135,62,255)
DODGER_BLUE = (30,144,255,255)
GREEN = (0,123,0,255)
GREY = (200, 200, 220, 255)
LIGHTSABER_GREEN = (47,249,36,255)
WHITE = (255,255,255,255)

BLACK_3 = (0,0,0)
BLUE_3 = (91, 115, 239)
CHRISTMAS_GREEN_3 = (0,135,62)
DODGER_BLUE_3 = (30,144,255)
GREEN_3 = (0,123,0)
GREY_3 = (200, 200, 220)
LIGHTSABER_GREEN_3 = (47,249,36)
WHITE_3 = (255,255,255)



##Must have only 3 values
ICON_BOX_COLOR = CHRISTMAS_GREEN_3
ICON_BOX_COLOR_HOVER = LIGHTSABER_GREEN_3

TASK_BTN_COLOR = BLUE_3
TASK_BTN_COLOR_HOVER = LIGHTSABER_GREEN_3

WNDW_WIDTH = 600
WNDW_HEIGHT = 500

TASK_BX_LIST = []
TASK_BX_HEIGHT = 50
TASK_BX_WIDTH = 100

##The 'Add Task' button size and screen location information
ADD_ICON_SIZE = 40
ADD_ICON_COORDS = [WNDW_WIDTH//2-ADD_ICON_SIZE,WNDW_HEIGHT-130]

GREETING_TEXT = 'Welcome to tasktrack.  To add a new task, press the plus \
sign.'


        # self.task_boxes.append(EnterIcon('new thing',
        #                         190,190,70,100,GREY,BLACK_3,self.batch))
