import pyglet
import time
import threading
from pyglet.window import mouse, key
from create_db import db_startup
from db_functions import *
from constants import *

global TIMER
global handlers_on
##EVENT LOGGER CODE
event_logger = pyglet.window.event.WindowEventLogger()
##Change to True to see the events of the different windows in the console.
handlers_on = False

# 'Canvas not attached' bug fix \Lib\site-packages\pyglet\gl\base.py
# lines 306 and 328 were changed.  now has a self.is_ok var
# Bug happened sometimes when a window opened.  Didn't allow mouse events.

class Home_Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super(Home_Window,self).__init__(*args, **kwargs)
        if handlers_on == True:
            self.push_handlers(event_logger)

        self.set_location(S_WIDTH//2-120,S_HEIGHT//3)

        ##Counts the amount of time spent on the project so far.
        proj_time = str(retrieve_project_time())
        pyglet.clock.schedule_interval(
                            display_project_time, 60)

        self.task_list = []
        self.task_grid_x = int(50)
        self.task_grid_y = int(self.height-210)
        # Vars used to make sure only one window can open and for canvas
        # error check
        self.description_window_open = False
        self.add_task_window_open = False
        self.completed_window_open = False
        self.notes_window_open = False

        self.rndrd_task_count = 0
        self.task_item = 0
        self.confirm = False
        #Enables hovering of ! box to return to grey after the mouse is moved
        #off if that's the color it started as
        self.orig_check_box_color = GREY_3

        self.focus = None
        self.main_batch = pyglet.graphics.Batch()
        self.background = pyglet.graphics.OrderedGroup(0)
        self.foreground = pyglet.graphics.OrderedGroup(1)
        self.retrieve_saved_tasks()

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
                                    y=ADD_ICON_COORDS[1]+10,
                                    bold=True,
                                    color=BLACK,
                                    font_size=20,
                                    batch = self.main_batch,
                                    group = self.foreground)

        self.completed_tab_btn = pyglet.shapes.Rectangle(
                                            x=WNDW_WIDTH-175,
                                            y=WNDW_HEIGHT-118,
                                            width=120,
                                            height=30,
                                            color=ORANGE_3,
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

        self.end_project = pyglet.text.Label(
                                    'Finish Project',
                                    x=WNDW_WIDTH-159,
                                    y=5,
                                    bold=True,
                                    color=BLACK,
                                    font_size=16,
                                    batch = self.main_batch,
                                    group = self.foreground)
        self.end_project_btn = pyglet.shapes.Rectangle(
                                            x=WNDW_WIDTH-165,
                                            y=3,
                                            width=160,
                                            height=27,
                                            color=DODGER_BLUE_3,
                                            batch = self.main_batch,
                                            group = self.background)



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

        if hit_test(self.completed_tab_btn, x, y):

            self.completed_tab_btn.color = ICON_BOX_COLOR_HOVER
        else:
            self.completed_tab_btn.color = (252,194,0)

        if hit_test(self.end_project_btn, x, y):
            self.end_project_btn.color = RED_3
        else:
            self.end_project_btn.color = DODGER_BLUE_3

        try:
            if hit_test(self.yes_btn, x, y):
                self.yes_btn.color = LIGHTSABER_GREEN_3
            else:
                self.yes_btn.color = DODGER_BLUE_3

            if hit_test(self.no_btn, x, y):
                self.no_btn.color = RED_3
            else:
                self.no_btn.color = DODGER_BLUE_3
        except:
            pass

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

                #Checks to see if the tasks timer is already up, if so
                #this if statement keeps the box's color green
                if item["check_box"].color == LIGHTSABER_GREEN_3:
                    continue
                elif hit_test(item["check_box"], x, y):
                    item["check_box"].color = LIGHTSABER_GREEN_3
                else:
                    item["check_box"].color = GREY_3


    def on_mouse_press(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            if hit_test(self.add_task_btn, x, y):
                if self.rndrd_task_count == 10:
                    return
                else:
                    AddTaskWindow(
                                  WNDW_WIDTH//2,
                                  WNDW_HEIGHT//2,
                                  timer_amount = 0,
                                  task_text = 'Enter Task Name',
                                  task_description = 'Enter task description')

            elif hit_test(self.completed_tab_btn, x, y):
                if self.completed_window_open == True:
                    return

                elif retrieve_completions():
                    self.completed_win = Completed_Window(430,700,
                                "Completed Tasks",visible=False)

            elif hit_test(self.end_project_btn, x, y):
                try:
                    if self.finish_prompt.document.text == '':
                        self.confirm_end()
                    else:
                        return
                except:
                    self.confirm_end()

            try:
                if hit_test(self.yes_btn, x, y):
                    if self.confirm == True:
                        self.final_confirmation()
                    else:
                        self.yes_confirm()
                elif hit_test(self.no_btn, x, y):
                    self.no_confirm()
            except:
                pass


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
                            self.description_window_open = True
                            InfoWindow(info[0], x, y,
                                            caption = 'Description')
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
                        if self.add_task_window_open == True:
                            return
                        self.edit_task(item["task_label"].text)
                        return

                    elif hit_test(item["delete_x_box"], x, y):
                        #Resetting rendered task list for a fresh count
                        self.rndrd_task_count = 0
                        remove_task(item)
                        return

                    item_index += 1

                    try:
                        if hit_test(item["check_box"], x, y):
                            x,y = self.get_location()
                            #Add additional notes window
                            self.notes_window = AddNotesWindow(x, y, item)
                    except:
                        pass


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
                self.render_new_task(item[0],item[1])


    def edit_task(self, task):

        info = retrieve_task_info(task)
        description_window = AddTaskWindow(
                              WNDW_WIDTH//2,
                              WNDW_HEIGHT//2,
                              timer_amount = info[2],
                              task_text = info[0],
                              task_description = info[1])

    def confirm_end(self):

        prompt = 'Save the completions tab to the desktop \
and start a new project?'
        self.finish_prompt = TextWidget(
                       prompt,
                       WNDW_WIDTH-163,
                       30,
                       160,
                       self.main_batch,
                       self.foreground,
                       )
        self.finish_prompt.document.set_style(0,30, dict(font_size=11))
        self.finish_prompt.caret.visible = False

        self.yes = pyglet.text.Label(
                                    'Yes',
                                    x=WNDW_WIDTH-155,
                                    y=85,
                                    bold=True,
                                    color=BLACK,
                                    font_size=13,
                                    batch = self.main_batch,
                                    group = self.foreground)

        self.yes_btn = pyglet.shapes.Rectangle(
                                        x=WNDW_WIDTH-160,
                                        y=83,
                                        width=50,
                                        height=20,
                                        color=DODGER_BLUE_3,
                                        batch = self.main_batch,
                                        group = self.background)


        self.no = pyglet.text.Label(
                                    'No',
                                    x=WNDW_WIDTH-65,
                                    y=85,
                                    bold=True,
                                    color=BLACK,
                                    font_size=11,
                                    batch = self.main_batch,
                                    group = self.foreground)

        self.no_btn = pyglet.shapes.Rectangle(
                                            x=WNDW_WIDTH-70,
                                            y=83,
                                            width=50,
                                            height=20,
                                            color=DODGER_BLUE_3,
                                            batch = self.main_batch,
                                            group = self.background)

    def yes_confirm(self):
        #Give the user one more opportunity to continue their project.
        self.confirm = True
        self.finish_prompt.caret.delete()
        self.finish_prompt.document.text = "Are you sure you want to \
end this current project?"


    def no_confirm(self):
        self.confirm = False
        self.yes_btn.delete()
        self.yes.delete()
        self.no_btn.delete()
        self.no.delete()
        self.finish_prompt.document.text = ''
        self.finish_prompt.caret.delete()


    def final_confirmation(self):
        print("final confirmation")
        pass


    def render_new_task(self, task, timer):
        self.rndrd_task_count += 1
        #Makes the selection box taller to fit in a longer name if nessecary

        if len(task) > 15:
            #Checks if a task is the first on a new line and lowers it if so.
            if self.task_grid_y == int(self.height-210):
                self.task_grid_y -= 20
                task_label_y = self.task_grid_y + 24

            else:
                task_label_y = self.task_grid_y + 24
            task_label_box_height = 43

        else:
            task_label_y = self.task_grid_y + 5
            task_label_box_height = 23

        self.task_label = pyglet.text.Label(
                                     task,
                                     x = self.task_grid_x + 4,
                                     y = task_label_y,
                                     width = 150,
                                     multiline = True,
                                     bold=True,
                                     color=BLACK,
                                     batch=self.main_batch,
                                     group=self.foreground)

        ##Click this for the task description
        self.task_label_box = pyglet.shapes.Rectangle(
                                     self.task_grid_x,
                                     self.task_grid_y,
                                     width=150,
                                     height=task_label_box_height,
                                     color=TASK_BTN_COLOR,
                                     batch=self.main_batch,
                                     group=self.background)

        ## Time count
        self.task_time = pyglet.text.Label(
                                     str(timer),
                                     x = self.task_grid_x+33,
                                     y = self.task_grid_y-24,
                                     bold = True,
                                     color = BLACK,
                                     batch = self.main_batch,
                                     group = self.foreground)

        ##Box for time countdown
        self.task_time_box = pyglet.shapes.Rectangle(
                                      self.task_grid_x+25,
                                      self.task_grid_y-30,
                                      width = 30,
                                      height = 23,
                                      color = GREY_3,
                                      batch=self.main_batch,
                                      group = self.background)

        self.start = pyglet.text.Label(
                                     'Start',
                                     x = self.task_grid_x+70,
                                     y = self.task_grid_y-24,
                                     bold=True,
                                     color=BLACK,
                                     batch = self.main_batch,
                                     group = self.foreground)

        ##Box pressed to start timer
        self.start_timer_box = pyglet.shapes.Rectangle(
                                     self.task_grid_x+66,
                                     self.task_grid_y-28,
                                     width = 50,
                                     height = 20,
                                     color = GREY_3,
                                     batch=self.main_batch,
                                     group = self.background)

        self.delete_x = pyglet.text.Label(
                                     'x',
                                     x = self.task_grid_x+137,
                                     y = self.task_grid_y-15,
                                     bold=True,
                                     color=BLACK,
                                     batch = self.main_batch,
                                     group = self.foreground)

        self.delete_x_box = pyglet.shapes.Rectangle(
                                     self.task_grid_x+134,
                                     self.task_grid_y-17,
                                     width = 14,
                                     height = 14,
                                     color = GREY_3,
                                     batch=self.main_batch,
                                     group = self.background)

        self.edit = pyglet.text.Label(
                                     '...',
                                     x = self.task_grid_x+133,
                                     y = self.task_grid_y-28,
                                     bold=True,
                                     color=BLACK,
                                     batch = self.main_batch,
                                     group = self.foreground)

        self.edit_box = pyglet.shapes.Rectangle(
                                     self.task_grid_x+131,
                                     self.task_grid_y-32,
                                     width = 18,
                                     height = 11,
                                     color = GREY_3,
                                     batch=self.main_batch,
                                     group = self.background)

        self.check = pyglet.text.Label(
                                     "!",
                                     x = self.task_grid_x + 6,
                                     y = self.task_grid_y - 23,
                                     bold=True,
                                     color=BLACK,
                                     batch=self.main_batch,
                                     group=self.foreground)
        #Checks to see if the task still has time remaining
        if timer == 0:
            check_box_color = LIGHTSABER_GREEN_3
        else:
            check_box_color = GREY_3

        self.check_box = pyglet.shapes.Rectangle(
                                     self.task_grid_x + 2,
                                     self.task_grid_y - 25,
                                     width=14,
                                     height=16,
                                     color=check_box_color,
                                     batch=self.main_batch,
                                     group=self.background)

        self.task_list.append({"task_label" : self.task_label,
                               "task_label_box" : self.task_label_box,
                               "task_time" : self.task_time,
                               "task_time_box" : self.task_time_box,
                               "start" : self.start,
                               "start_timer_box" : self.start_timer_box,
                               "delete_x" : self.delete_x,
                               "delete_x_box" : self.delete_x_box,
                               "edit" : self.edit,
                               "edit_box" : self.edit_box,
                               "check" : self.check,
                               "check_box" : self.check_box})

        ## Places each new task on a grid
        if self.task_grid_y > 90:
            self.task_grid_y -= 95
            return
        else:
            self.task_grid_y = int(self.height-210)
            self.task_grid_x += 160


class AddTaskWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(550, 450, caption='ADD TASK', visible=False)
        self.set_location(S_WIDTH//2-160,S_HEIGHT//3-30)
        if handlers_on == True:
            self.push_handlers(event_logger)

        self.main_batch = pyglet.graphics.Batch()
        self.background = pyglet.graphics.OrderedGroup(0)
        self.foreground = pyglet.graphics.OrderedGroup(1)
        self.crnt_task = kwargs["task_text"]

        self.greeting_label = pyglet.text.Label(
                                            "Enter task information",
                                            x = 185,
                                            y = self.height-40,
                                            bold = True,
                                            color = BLACK,
                                            batch = self.main_batch,
                                            group = self.foreground)

        self.add_task_btn = pyglet.shapes.Rectangle(
                                            (self.width//2)-10,
                                            self.height-100,
                                            color = CHRISTMAS_GREEN_3,
                                            width = ADD_ICON_SIZE,
                                            height = ADD_ICON_SIZE,
                                            batch = self.main_batch,
                                            group = self.background)

        self.add_task = pyglet.text.Label(
                                    '+',
                                    x = self.width//2,
                                    y = self.height-91,
                                    bold = True,
                                    color = BLACK,
                                    font_size = 20,
                                    batch = self.main_batch,
                                    group = self.foreground)

        self.minutes_label = pyglet.text.Label(
                                            "Minute total",
                                            x = self.width//2-40,
                                            y = self.height-133,
                                            bold = True,
                                            color = BLACK,
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
                       self.crnt_task,
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
                                       batch = self.main_batch,
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
                                              batch = self.main_batch,
                                              group = self.background
                                              )

        self.tab_group = [self.timer, self.task, self.task_description]

        self.text_cursor = self.get_system_mouse_cursor('text')
        self.focus = None
        self.set_focus(self.timer)

        main_window.add_task_window_open = True
        # Canvas not attached bug fix in \Lib\site-packages\pyglet\gl\base.py
        # lines 306 and 328 were changed.  now has a self.is_ok var
        if self.context.is_ok == 0:
            main_window.add_task_window_open = False
            self.close()
        self.set_visible()


    def invalid_entry_label(self):

            alert = pyglet.text.Label(
                            "-Invalid name",
                            x = self.width - 200,
                            y = self.height - 220,
                            bold = True,
                            color = BLACK,
                            batch = self.main_batch,
                            group = self.foreground
                            )


    def add_task_to_db(self):

            db_check = new_task_info(self.task.document.text,
                         self.task_description.document.text,
                         self.timer.document.text)
            print("db check is", db_check)
            if db_check == True:
                main_window.retrieve_saved_tasks()

            else:
                main_window.render_new_task(self.task.document.text,
                                            self.timer.document.text)

                retrieve_tasks()

            main_window.add_task_window_open = False
            self.close()


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

            if check_completed_names(self.task.document.text) == False:
                ##It equals 0 if no tasks have been added yet
                if len(main_window.task_list) != 0:
                    #Make sure the name isn't already being used by a waiting
                    #task
                    for item in main_window.task_list:
                        if item["task_label"].text == \
                        self.task.document.text and \
                        self.crnt_task != item["task_label"].text:
                            self.invalid_entry_label()
                            return
                    else:
                        self.add_task_to_db()
                else:
                        self.add_task_to_db()
            else:
                self.invalid_entry_label()
        else:
            self.set_focus(None)


    def on_text(self, text):
        if self.focus:
            #User can only enter in under 21 characters for title name
            if self.focus == self.task and len(self.task.document.text) > 20:
                return
            #User must enter a number for the time amount
            elif self.focus == self.timer and text not in ('0123456789'):
                return
            #User must keep the description under 130 characters
            elif self.focus == self.task_description and \
                           len(self.task_description.document.text) > 130:
                return
            else:
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


class Completed_Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super(Completed_Window,self).__init__(*args, **kwargs)

        x,y = main_window.get_location()
        self.set_location(x + 60, y + 120)

        if handlers_on == True:
            self.push_handlers(event_logger)

        self.main_batch = pyglet.graphics.Batch()
        self.background = pyglet.graphics.OrderedGroup(0)
        self.foreground = pyglet.graphics.OrderedGroup(1)

        main_window.completed_window_open = True
        # 'Canvas not attached' bug fix \Lib\site-packages\pyglet\gl\base.py
        # lines 306 and 328 were changed.  now has a self.is_ok var
        if self.context.is_ok == 0:
            main_window.completed_window_open = False
            self.close()


        #Makes sure the notes window is only opened once
        self.notes_window_open = False
        self.notes_box_list = []
        self.completed_tab_list = []
        self.current_row = 0

        info = retrieve_completions()
        row_counter = len(info)//4
        if 4 < len(info) < 9:
            self.width = 690

        elif row_counter == 2:
            self.width = 1020

        elif row_counter > 2:
            self.width = 1020
            self.height = 800

            self.next = pyglet.text.Label(
                                         '>>',
                                         x = self.width-110,
                                         y = self.height-40,
                                         bold=True,
                                         color=BLACK,
                                         batch = self.main_batch,
                                         group = self.foreground)

            self.next_box = pyglet.shapes.Rectangle(
                                         self.width - 117,
                                         self.height-42,
                                         width = 30,
                                         height = 16,
                                         color = GREY_3,
                                         batch=self.main_batch,
                                         group = self.background)

            self.previous = pyglet.text.Label(
                                         '<<',
                                         x = self.width - 150,
                                         y = self.height-40,
                                         bold=True,
                                         color=BLACK,
                                         batch = self.main_batch,
                                         group = self.foreground)

            self.previous_box = pyglet.shapes.Rectangle(
                                         self.width - 155,
                                         self.height-42,
                                         width = 30,
                                         height = 16,
                                         color = GREY_3,
                                         batch=self.main_batch,
                                         group = self.background)

        self.x_offset = 30
        self.y_offset = self.height - 160
        self.greeting_label = pyglet.text.Label(
                                        'Completed Tasks',
                                        x=self.width//2-50,
                                        y=self.height-37,
                                        bold=True,
                                        multiline=True,
                                        width=280,
                                        color=BLACK,
                                        batch=self.main_batch)



        if row_counter > 1:
            self.greeting_label.font_size = 16

        # self.completed_task_list = organize_completed_tab(info)
        self.completed_task_list = info
        self.delete_list = []
        self.page_number = 0
        self.task_place_counter = 0

        for item in self.completed_task_list:
            if self.current_row < 3:
                self.draw_task(item)
                self.task_place_counter += 1
            else:
                pass

        self.set_visible()

    def next_page(self):
        if self.task_place_counter == len(self.completed_task_list):
            pass
        else:
            self.page_number += 1
            self.delete_drawn_tasks()
            for item in self.completed_task_list[self.task_place_counter:]:
                if self.current_row < 4:
                    self.draw_task(item)
                    self.task_place_counter += 1
                else:
                    pass


    def previous_page(self):
        self.page_number -= 1
        self.delete_drawn_tasks()
        if self.page_number == 0:
            self.task_place_counter = 0
            for item in self.completed_task_list:
                if self.current_row < 3:
                    self.draw_task(item)
                    self.task_place_counter += 1
        else:
            num = len(self.completed_task_list) - self.task_place_counter

            for item in self.completed_task_list[num]:
                if self.current_row < 3:
                    self.draw_task(item)
                    self.task_place_counter -= 1
                else:
                    pass


#This clears all tasks so a new "page" of tasks can be drawn (back/forward)
    def delete_drawn_tasks(self):
        self.x_offset = 25
        self.y_offset = self.height - 160
        #Erase this list so mouse motion function won't throw an error
        self.notes_box_list = []

        for item in self.delete_list:
            item[0].layout.delete()
            item.pop(0)
            for task in item:
                task.delete()
        self.delete_list = []


    def draw_task(self,item):
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
                                    "Est. Time: ",
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
                                    y=self.y_offset,
                                    bold=True,
                                    color=BLACK,
                                    batch = self.main_batch,
                                    group = self.foreground
                                    )

        self.task_description = TextWidget(
                                    item[1],
                                    self.x_offset+120,
                                    self.y_offset-41,
                                    200,
                                    self.main_batch,
                                    self.foreground
                                    )

        # This prevents flashing carets from appearing while scrolling
        # back/forward
        self.task_description.caret.delete()

        self.notes = pyglet.text.Label(
                                    'Notes',
                                    x=self.x_offset+15,
                                    y=self.y_offset-26,
                                    bold=True,
                                    color=BLACK,
                                    batch = self.main_batch,
                                    group = self.foreground
                                    )

        self.notes_box = pyglet.shapes.Rectangle(
                                            x=self.x_offset+13,
                                            y=self.y_offset-29,
                                            width=50,
                                            height=20,
                                            color=ORANGE_3,
                                            batch = self.main_batch,
                                            group = self.background
                                            )

        self.notes_box_list.append({"task_name" : self.task_name,
                                    "notes_box" : self.notes_box,
                                    })

        self.delete_list.append([self.task_description,
                                self.task_name_intro,
                                self.task_name,
                                self.task_time_info_intro,
                                self.task_time_info,
                                self.task_description_intro,
                                self.task_time_info,
                                self.task_description_intro,
                                self.notes,
                                self.notes_box])

        ##This adds more lines to show the full description if it's
        #greater than the original 3 lines-worth of height.
        text_height = self.task_description.layout.get_line_count()
        if text_height > 3:
            self.task_description.layout.height = 18 * text_height
            self.task_description.layout.y = \
                                (self.y_offset - 41) - (9 * text_height)
        self.y_offset -= (20 * text_height)
        self.y_offset -= 110

        if self.y_offset < 110:
            self.x_offset += 330
            self.y_offset = self.height - 160
            self.current_row += 1


    def on_draw(self):
        pyglet.gl.glClearColor(1, 1, 1, 1)
        self.clear()
        self.main_batch.draw()


    def on_mouse_motion(self, x, y, dx, dy):

        for item in self.notes_box_list:
            if hit_test(item["notes_box"], x, y):
                item["notes_box"].color = LIGHTSABER_GREEN_3
            else:
                item["notes_box"].color = ORANGE_3
        try:

            if hit_test(self.next_box, x, y):
                self.next_box.color = LIGHTSABER_GREEN_3
            else:
                self.next_box.color = GREY_3

            if hit_test(self.previous_box, x, y):
                self.previous_box.color = LIGHTSABER_GREEN_3
            else:
                self.previous_box.color = GREY_3
        except:
            pass


    def on_mouse_press(self, x, y, button, modifiers):

        if button ==  mouse.LEFT:

            for item in self.notes_box_list:
                if hit_test(item["notes_box"], x, y):
                    if self.notes_window_open == True:
                        return
                    else:
                        info=retrieve_notes(item["task_name"].text)
                        x,y = self.get_location()
                        InfoWindow(info[0], x, y, caption = 'Notes')
                        return
            try:
                if hit_test(self.next_box, x, y):
                    if self.page_number  != 3:
                        self.current_row = 0
                        self.next_page()

                if hit_test(self.previous_box, x, y):
                    if self.page_number != 0:
                        self.current_row = 0
                        self.previous_page()
            except:
                pass


    def on_close(self):
        main_window.completed_window_open = False
        self.close()

# fix the notes layout
class AddNotesWindow(pyglet.window.Window):
    def __init__(self, x, y, item):
        super().__init__(470, 300, caption = "Task Summary")
        self.set_location(x + 60, y + 120)
        if handlers_on == True:
            self.push_handlers(event_logger)

        self.main_batch = pyglet.graphics.Batch()
        self.background = pyglet.graphics.OrderedGroup(0)
        self.foreground = pyglet.graphics.OrderedGroup(1)
        self.item = item

        label_text = "Add notes about the completed task?"
        self.greeting_label = pyglet.text.Label(label_text,
                        x=90, y=self.height-30, bold=True,
                        multiline=True, width=350, color=BLACK,
                        batch=self.main_batch)
        icon_x = self.width//2-20

        main_window.notes_window_open = False
        # 'Canvas not attached' bug fix \Lib\site-packages\pyglet\gl\base.py
        # lines 306 and 328 were changed.  now has a self.is_ok var
        if self.context.is_ok == 0:
            main_window.notes_window_open = False
            self.close()

        self.set_visible()
        self.add_task_btn = pyglet.shapes.Rectangle(
                                            x=icon_x,
                                            y=self.height-90,
                                            width=ADD_ICON_SIZE,
                                            height=ADD_ICON_SIZE,
                                            color=ICON_BOX_COLOR,
                                            batch = self.main_batch,
                                            group = self.background)

        self.add_task = pyglet.text.Label(
                                    '+',
                                    x=icon_x+12,
                                    y=self.height-81,
                                    bold=True,
                                    color=BLACK,
                                    font_size=20,
                                    batch = self.main_batch,
                                    group = self.foreground)

        self.add_note = TextWidget(
                                    "Add Note",
                                    134,
                                    82,
                                    200,
                                    self.main_batch,
                                    self.foreground,
                                    height=30)

        self.add_note_box = pyglet.shapes.Rectangle(
                                      130,
                                      75,
                                      width = 220,
                                      height = 100,
                                      color = GREY_3,
                                      batch=self.main_batch,
                                      group = self.background
                                      )
        self.text_cursor = self.get_system_mouse_cursor('text')
        self.focus = None
        self.set_focus(self.add_note)


    def on_draw(self):
        pyglet.gl.glClearColor(1, 1, 1, 1)
        self.clear()
        self.main_batch.draw()


    def on_mouse_press(self, x, y, button, modifiers):

        if button == mouse.LEFT:
            if hit_test(self.add_task_btn, x, y):

                title = self.item['task_label'].text
                description = retrieve_description(title)[0]
                # time = 0
                time = retrieve_task_info(title)[-1]
                on_time = 1
                notes = self.add_note.document.text
                add_completed_task(
                                title,
                                description,
                                time,
                                on_time,
                                notes)

                description = add_break_lines(description)
                notes       = add_break_lines(notes)
                with open('records.txt', 'a') as file:
                    _ = "Task Name: "+title+"\n"+"Description: "+ \
                    description+"\n"+"Estimated Time to Complete: "+\
                    str(time)+"\n"+"Was the Task Ontime? "+str(on_time)+\
                    "\n"+"Notes: "+notes+"\n\n"

                    file.write(_)

                remove_task(self.item)
                self.close()


    def on_mouse_motion(self, x,y,dx,dy):
        #Change "+" button color on hover
        if hit_test(self.add_task_btn, x, y):
                self.add_task_btn.color = ICON_BOX_COLOR_HOVER
        else:
                self.add_task_btn.color = ICON_BOX_COLOR

        if hit_test(self.add_note_box, x, y):
            self.set_mouse_cursor(self.text_cursor)
        else:
            self.set_mouse_cursor(None)


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


    def set_focus(self, focus):
        if self.focus:
            self.focus.caret.visible = False
            self.focus.caret.mark = self.focus.caret.position = 0

        self.focus = focus
        if self.focus:
            self.focus.caret.visible = True
            self.focus.caret.mark = 0
            self.focus.caret.position = len(self.focus.document.text)


class InfoWindow(pyglet.window.Window):
    def __init__(self,task_description,x,y, caption = "Description",
                  ):
        super().__init__(300,200, caption = caption, visible=False)


        self.set_location(x+60,y+120)
        if handlers_on == True:
            self.push_handlers(event_logger)
        self.task_description = task_description
        if len(task_description) > 45:
            self.width = 500
            self.height = 400
        self.greeting_label = pyglet.text.Label(self.task_description,
                        x=18, y=self.height-30, bold=True,
                        multiline = True, width = 270, color=BLACK)
        self.xyz = 0
        #
        if caption == "Description":
            main_window.description_window_open = True
        else:
            main_window.completed_win.notes_window_open = True
            #Canvas not attached' bug fix \Lib\site-packages\pyglet\gl\base.py
            #lines 306 and 328 were changed.  now has a self.is_ok var
        if self.context.is_ok == 0:
            if caption == "Description":
                main_window.completed_win.notes_window_open = False
                self.close()
            else:
                main_window.description_window_open = False

        self.set_visible()


    def on_draw(self):
        pyglet.gl.glClearColor(1, 1, 1, 1)
        self.clear()
        self.greeting_label.draw()

    #This ensures when a task button is pressed only one window can open
    def on_close(self):
        main_window.description_window_open = False
        self.close()

########### End of Window Classes^ ###########
##############################################

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
        item['check_box'].color = LIGHTSABER_GREEN_3

    else:
        TIMER -= 1
        item["task_time"].text = ""
        item["task_time"].text = str(TIMER)
        update_timer(TIMER, item["task_label"].text)


def display_project_time(dt):

    #Keeps track of total time programming still even if db is deleted
    new_time = run_project_timer()
    main_window.project_time_count.text = str(new_time)


def add_break_lines(item):
    count = len(item)//60
    if count > 0:
        _ = 60
        for x in range(count):
            #Breaks a long item into multiple lines.
            item = item[:_]+"\n"+(" "*7)+item[_:]

            _ += 62
    return item


def organize_completed_tab(info):
    rslts = []
    x=0
    if len(info) > 12:
        for item in range(len(info)//12):
            rslts.append(info[x:x+12])
            x += 12
    else:
        rslts.append(info)
    return rslts

if __name__ == '__main__':
    db_startup()
    main_window = Home_Window(WNDW_WIDTH,WNDW_HEIGHT,"TaskTrack")
    # main_window.retrieve_saved_tasks()
    pyglet.app.run()
