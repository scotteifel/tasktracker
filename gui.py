import pyglet
from pyglet.window import mouse, key

window = pyglet.window.Window()

label = pyglet.text.Label("document", x=50,y=50)
# label = pyglet.text.Label("document", x=window.width//2,y=window.height//2,
# anchor_x='center',anchor_y='center')

# window = pyglet.window.Window()

rectang = pyglet.shapes.Rectangle(x=50,y=50,
            width=100,height=50,color = (55,55,255))

@window.event
def on_draw():
    window.clear()
    rectang.draw()
    label.draw()

@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == mouse.LEFT:
        print('The left mouse button was pressed.')

if __name__ == '__main__':
    pyglet.app.run()
