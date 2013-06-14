import pyglet
from pyglet.gl import *

import cv2
from cv2 import VideoCapture

from videostream import VideoStream


class Main(pyglet.window.Window):

    def __init__(self, **kwargs):
        super(Main, self).__init__(**kwargs)
	self.streams = [VideoStream(0, 1024, 768)]
	
    def on_resize(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
	glOrtho(0.0, 1.0, 1.0, 0.0, -1, 1);
        glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
        glDisable(GL_DEPTH_TEST)
	glEnable(GL_TEXTURE_2D)
	glClearColor(0.0, 0.0, 0.0, 1.0)
        return pyglet.event.EVENT_HANDLED

    def on_idle(self, dt):
    	for stream in self.streams:
	    stream.next()
    	
    def on_draw(self):
	glClear(GL_COLOR_BUFFER_BIT)
	def quad(x0, y0, x1, y1, du, dv):
	    glTexCoord2f(0.0 + du, 0.0 + dv)
	    glVertex2f(x0, y0)
	    glTexCoord2f(1.0 + du, 0.0 + dv)
    	    glVertex2f(x1, y0)
	    glTexCoord2f(1.0 + du, 1.0 + dv)
    	    glVertex2f(x1, y1)
	    glTexCoord2f(0.0 + du, 1.0 + dv)
    	    glVertex2f(x0, y1)
        glBegin(GL_QUADS)
	quad(0.0, 0.0, 0.5, 1.0, -0.125, 0.0)
    	quad(0.5, 0.0, 1.0, 1.0, +0.125, 0.0)
	glEnd()

    def on_mouse_press(self, x, y, button, modifiers):
        return

    def on_mouse_release(self, x, y, button, modifiers):
        return

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        return


def main():
    config = pyglet.gl.Config(sample_buffers=1, samples=4, double_buffer=True)
    window = Main(caption='chameleon', resizable=True, vsync=True, config=config)

    pyglet.clock.schedule_interval(window.on_idle, (1.0/30))
    pyglet.app.run()


if __name__ == '__main__':
    main()

