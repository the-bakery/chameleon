import pyglet
from pyglet.gl import *

import cv2
from cv2 import VideoCapture


class VideoStream(object):

    def __init__(self, device, width, height):
        self.capture = VideoCapture(device)
        assert self.capture.isOpened(), 'failed to open stream %s' % device
        self.capture.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, width)
        self.capture.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, height)
        self.texture = pyglet.gl.GLuint()
        glGenTextures(1, self.texture)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexParameteri(GL_TEXTURE_2D, GL_GENERATE_MIPMAP, GL_TRUE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)

    def next(self):
        status, frame = self.capture.read()
        if status:
            width = frame.shape[1]
            height = frame.shape[0]
            glBindTexture(GL_TEXTURE_2D, self.texture)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_BGR, GL_UNSIGNED_BYTE, frame.ctypes.data)

    def bind(self):
	glBindTexture(GL_TEXTURE_2D, self.texture)

