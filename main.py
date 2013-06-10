import pyglet
from pyglet.gl import *

import cv2
from cv2 import VideoCapture


class Main(pyglet.window.Window):

    def __init__(self, **kwargs):
        super(Main, self).__init__(**kwargs)
	self.streams = [VideoCapture(1)]
	assert self.streams[0].isOpened(), 'failed to open stream 0'
	self.streams[0].set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 720)
	self.streams[0].set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 540)
	self.textures = (pyglet.gl.GLuint * 2)()
	glGenTextures(2, self.textures)

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
    	status, frame = self.streams[0].read()
	if status:
	    width = frame.shape[1]
	    height = frame.shape[0]
	    glBindTexture(GL_TEXTURE_2D, self.textures[0])
	    glTexParameteri(GL_TEXTURE_2D, GL_GENERATE_MIPMAP, GL_TRUE)
	    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
	    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
	    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_BGR, GL_UNSIGNED_BYTE, frame.ctypes.data)

    def on_draw(self):
	glClear(GL_COLOR_BUFFER_BIT)
        glBegin(GL_QUADS)
    	glTexCoord2f(0.0, 0.0)
	glVertex2f(0.0, 0.0)
	glTexCoord2f(1.0, 0.0)
    	glVertex2f(1.0, 0.0)
	glTexCoord2f(1.0, 1.0)
    	glVertex2f(1.0, 1.0)
	glTexCoord2f(0.0, 1.0)
    	glVertex2f(0.0, 1.0)
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

