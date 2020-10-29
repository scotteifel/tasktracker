import pyglet
from pyglet.window import mouse, key
from create_db import create_database
from db_functions import *
from constants import *

##EVENT LOGGER CODE
event_logger = pyglet.window.event.WindowEventLogger()

class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super(Window,self).__init__(*args, **kwargs)
        self.set_location(S_WIDTH//2-120,S_HEIGHT//3)

        self.task_list = []
        self.task_grid_x = int(50)
        self.task_grid_y = int(self.height-210)
        self.batch = pyglet.graphics.Batch()

        self.greeting_label = pyglet.text.Label(GREETING_TEXT,
            x=50, y=WNDW_HEIGHT-40, bold=True, color=BLACK,
            batch = self.batch)

        self.add_task_btn = pyglet.shapes.Rectangle(x=ADD_ICON_COORDS[0],
            y=ADD_ICON_COORDS[1], width=ADD_ICON_SIZE, height=ADD_ICON_SIZE,
            color=ICON_BOX_COLOR)

        self.task_btn_icon = pyglet.text.Label('+',x=ADD_ICON_COORDS[0]+12,
            y=ADD_ICON_COORDS[1]+11 ,bold=True, color=BLACK, font_size=20)

    def retrieve_saved_tasks(self):
        tasks = retrieve_tasks()
        print(tasks)
        if tasks:
            for item in tasks:
                self.render_new_task(item[0],item[1])

    def on_draw(self):
        pyglet.gl.glClearColor(1, 1, 1, 1)
        self.clear()
        self.batch.draw()
        self.add_task_btn.draw()
        self.task_btn_icon.draw()

    def on_mouse_motion(self, x,y,dx,dy):
        #Change "+" button color on hover

        if hit_test(self.add_task_btn, x, y):
                self.add_task_btn.color = ICON_BOX_COLOR_HOVER
        else:
                self.add_task_btn.color = ICON_BOX_COLOR

        if self.task_list:
            for item in self.task_list:
                if hit_test(item, x, y):
                    item.color = ICON_BOX_COLOR_HOVER
                else:
                    item.color = ICON_BOX_COLOR


    def on_mouse_press(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            if hit_test(self.add_task_btn, x, y):
                self.new_task()

        description_window = None
        if button == mouse.LEFT:
            if self.task_list:
                #cnt used to match db result with self.task_list place
                cnt = 0
                for item in self.task_list:
                    if hit_test(item, x, y):
                        if description_window == None:
                            info = retrieve_tasks()
                            print(info[cnt], ' IS INFO 1')

                            x_y = self.get_location()
                            description_window = TaskDescription(
                                        info[cnt][1], x_y[0], x_y[1])
                            return
                    else:
                        cnt += 1

                        if description_window == None:
                            pass
                        else:
                            description_window.close()
                            description_window = None
                    #         try:
                    #             print('trying')
                    #             description_window = TaskDescription(
                    #                         item.description, x_y[0], x_y[1])
                    #         except Exception as e:
                    #             print('accepted')
                    #             exit(1)
                    #         return
                    #
                    # else:
                    #
                    #     if description_window == None:
                    #         pass
                    #     else:
                    #         description_window.close()
                    #         description_window = None

    def new_task(self):
        AddTask(WNDW_WIDTH//2,WNDW_HEIGHT//2,"New Task")

    def render_new_task(self, task_name, description):
        name = self.task_grid_x
        name = pyglet.shapes.Rectangle(self.task_grid_x, self.task_grid_y,
                    width=80,height=60,color=ICON_BOX_COLOR,batch=self.batch)
        # name = EnterIcon(task_name,
        #                   description,
        #                   self.task_grid_x,
        #                   self.task_grid_y,
        #                   GREY_3,
        #                   BLACK,
        #                   self.batch,
        #                   width=75,
        #                   height=50,
        #                   font_size=12)

        self.task_list.append(name)

        self.task_grid_x += 85

    # def render_new_task(self, task_name, description):
    #     name = self.task_grid_x
    #     name = EnterIcon(task_name,
    #                       description,
    #                       self.task_grid_x,
    #                       self.task_grid_y,
    #                       GREY_3,
    #                       BLACK,
    #                       self.batch,
    #                       width=75,
    #                       height=50,
    #                       font_size=12)
    #
    #     self.task_list.append(name)
    #
    #     self.task_grid_x += 75




class AddTask(pyglet.window.Window):

    def __init__(self, *args, **kwargs):
        super().__init__(550, 500, caption='ADD TASK')
        self.set_location(S_WIDTH//2-160,S_HEIGHT//3-30)
        self.batch = pyglet.graphics.Batch()
        self.greeting_label = pyglet.text.Label('Enter new task',
        x=200,y=self.height-30,bold=True,color=BLACK, batch = self.batch)

        self.add_task_btn = pyglet.shapes.Rectangle(ADD_ICON_COORDS[0],
ADD_ICON_COORDS[1], color=CHRISTMAS_GREEN_3, width=ADD_ICON_SIZE,
height=ADD_ICON_SIZE)

        self.task_btn_icon = pyglet.text.Label('+',x=ADD_ICON_COORDS[0]+12,
            y=ADD_ICON_COORDS[1]+11 ,bold=True, color=BLACK, font_size=20)

        self.task = TextWidget('Enter taskname', 210, 310,
130, self.batch)
        self.task_description = TextWidget('Description', 155, 240,
                    250,  self.batch)
        self.tab_group = [self.task,self.task_description]

        self.text_cursor = self.get_system_mouse_cursor('text')

        self.focus = None
        self.set_focus(self.task_description)
        # self.push_handlers(event_logger)


    def on_draw(self):
        pyglet.gl.glClearColor(1, 1, 1, 1)
        self.clear()
        self.batch.draw()
        self.add_task_btn.draw()
        self.task_btn_icon.draw()

    def on_mouse_motion(self, x, y, dx, dy):
            if self.task.hit_test(x, y):
                self.set_mouse_cursor(self.text_cursor)

            elif self.task_description.hit_test(x, y):
                self.set_mouse_cursor(self.text_cursor)
            else:
                self.set_mouse_cursor(None)

            if hit_test(self.add_task_btn, x, y):
                self.add_task_btn.color = ICON_BOX_COLOR_HOVER
            else:
                self.add_task_btn.color = ICON_BOX_COLOR

    def on_mouse_press(self, x, y, button, modifiers):
        description = ''

        if self.task.hit_test(x, y):
            self.set_focus(self.task)

        elif self.task_description.hit_test(x, y):
            self.set_focus(self.task_description)

        elif hit_test(self.add_task_btn, x,y):
            send_to_main_window(self.task.document.text,
                                self.task_description.document.text)
            new_task_info(self.task.document.text,
                                self.task_description.document.text)
            retrieve_tasks()
            self.close()

        else:
            self.set_focus(None)

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

        #Switches from name box to description box
        if symbol == pyglet.window.key.TAB:
            if self.focus == self.tab_group[0]:
                self.set_focus(self.task_description)
                return
            else:
                self.set_focus(self.task)
                return

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


class TaskDescription(pyglet.window.Window):

    def __init__(self,task_description,x,y):
        super().__init__(300,200, caption="Description")
        self.set_location(x+60,y+120)
        self.task_description = task_description

        self.greeting_label = pyglet.text.Label(self.task_description,
            x=10, y=self.height-15, bold=True, color=BLACK)

    def on_draw(self):
        pyglet.gl.glClearColor(1, 1, 1, 1)
        self.clear()
        self.greeting_label.draw()

######  End of window classes^^^^^ #########

###  Rectangle object goes with the TextWidget class
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

    def hit_test(self, x, y):
        return (0 < x - self.layout.x < self.layout.width and
                0 < y - self.layout.y < self.layout.height)


class Rectangle(object):
    '''Draws a rectangle into a batch.'''
    def __init__(self, x1, y1, x2, y2, batch):
        self.vertex_list = batch.add(4, pyglet.gl.GL_QUADS, None,
            ('v2i', [x1, y1, x2, y1, x2, y2, x1, y2]),
            ('c4B', [200, 200, 220, 255] * 4)
        )


# class TaskBox(object):
#     def __init__(self,label,x,y):
#         self.win_size = window.get_size()
#         self.label = label
#         self.x = x
#         self.y = y
#         self.color = TASK_BX_COLOR
#
#
#     def draw_task_box(self):
#         self.task = pyglet.shapes.Rectangle(x=self.x,y=self.y,
#               width=TASK_BX_WIDTH,height=TASK_BX_HEIGHT,color = self.color)
#
#         self.title = pyglet.text.Label(self.label, x=self.task.position[0]+20,
#                                     y=self.task.position[1]+20)
#         self.task.draw()
#         self.title.draw()
#
#
#     def add_info(self,description):
#         print(description)
#         print(self.label)
#         pass
#
#
#     def isOver(self,pos):
#         if pos[0] > self.x and pos[0] < self.x + TASK_BX_WIDTH:
#             if pos[1] > self.y and pos[1] < self.y + TASK_BX_HEIGHT:
#                 return True
#
#
#     def time_adjuster(self,time):
#         pass

def send_to_main_window(task_name, description):
    this1.render_new_task(task_name, description)

def hit_test(obj, x, y):
    return (0 < x - obj.x < obj.width and 0 < y - obj.y < obj.height)


create_database()
this1 = Window(WNDW_WIDTH,WNDW_HEIGHT,"TaskTrack")
this1.retrieve_saved_tasks()
pyglet.app.run()
