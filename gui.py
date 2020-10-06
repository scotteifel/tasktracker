import pyglet
from pyglet.window import mouse, key
from constants import *


class Window(pyglet.window.Window):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.background = pyglet.shapes.Rectangle(x=0,y=0,width=700,
                            height=700,color=WHITE_3)

        self.greeting_label = pyglet.text.Label(GREETING_TEXT,
                                x=50,y=WNDW_HEIGHT-40,bold=True,color=BLACK)

        self.add_task_btn = pyglet.shapes.Rectangle(
                                    x=ADD_TASK_COORDS[0],
                                    y=ADD_TASK_COORDS[1],
                                    width=ADD_TASK_SIZE,
                                    height=ADD_TASK_SIZE,
                                    color=DODGER_BLUE_3)

        self.task_btn_icon = pyglet.text.Label('+',x=ADD_TASK_COORDS[0]+12,
            y=ADD_TASK_COORDS[1]+11 ,bold=True,color=BLACK,font_size=20)


    def on_draw(self):
        self.clear()
        self.background.draw()
        self.greeting_label.draw()
        self.add_task_btn.draw()
        self.task_btn_icon.draw()

        if TASK_BX_LIST:
            for item in TASK_BX_LIST:
                item.draw_task_box()


    def on_mouse_motion(self, x,y,dx,dy):
        #Change add task button on hover
        if ADD_TASK_COORDS[0] < x < ADD_TASK_COORDS[0]+ADD_TASK_SIZE and \
        ADD_TASK_COORDS[1] < y < ADD_TASK_COORDS[1]+ADD_TASK_SIZE:
                self.add_task_btn.color = GREEN_3
        else:
                self.add_task_btn.color = DODGER_BLUE_3

        #Change different task's box on hover
        if TASK_BX_LIST:
            for item in TASK_BX_LIST:
                if item.isOver((x,y)):
                    item.color = (30,30,100)
                else:
                    item.color = TASK_BX_COLOR


    def on_mouse_press(self, x, y, button, modifiers):
        if button == mouse.LEFT and \
        ADD_TASK_COORDS[0] < x < ADD_TASK_COORDS[0] + ADD_TASK_SIZE and \
        ADD_TASK_COORDS[1] < y < ADD_TASK_COORDS[1] + ADD_TASK_SIZE:
            self.new_task()
            print('clicked')

        if TASK_BX_LIST:
            for item in TASK_BX_LIST:
                if button == mouse.LEFT and item.isOver((x,y)):
                    print('The left mouse button was pressed over '+item.label)

    def new_task(self):
        AddTask(WNDW_WIDTH//2,WNDW_HEIGHT//2,"New Task")


class AddTask(pyglet.window.Window):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.width = 400
        self.height = 150

        self.background = pyglet.shapes.Rectangle(x=0,y=0,width=self.width,
                            height=self.height,color=WHITE_3)

        self.greeting_label = pyglet.text.Label('Hey',
                                x=10,y=10,bold=True,color=BLACK)

    def on_draw(self):
        self.background.draw()
        self.greeting_label.draw()


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


if __name__ == '__main__':
    this1 = Window(WNDW_WIDTH,WNDW_HEIGHT,"TaskTrack")
    pyglet.app.run()
