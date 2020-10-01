import pyglet
from pyglet.window import mouse, key

window = pyglet.window.Window(700,700,"TaskTrack")

background = pyglet.shapes.Rectangle(x=0,y=0,width=700,
                            height=700,color=(255,255,255))
background.draw()
window.clear()
background.draw()
print("done")
event_logger = pyglet.window.event.WindowEventLogger()
window.push_handlers(event_logger)

# rectang = pyglet.shapes.Rectangle(x=50,y=50,
#             width=100,height=50,color = (55,55,255))

# label = pyglet.text.Label("document", x=window.width//2,y=window.height//2,
# anchor_x='center',anchor_y='center')


class TaskBox:

    def __init__(self,label,x,y):
        self.win_size = window.get_size()
        self.label = label
        self.x = x
        self.y = y

    def draw_btn(self):

        task = pyglet.shapes.Rectangle(x=self.x,y=self.y,
                    width=100,height=50,color = (173, 216, 230))
        # task_border = pyglet.shapes.Rectangle(x=self.win_size[0]//2,y=self.win_size[1]//2,
        #             width=100,height=50,color = (55,55,255))

        label = pyglet.text.Label(self.label, x=task.position[0]+20,
                                    y=task.position[1]+20)
        task.draw()
        label.draw()


    def add_info(self,description):
        print(description)
        print(self.label)
        pass


    def isOver(self,pos):
        if pos[0] >self.x and pos[0] < self.x + 100:
            if pos[1] > self.y and pos[0] > self.y - 50:
                return True


    def time_adjuster(self,time):
        pass

# rectang = pyglet.shapes.Rectangle(x=win_size[0]//2,y=win_size[1]//2,
#             width=100,height=50,color = (55,55,255))

# @window.event




new_tang = TaskBox("Task1",50,50)
double_tang = TaskBox("AnotherTask",90,90)



@window.event
def on_draw():
    window.clear()
    background.draw()
    new_tang.draw_btn()
    double_tang.draw_btn()


@window.event
def on_mouse_motion(x,y,dx,dy):
    try:
        if new_tang.isOver((x,y)):
            print(x,y)
            new_tang.color = (200,200,200)
        else:
            new_tang.color = (173, 216, 230)
            print("Its elsed")
    except:
        print("no")

if __name__ == '__main__':
    pyglet.app.run()
