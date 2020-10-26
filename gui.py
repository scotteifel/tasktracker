import pyglet
from pyglet.window import mouse, key
from constants import *


class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super(Window,self).__init__(*args, **kwargs)
        self.task_list = []
        self.task_grid_x = int(50)
        self.task_grid_y = int(self.height-210)
        self.batch = pyglet.graphics.Batch()


        self.greeting_label = pyglet.text.Label(GREETING_TEXT,
            x=50, y=WNDW_HEIGHT-40, bold=True, color=BLACK,
            batch = self.batch)

        self.add_task_btn = pyglet.shapes.Rectangle(x=ADD_ICON_COORDS[0],
            y=ADD_ICON_COORDS[1], width=ADD_ICON_SIZE, height=ADD_ICON_SIZE,
            color=ORANGE)

        self.task_btn_icon = pyglet.text.Label('+',x=ADD_ICON_COORDS[0]+12,
            y=ADD_ICON_COORDS[1]+11 ,bold=True, color=BLACK, font_size=20)

    def on_draw(self):
        pyglet.gl.glClearColor(1, 1, 1, 1)
        self.clear()
        self.batch.draw()
        self.add_task_btn.draw()
        self.task_btn_icon.draw()

    def on_mouse_motion(self, x,y,dx,dy):
        #Change "+" button color on hover
        if ADD_ICON_COORDS[0] < x < ADD_ICON_COORDS[0]+ADD_ICON_SIZE and \
        ADD_ICON_COORDS[1] < y < ADD_ICON_COORDS[1]+ADD_ICON_SIZE:
                self.add_task_btn.color = GREEN_3
        else:
                self.add_task_btn.color = ORANGE

        if self.task_list:
            for item in self.task_list:
                if item.hit_test(x,y):
                    item.add_task_btn.color = GREEN_3
                else:
                    item.add_task_btn.color = ORANGE


    def on_mouse_press(self, x, y, button, modifiers):
        if button == mouse.LEFT and \
        ADD_ICON_COORDS[0] < x < ADD_ICON_COORDS[0] + ADD_ICON_SIZE and \
        ADD_ICON_COORDS[1] < y < ADD_ICON_COORDS[1] + ADD_ICON_SIZE:
            self.new_task()

        description_window = None
        if button == mouse.LEFT:
            if self.task_list:
                for item in self.task_list:
                    if item.hit_test(x,y):
                        if description_window == None:
                            description_window = TaskDescription(
                                        item.description, 200,200)
                            return

                    else:

                        if description_window == None:
                            pass
                        else:
                            description_window.close()
                            description_window = None

    def new_task(self):
        AddTask(WNDW_WIDTH//2,WNDW_HEIGHT//2,"New Task")

    def render_new_task(self, task_name, description):
        name = self.task_grid_x
        name = EnterIcon(task_name,
                          description,
                          self.task_grid_x,
                          self.task_grid_y,
                          60,
                          50,
                          GREY_3,
                          BLACK,
                          self.batch)

        self.task_list.append(name)

        self.task_grid_x += 75


class TaskDescription(pyglet.window.Window):
    def __init__(self,task_description, x, y):
        super().__init__()
        self.task_description = task_description

        self.greeting_label = pyglet.text.Label(self.task_description,
            x=10, y=10, bold=True, color=BLACK)



    def on_draw(self):
        pyglet.gl.glClearColor(1, 1, 1, 1)
        self.clear()
        self.greeting_label.draw()

    # @event



class AddTask(pyglet.window.Window):

    def __init__(self, *args, **kwargs):
        super().__init__(550, 500, caption='Text entry')
        self.batch = pyglet.graphics.Batch()
        self.greeting_label = pyglet.text.Label('Here I am. Enter new task',
            x=20,y=self.height-30,bold=True,color=BLACK, batch = self.batch)

        self.btn = EnterIcon('+','',50,self.height-100,50,60,DODGER_BLUE_3,
                                BLACK, self.batch)
        self.task = TextWidget('Enter taskname', 200, 350,
                                            130, self.batch)
        self.text_cursor = self.get_system_mouse_cursor('text')

        self.task_description = TextWidget('Description', 180, 150, 250,
                                    self.batch)

        self.focus = None
        self.set_focus(self.task)

    def on_draw(self):
        pyglet.gl.glClearColor(1, 1, 1, 1)
        self.clear()
        self.batch.draw()

    def on_mouse_motion(self, x, y, dx, dy):
            if self.task.hit_test(x, y):
                self.set_mouse_cursor(self.text_cursor)
            else:
                self.set_mouse_cursor(None)

            if self.task_description.hit_test(x, y):
                self.set_mouse_cursor(self.text_cursor)
            else:
                self.set_mouse_cursor(None)

            if self.btn.hit_test(x,y):
                self.btn.add_task_btn.color = GREEN_3
            else:
                self.btn.add_task_btn.color = DODGER_BLUE_3

    def on_mouse_press(self, x, y, button, modifiers):
        description = ''

        if self.task.hit_test(x, y):
            self.set_focus(self.task)
            return
        else:
            self.set_focus(None)


        if self.task_description.hit_test(x, y):
            self.set_focus(self.task_description)
        else:
            self.set_focus(None)


        if self.btn.hit_test(x,y):
            send_to_main_window(self.task.document.text,
                                self.task_description.document.text)
            self.close()

    def on_text(self, text):
        if self.focus:
            self.focus.caret.on_text(text)

    def on_text_motion(self, motion):
        if self.focus:
            self.focus.caret.on_text_motion(motion)

    def on_text_motion_select(self, motion):
        if self.focus:
            self.focus.caret.on_text_motion_select(motion)

        elif symbol == pyglet.window.key.ESCAPE:
            pyglet.app.exit()

    def on_key_press(self, symbol, modifiers):

        if symbol == pyglet.window.key.ENTER:
            pass

        if symbol == pyglet.window.key.ESCAPE:
            pyglet.app.exit()

    def set_focus(self, focus):
        if self.focus:
            self.focus.caret.visible = False
            self.focus.caret.mark = self.focus.caret.position = 0

        self.focus = focus
        if self.focus:
            self.focus.caret.visible = True
            self.focus.caret.mark = 0
            self.focus.caret.position = len(self.focus.document.text)


class EnterIcon(object):
    # A pressable icon
    def __init__(self,task_name,description,x,y, width, height,
                                    box_color, text_color,batch):
        self.task_name = task_name
        self.description = description
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.box_color = box_color
        self.text_color = text_color
        self.batch = batch

        self.add_task_btn = pyglet.shapes.Rectangle(x=self.x, y=self.y,
                width=self.width, height=self.height, color=self.box_color,
                                                    batch = self.batch)

        self.task_btn_icon = pyglet.text.Label(self.task_name,x=self.x+12,
            y=self.y+11 ,bold=True, color=self.text_color, font_size=15,
            batch=self.batch)

    def hit_test(self, x, y):
        return (0 < x - self.x < self.width and 0 < y - self.y < self.height)


class Rectangle(object):
    '''Draws a rectangle into a batch.'''
    def __init__(self, x1, y1, x2, y2, batch):
        self.vertex_list = batch.add(4, pyglet.gl.GL_QUADS, None,
            ('v2i', [x1, y1, x2, y1, x2, y2, x1, y2]),
            ('c4B', [200, 200, 220, 255] * 4)
        )


class TextWidget(object):
    def __init__(self, text, x, y, width, batch, height = None):
        self.document = pyglet.text.document.UnformattedDocument(text)
        self.document.set_style(0, len(self.document.text),
            dict(color=(0, 0, 0, 255)))

        font = self.document.get_font()
        if height:
            print("passed")
            pass
        else:
            height = font.ascent - font.descent
        # height = font.ascent - font.descent

        pad = 2
        self.rectangle = Rectangle(x - pad, y - pad,
        x + width + pad, y + height*3 + pad, batch)

        self.layout = pyglet.text.layout.IncrementalTextLayout(
                  self.document, width, height*3, multiline=True, batch=batch)
        self.caret = pyglet.text.caret.Caret(self.layout)

        self.layout.x = x
        self.layout.y = y

        # Rectangular outline

    def hit_test(self, x, y):
        return (0 < x - self.layout.x < self.layout.width and
                0 < y - self.layout.y < self.layout.height)


class TaskBox(object):
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

def send_to_main_window(task_name, description):
    this1.render_new_task(task_name, description)

this1 = Window(WNDW_WIDTH,WNDW_HEIGHT,"TaskTrack")
pyglet.app.run()
