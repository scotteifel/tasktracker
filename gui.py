import pyglet
from pyglet.window import mouse, key
from constants import *



greeting_text = 'Welcome to tasktrack.  To add a new task, press the plus \
sign.'



##The 'Add Task' button size and screen location information
ADD_TASK_SIZE = 40
ADD_TASK_COORDS = [WNDW_WIDTH//2-ADD_TASK_SIZE,WNDW_HEIGHT-130]


window = pyglet.window.Window(WNDW_WIDTH,WNDW_HEIGHT,"TaskTrack")

background = pyglet.shapes.Rectangle(x=0,y=0,width=700,
                    height=700,color=WHITE_3)

greeting_label = pyglet.text.Label(greeting_text,
                        x=30,y=WNDW_HEIGHT-30,bold=True,color=BLACK)

add_task_btn = pyglet.shapes.Rectangle(
                            x=ADD_TASK_COORDS[0],
                            y=ADD_TASK_COORDS[1],
                            width=ADD_TASK_SIZE,
                            height=ADD_TASK_SIZE,
                            color=DODGER_BLUE_3)

task_btn_icon = pyglet.text.Label('+',x=ADD_TASK_COORDS[0]+12,
    y=ADD_TASK_COORDS[1]+11 ,bold=True,color=BLACK,font_size=20)


# document = pyglet.text.document.FormattedDocument()
# layout = pyglet.text.layout.IncrementalTextLayout(document, 30, 20)
# caret = pyglet.text.caret.Caret(layout)
# window.push_handlers(caret)

class TaskBox:

    def __init__(self,label,x,y):
        self.win_size = window.get_size()
        self.label = label
        self.x = x
        self.y = y
        self.color = TASK_BX_COLOR


    def draw_task_box(self):

        self.task = pyglet.shapes.Rectangle(x=self.x,y=self.y,
              width=TASK_BX_WIDTH,height=TASK_BX_HEIGHT,color = self.color)

        self.title = pyglet.text.Label(self.label, x=self.task.position[0]+20,
                                    y=self.task.position[1]+20)
        self.task.draw()
        self.title.draw()


    def add_info(self,description):
        print(description)
        print(self.label)
        pass


    def isOver(self,pos):
        if pos[0] > self.x and pos[0] < self.x + TASK_BX_WIDTH:
            if pos[1] > self.y and pos[1] < self.y + TASK_BX_HEIGHT:
                return True


    def time_adjuster(self,time):
        pass


# new_tang = TaskBox("Task1",50,WNDW_HEIGHT - 80)
# double_tang = TaskBox("AnotherTask",150,WNDW_HEIGHT - 80)
# TASK_BX_LIST.append(new_tang)
# TASK_BX_LIST.append(double_tang)


@window.event
def on_draw():
    window.clear()
    background.draw()
    greeting_label.draw()
    add_task_btn.draw()
    task_btn_icon.draw()

    if TASK_BX_LIST:
        for item in TASK_BX_LIST:
            item.draw_task_box()


@window.event
def on_mouse_motion(x,y,dx,dy):
    #Change add task button on hover
    if ADD_TASK_COORDS[0] < x < ADD_TASK_COORDS[0]+ADD_TASK_SIZE and \
    ADD_TASK_COORDS[1] < y < ADD_TASK_COORDS[1]+ADD_TASK_SIZE:
            add_task_btn.color = GREEN_3
    else:
        add_task_btn.color = DODGER_BLUE_3

    #Change different task's box on hover
    if TASK_BX_LIST:
        for item in TASK_BX_LIST:
            if item.isOver((x,y)):
                item.color = (30,30,100)
            else:
                item.color = TASK_BX_COLOR


@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == mouse.LEFT and \
    ADD_TASK_COORDS[0] < x < ADD_TASK_COORDS[0]+ADD_TASK_SIZE and \
    ADD_TASK_COORDS[1] < y < ADD_TASK_COORDS[1]+ADD_TASK_SIZE:
        print('clicked')

    if TASK_BX_LIST:
        for item in TASK_BX_LIST:
            if button == mouse.LEFT and item.isOver((x,y)):
                print('The left mouse button was pressed over '+item.label)


if __name__ == '__main__':
    pyglet.app.run()
