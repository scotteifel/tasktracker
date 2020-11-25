import pyglet
import time
import threading
from pyglet.window import mouse, key
from create_db import create_database
from db_functions import *
from constants import *

global TIMER
global handlers_on
##EVENT LOGGER CODE
event_logger = pyglet.window.event.WindowEventLogger()
##Change to True to see the events of the different windows in the console.
handlers_on = False


class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super(Window,self).__init__(*args, **kwargs)
        if handlers_on == True:
            self.push_handlers(event_logger)

        self.set_location(S_WIDTH//2-120,S_HEIGHT//3)

        ##Counts the amount of time spent on the project so far.
        proj_time = str(retrieve_project_time())
        pyglet.clock.schedule_interval(
                            display_project_time, 60)
        ##

        self.task_list = []
        self.task_grid_x = int(50)
        self.task_grid_y = int(self.height-210)
        #var used to make sure only one description window can open
        self.description_window_open = False
        self.add_task_window_open = False
        self.task_item = 0
        self.focus = None

        self.main_batch = pyglet.graphics.Batch()
        self.background = pyglet.graphics.OrderedGroup(0)
        self.foreground = pyglet.graphics.OrderedGroup(1)

        self.greeting_label = pyglet.text.Label(
                                            GREETING_TEXT,
                                            x=50,
                                            y=WNDW_HEIGHT-40,
                                            bold=True,
                                            color=BLACK,
                                            batch = self.main_batch,
                                            group = self.foreground)

        self.project_time_count = pyglet.text.Label(
                                                proj_time,
                                                x=120,
                                                y=WNDW_HEIGHT-115,
                                                bold=True,
                                                color=BLACK,
                                                batch = self.main_batch,
                                                group = self.foreground)

        self.project_time_label = pyglet.text.Label(
                                                'Total Project Time',
                                                x=50,
                                                y=WNDW_HEIGHT-90,
                                                bold=True,
                                                color=BLACK,
                                                batch = self.main_batch,
                                                group = self.foreground)

        self.add_task_btn = pyglet.shapes.Rectangle(
                                            x=ADD_ICON_COORDS[0],
                                            y=ADD_ICON_COORDS[1],
                                            width=ADD_ICON_SIZE,
                                            height=ADD_ICON_SIZE,
                                            color=ICON_BOX_COLOR,
                                            batch = self.main_batch,
                                            group = self.background)

        self.add_task = pyglet.text.Label(
                                    '+',
                                    x=ADD_ICON_COORDS[0]+12,
                                    y=ADD_ICON_COORDS[1]+11,
                                    bold=True,
                                    color=BLACK,
                                    font_size=20,
                                    batch = self.main_batch,
                                    group = self.foreground)

        self.completed_tab_box = pyglet.shapes.Rectangle(
                                            x=WNDW_WIDTH-175,
                                            y=WNDW_HEIGHT-118,
                                            width=120,
                                            height=30,
                                            color=(252,194,0),
                                            batch = self.main_batch,
                                            group = self.background)

        self.completed_tab = pyglet.text.Label(
                                    'Completed',
                                    x=WNDW_WIDTH-170,
                                    y=WNDW_HEIGHT-115,
                                    bold=True,
                                    color=BLACK,
                                    font_size=16,
                                    batch = self.main_batch,
                                    group = self.foreground)

    def on_draw(self):
        pyglet.gl.glClearColor(1, 1, 1, 1)
        self.clear()
        self.main_batch.draw()

    def on_mouse_motion(self, x,y,dx,dy):
        #Change "+" button color on hover
        if hit_test(self.add_task_btn, x, y):
                self.add_task_btn.color = ICON_BOX_COLOR_HOVER
        else:
                self.add_task_btn.color = ICON_BOX_COLOR

        if hit_test(self.completed_tab_box, x, y):
            if retrieve_completions():
                    self.completed_tab_box.color = ICON_BOX_COLOR_HOVER
            elif retrieve_completions():
                    self.completed_tab_box.color = (252,194,0)

        if self.task_list:
            for item in self.task_list:
                if hit_test(item["task_label_box"], x, y):
                    item["task_label_box"].color = TASK_BTN_COLOR_HOVER
                else:
                    item["task_label_box"].color = TASK_BTN_COLOR

                if hit_test(item["start_timer_box"], x, y) and \
                                int(item["task_time"].text) != 0:
                    item["start_timer_box"].color = TASK_BTN_COLOR_HOVER

                else:
                    item["start_timer_box"].color = GREY_3

                if hit_test(item["edit_box"], x, y):
                    item["edit_box"].color = LIGHTSABER_GREEN_3
                else:
                    item["edit_box"].color = GREY_3

                if hit_test(item["delete_x_box"], x ,y):
                    item["delete_x_box"].color = RED_3
                else:
                    item["delete_x_box"].color = GREY_3

    def on_mouse_press(self, x, y, button, modifiers):

        if button == mouse.LEFT:
            if hit_test(self.add_task_btn, x, y):
                AddTaskWindow(
                              WNDW_WIDTH//2,
                              WNDW_HEIGHT//2,
                              timer_amount = 0,
                              task_text = 'Enter Task Name',
                              task_description = 'Enter task description')

            elif hit_test(self.completed_tab_box, x, y):
                x,y = self.get_location()
                if retrieve_completions():
                    completed_win = CompletedWindow(x, y)

            if self.task_list:
                #item_index used to match db result with self.task_list place
                item_index = 0

                for item in self.task_list:
                    if hit_test(item["task_label_box"], x, y):
                        if self.description_window_open == True:
                            return
                        else:
                            info=retrieve_description(item["task_label"].text)
                            x,y = self.get_location()
                            print(info)
                            self.description_window_open = TaskDescription(
                                                            info[0], x, y)
                            return

                    elif hit_test(item["start_timer_box"], x, y):
                        global TIMER

                        if item["start"].text == "Start":
                            TIMER = int(item["task_time"].text)
                            if TIMER == 0:
                                return

                            item["task_time"].text = str(TIMER-1)
                            item["task_time_box"].color = LIGHTSABER_GREEN_3
                            pyglet.clock.schedule_interval(
                                                            countdown,
                                                            60,
                                                            item,
                                                            item_index)
                            item["start"].text = "Stop"
                            return
                        else:
                            item["start"].text = "Start"
                            pyglet.clock.unschedule(countdown)
                            item["task_time_box"].color = GREY_3
                            return

                    elif hit_test(item["edit_box"], x, y):
                        print(self.add_task_window_open)
                        if self.add_task_window_open == True:
                            return
                        self.edit_task(item["task_label"].text)
                        return

                    elif hit_test(item["delete_x_box"], x, y):

                        # delete_task(item["task_label"].document.text)
                        remove_task(item)
                        return

                    item_index += 1

                    try:
                        if hit_test(item["check_box"], x, y):
                            x,y = self.get_location()
                            #Add additional notes option
                            notes_window = AddNotesWindow(x, y, item)
                            #Get the items description from the database
                            description=retrieve_description(
                                                    item["task_label"].text)[0]
                            add_completed_task(item["task_label"].text,
                                               description,
                                               int(item["task_time"].text),
                                               4444,
                                               1,
                                               'placeholder note')
                            print("Right above retrieve completions")
                            retrieve_completions()
                            delete_task(item["task_label"].document.text)
                            remove_task(item)
                    except:
                        pass

    def on_close(self):
        proj_time = retrieve_project_time()

        ## Keeping track of the total project time through a text file
        ## so if the database has to be deleted for debugging or updating
        ## it won't erase the info of the total time spent on the project.
        with open('records.txt', 'a+') as file:
            file.seek(0)
            inf = file.read()
            if not inf:
                contents = 0
            else:
                contents = int(inf)
            if contents != 0:
                if proj_time >= contents:
                    new_file_info = str(proj_time + (proj_time - contents))
                else:
                    new_file_info = str(proj_time + contents)
            else:
                new_file_info = str(proj_time)

        with open('records.txt', 'w') as file:
            file.write(new_file_info)

        self.close()

    def retrieve_saved_tasks(self):
        #If statement will clean up the gui screen before tasks are drawn
        #or redrawn
        if len(self.task_list) != 0:
            for item in self.task_list:
                redraw_all_tasks(item)

        self.task_list = []
        self.task_grid_x = int(50)
        self.task_grid_y = int(self.height-210)

        tasks = retrieve_tasks()
        if tasks:
            for item in tasks:
                self.render_new_task(item[0],item[1],item[2])

    def edit_task(self, task):

        info = retrieve_task_info(task)
        description_window = AddTaskWindow(
                              WNDW_WIDTH//2,
                              WNDW_HEIGHT//2,
                              timer_amount = info[2],
                              task_text = info[0],
                              task_description = info[1])

    def show_completed_tasks(self, item, item_index):

        self.check = pyglet.text.Label(
                                     "!",
                                     x = item["task_label_box"].x + 4,
                                     y = item["task_label_box"].y - 23,
                                     bold=True,
                                     color=BLACK,
                                     batch=self.main_batch,
                                     group=self.foreground)

        self.check_box = pyglet.shapes.Rectangle(
                                     item["task_label_box"].x + 1,
                                     item["task_label_box"].y - 25,
                                     width=14,
                                     height=14,
                                     color=LIGHTSABER_GREEN_3,
                                     batch=self.main_batch,
                                     group=self.background)

        self.task_list[item_index]["check"] = self.check
        self.task_list[item_index]["check_box"] = self.check_box

    #Renders a new task.
    def render_new_task(self, task, description, timer):

        self.task_label = pyglet.text.Label(
                                     task,
                                     x = self.task_grid_x + 4,
                                     y = self.task_grid_y + 5,
                                     bold=True,
                                     color=BLACK,
                                     batch=self.main_batch,
                                     group=self.foreground)

        ##Task description box
        self.task_label_box = pyglet.shapes.Rectangle(
                                     self.task_grid_x,
                                     self.task_grid_y,
                                     width=150,height=30,
                                     color=TASK_BTN_COLOR,
                                     batch=self.main_batch,
                                     group=self.background)

        ## Time count
        self.task_time = pyglet.text.Label(
                                     str(timer),
                                     x = self.task_grid_x+30,
                                     y = self.task_grid_y-27,
                                     bold = True,
                                     color = BLACK,
                                     batch = self.main_batch,
                                     group = self.foreground)

        ##Box for time countdown
        self.task_time_box = pyglet.shapes.Rectangle(
                                      self.task_grid_x+24,
                                      self.task_grid_y-32,
                                      width = 30,
                                      height = 23,
                                      color = GREY_3,
                                      batch=self.main_batch,
                                      group = self.background)

        self.start = pyglet.text.Label(
                                     'Start',
                                     x = self.task_grid_x+73,
                                     y = self.task_grid_y-28,
                                     bold=True,
                                     color=BLACK,
                                     batch = self.main_batch,
                                     group = self.foreground)

        ##Box pressed to start timer
        self.start_timer_box = pyglet.shapes.Rectangle(
                                     self.task_grid_x+70,
                                     self.task_grid_y-30,
                                     width = 50,
                                     height = 18,
                                     color = GREY_3,
                                     batch=self.main_batch,
                                     group = self.background)

        self.delete_x = pyglet.text.Label(
                                     'x',
                                     x = self.task_grid_x+143,
                                     y = self.task_grid_y-16,
                                     bold=True,
                                     color=BLACK,
                                     batch = self.main_batch,
                                     group = self.foreground)

        self.delete_x_box = pyglet.shapes.Rectangle(
                                     self.task_grid_x+140,
                                     self.task_grid_y-18,
                                     width = 14,
                                     height = 14,
                                     color = GREY_3,
                                     batch=self.main_batch,
                                     group = self.background)

        self.edit = pyglet.text.Label(
                                     '...',
                                     x = self.task_grid_x+135,
                                     y = self.task_grid_y-29,
                                     bold=True,
                                     color=BLACK,
                                     batch = self.main_batch,
                                     group = self.foreground)

        self.edit_box = pyglet.shapes.Rectangle(
                                     self.task_grid_x+133,
                                     self.task_grid_y-33,
                                     width = 18,
                                     height = 12,
                                     color = GREY_3,
                                     batch=self.main_batch,
                                     group = self.background)

        self.task_list.append({"task_label" : self.task_label,
                               "task_label_box" : self.task_label_box,
                               "task_time" : self.task_time,
                               "task_time_box" : self.task_time_box,
                               "start" : self.start,
                               "start_timer_box" : self.start_timer_box,
                               "delete_x" : self.delete_x,
                               "delete_x_box" : self.delete_x_box,
                               "edit" : self.edit,
                               "edit_box" : self.edit_box})

        ## Places new tasks on grid plane
        if self.task_grid_y > 90:
            self.task_grid_y -= 90
            return
        else:
            self.task_grid_y = int(self.height-210)
            self.task_grid_x += 160


class AddTaskWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(550, 450, caption='ADD TASK')
        self.set_location(S_WIDTH//2-160,S_HEIGHT//3-30)
        if handlers_on == True:
            self.push_handlers(event_logger)

        self.main_batch = pyglet.graphics.Batch()
        self.background = pyglet.graphics.OrderedGroup(0)
        self.foreground = pyglet.graphics.OrderedGroup(1)
        main_window.add_task_window_open = True

        self.greeting_label = pyglet.text.Label(
                                            "Enter task information",
                                            x=185,
                                            y=self.height-40,
                                            bold=True,
                                            color=BLACK,
                                            batch = self.main_batch,
                                            group = self.foreground)

        self.add_task_btn = pyglet.shapes.Rectangle(
                                            (self.width//2)-10,
                                            self.height-100,
                                            color=CHRISTMAS_GREEN_3,
                                            width=ADD_ICON_SIZE,
                                            height=ADD_ICON_SIZE,
                                            batch = self.main_batch,
                                            group = self.background)

        self.add_task = pyglet.text.Label(
                                    '+',
                                    x=self.width//2,
                                    y=self.height-91,
                                    bold=True,
                                    color=BLACK,
                                    font_size=20,
                                    batch = self.main_batch,
                                    group = self.foreground)

        self.minutes_label = pyglet.text.Label(
                                            "Minute total",
                                            x=self.width//2-40,
                                            y=self.height-133,
                                            bold=True,
                                            color=BLACK,
                                            batch = self.main_batch,
                                            group = self.foreground)

        self.timer = TextWidget(
                        str(kwargs["timer_amount"]),
                        self.width//2-5,
                        self.height-200,
                        35,
                        self.main_batch,
                        self.foreground)

        self.timer_box = pyglet.shapes.Rectangle(
                                      self.width//2-9,
                                      self.height-167,
                                      width = 35,
                                      height = 25,
                                      color = GREY_3,
                                      batch=self.main_batch,
                                      group = self.background)

        self.task = TextWidget(
                       kwargs["task_text"],
                       self.width//2-45,
                       self.height-250,
                       90,
                       self.main_batch,
                       self.foreground)

        self.task_box = pyglet.shapes.Rectangle(
                                       self.width//2-48,
                                       self.height-250,
                                       width = 110,
                                       height = 60,
                                       color = GREY_3,
                                       batch=self.main_batch,
                                       group = self.background
                                       )

        self.task_description = TextWidget(
                                   kwargs["task_description"],
                                   self.width//2-120,
                                   self.height-340,
                                   240,
                                   self.main_batch,
                                   self.foreground)

        self.description_box = pyglet.shapes.Rectangle(
                                              self.width//2-123,
                                              self.height-350,
                                              width = 260,
                                              height = 70,
                                              color = GREY_3,
                                              batch=self.main_batch,
                                              group = self.background
                                              )

        self.tab_group = [self.timer, self.task, self.task_description]

        self.text_cursor = self.get_system_mouse_cursor('text')
        self.focus = None
        self.set_focus(self.timer)

    def on_draw(self):
        pyglet.gl.glClearColor(1, 1, 1, 1)
        self.clear()
        self.main_batch.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        ##Shows the text_cursor when hovering over these boxes
        if hit_test(self.timer_box, x, y):
            self.set_mouse_cursor(self.text_cursor)

        elif hit_test(self.description_box, x, y):
            self.set_mouse_cursor(self.text_cursor)

        elif hit_test(self.task_box, x, y):
            self.set_mouse_cursor(self.text_cursor)

        else:
            self.set_mouse_cursor(None)

        if hit_test(self.add_task_btn, x, y):
            self.add_task_btn.color = ICON_BOX_COLOR_HOVER
        else:
            self.add_task_btn.color = ICON_BOX_COLOR

    def on_mouse_press(self, x, y, button, modifiers):
        if hit_test(self.task_box, x, y):
            self.set_focus(self.task)

        elif hit_test(self.description_box, x, y):
            self.set_focus(self.task_description)

        elif hit_test(self.timer_box, x, y):
            self.set_focus(self.timer)

        elif hit_test(self.add_task_btn, x,y):

            db_check = new_task_info(self.task.document.text,
                                 self.task_description.document.text,
                                 self.timer.document.text)
            if db_check == True:
                main_window.retrieve_saved_tasks()

            else:
                send_to_main_window(self.task.document.text,
                                    self.task_description.document.text,
                                    self.timer.document.text)

                retrieve_tasks()

            main_window.add_task_window_open = False
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

        #Switch from name box to description box
        if symbol == pyglet.window.key.TAB:
            if self.focus == self.tab_group[0]:
                self.set_focus(self.tab_group[1])

            elif self.focus == self.tab_group[1]:
                self.set_focus(self.tab_group[2])

            else:
                self.set_focus(self.tab_group[0])

        if symbol == pyglet.window.key.ESCAPE:
            pyglet.app.exit()

    def on_close(self):
        main_window.add_task_window_open = False
        self.close()

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
        if handlers_on == True:
            self.push_handlers(event_logger)
        self.task_description = task_description

        self.greeting_label = pyglet.text.Label(self.task_description,
                        x=10, y=self.height-15, bold=True,
                        multiline = True, width = 280, color=BLACK)

    def on_draw(self):
        pyglet.gl.glClearColor(1, 1, 1, 1)
        self.clear()
        self.greeting_label.draw()

    #This ensures when a task button is pressed only one window can open
    def on_close(self):
        main_window.description_window_open = False
        self.close()


##Window to show the comleted tasks listed.
class CompletedWindow(pyglet.window.Window):
    def __init__(self, x, y):
        super().__init__(700, 600, caption = "Completed tasks")
        self.set_location(x + 60, y + 120)
        if handlers_on == True:
            self.push_handlers(event_logger)

        self.main_batch = pyglet.graphics.Batch()
        self.background = pyglet.graphics.OrderedGroup(0)
        self.foreground = pyglet.graphics.OrderedGroup(1)

        self.x_offset = 25
        self.y_offset = 480

        self.greeting_label = pyglet.text.Label('Completed Tasks',
                        x=180, y=self.height-20, bold=True,
                        multiline=True, width=280, color=BLACK)

        info = retrieve_completions()

        for item in info:

            self.task_name_intro = pyglet.text.Label(
                                        'Name: ',
                                        x=self.x_offset+5,
                                        y=self.y_offset+40,
                                        bold=True,
                                        color=BLACK,
                                        batch = self.main_batch,
                                        group = self.foreground
                                        )

            self.task_name = pyglet.text.Label(
                                        item[0],
                                        x=self.x_offset+120,
                                        y=self.y_offset+40,
                                        bold=True,
                                        color=BLACK,
                                        batch = self.main_batch,
                                        group = self.foreground
                                        )

            self.task_time_info_intro = pyglet.text.Label(
                                        "Time Info: ",
                                        x=self.x_offset+5,
                                        y=self.y_offset+20,
                                        bold=True,
                                        color=BLACK,
                                        batch = self.main_batch,
                                        group = self.foreground
                                        )

            self.task_time_info = pyglet.text.Label(
                                        str(item[2]),
                                        x=self.x_offset+120,
                                        y=self.y_offset+20,
                                        bold=True,
                                        color=BLACK,
                                        batch = self.main_batch,
                                        group = self.foreground
                                        )

            self.task_description_intro = pyglet.text.Label(
                                        'Description: ',
                                        x=self.x_offset+5,
                                        y=self.y_offset+5,
                                        bold=True,
                                        color=BLACK,
                                        batch = self.main_batch,
                                        group = self.foreground
                                        )

            self.task_description = pyglet.text.Label(
                                        item[1],
                                        x=self.x_offset+120,
                                        y=self.y_offset+5,
                                        bold=True,
                                        color=BLACK,
                                        batch = self.main_batch,
                                        group = self.foreground
                                        )

            self.y_offset -= 80
            if self.y_offset < 80:
                self.x_offset += 70
                self.y_offset = 480

    def on_draw(self):
        pyglet.gl.glClearColor(1, 1, 1, 1)
        self.clear()
        self.greeting_label.draw()
        self.main_batch.draw()


class AddNotesWindow(pyglet.window.Window):
    def __init__(self, x, y, item):
        super().__init__(500, 400, caption = "Task Summary")
        self.set_location(x + 60, y + 120)
        if handlers_on == True:
            self.push_handlers(event_logger)

        self.main_batch = pyglet.graphics.Batch()
        self.background = pyglet.graphics.OrderedGroup(0)
        self.foreground = pyglet.graphics.OrderedGroup(1)

        label_text = "Add any notes about the completed task?"
        self.greeting_label = pyglet.text.Label(label_text,
                        x=10, y=self.height-15, bold=True,
                        multiline=True, width=280, color=BLACK,
                        batch=self.main_batch)

        self.add_task_btn = pyglet.shapes.Rectangle(
                                            x=28,
                                            y=8,
                                            width=ADD_ICON_SIZE,
                                            height=ADD_ICON_SIZE,
                                            color=ICON_BOX_COLOR,
                                            batch = self.main_batch,
                                            group = self.background)

        self.add_task = pyglet.text.Label(
                                    '+',
                                    x=30,
                                    y=10,
                                    bold=True,
                                    color=BLACK,
                                    font_size=20,
                                    batch = self.main_batch,
                                    group = self.foreground)

        self.add_note_box = pyglet.shapes.Rectangle(
                                      50,
                                      52,
                                      width = 30,
                                      height = 25,
                                      color = GREY_3,
                                      batch=self.main_batch,
                                      group = self.background
                                      )

        self.add_note = TextWidget(
                                "Add Note",
                                52,
                                52,
                                35,
                                self.main_batch,
                                self.foreground)



        self.focus = None
        self.set_focus(self.add_note)




    def on_draw(self):
        pyglet.gl.glClearColor(1, 1, 1, 1)
        self.clear()
        self.main_batch.draw()

    def set_focus(self, focus):
        if self.focus:
            self.focus.caret.visible = False
            self.focus.caret.mark = self.focus.caret.position = 0

        self.focus = focus
        if self.focus:
            self.focus.caret.visible = True
            self.focus.caret.mark = 0
            self.focus.caret.position = len(self.focus.document.text)

######  End of window classes^^^^^ #########


class TextWidget(object):
    def __init__(self, text, x, y, width, main_batch ,
                foreground ,height = None):
        self.document = pyglet.text.document.UnformattedDocument(text)
        self.document.set_style(0, len(self.document.text),
                                dict(color=(0, 0, 0, 255)))
        self.main_batch = main_batch
        self.foreground = foreground
        self.text = text

        font = self.document.get_font()

        if height:
            pass
        else:
            height = font.ascent - font.descent

        self.layout = pyglet.text.layout.IncrementalTextLayout(
                                                self.document,
                                                width,
                                                height*3,
                                                multiline=True,
                                                wrap_lines=True,
                                                batch=self.main_batch,
                                                group=self.foreground)
        self.caret = pyglet.text.caret.Caret(self.layout)

        self.layout.x = x
        self.layout.y = y


def send_to_main_window(task_name, description, timer):
    main_window.render_new_task(task_name, description,timer)


def hit_test(obj, x, y):
    return (0 < x - obj.x < obj.width and 0 < y - obj.y < obj.height)


def redraw_all_tasks(task):
    for item in task.values():
        item.delete()


def remove_task(task):
    for item in task.values():
        item.delete()

    delete_task(task["task_label"].text)

    main_window.task_list.remove(task)
    main_window.retrieve_saved_tasks()


def countdown(dt, item, item_index):
    global TIMER

    if TIMER == 0:
        pyglet.clock.unschedule(countdown)
        main_window.show_completed_tasks(item, item_index)

    else:
        TIMER -= 1
        item["task_time"].text = ""
        item["task_time"].text = str(TIMER)
        update_timer(TIMER, item["task_label"].text)

def display_project_time(dt):
    new_time = run_project_timer()
    main_window.project_time_count.text = str(new_time)


create_database()
main_window = Window(WNDW_WIDTH,WNDW_HEIGHT,"TaskTrack")
main_window.retrieve_saved_tasks()
pyglet.app.run()
