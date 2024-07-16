# tasktrack
This app tracks different tasks and records notes about them.

While Pyglet is a big program for this job, I was learning to code and
ended up using it.

To run the program, make sure all dependencies are installed and run the gui.py file.

** Docs

When starting program, choose a name and press the plus icon.

Add a new task.
  - To add a new task, press the + icon on the main screen.  Once added, it can be ended early, using the ! icon, edited by pressing the "..." icon, or deleted by pressing the "x".

When task completes
 -A completed task's time counter will turn green.  It can then be added to the archive by pressing the "!" icon.  

Completed tasks
 - Completed tasks can be reviewed by pressing the "Completed" button.

Finish a project
 - To finish the project, click the "Finish Project" button.


App is in alpha.


PLEASE NOTE - Pyglet version has a small change.
  
  The pyglet package has two changed lines, noted at the top of the gui.py file.  This was done to handle the error "Canvas not attached."
  They add a flag.
