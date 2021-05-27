import threading
import random
import time

from pynput import mouse, keyboard # command : pip install pynumpyut
import cv2 # https://pypi.org/project/opencv-python/
from mss.windows import MSS as mss

import numpy

from win32api import GetSystemMetrics

class rod :
    def __init__(self) :
        print('initialised rod')

        # create mouse object
        self.mouse = mouse.Controller()

        # find out where to click
        screen = (GetSystemMetrics(0), GetSystemMetrics(1))
        x = screen[0] / 2 + random.randint(-5,5)
        y = screen[1] - (screen[1] / 10) + random.randint(-5,5)
        self.clickPos = (x,y)
        print('x :', x, 'y :', y)

    def catch(self, *args) :
        # click the mouse
        self.mouse.click(mouse.Button.left)
        time.sleep(3 + (random.randint(-5, 5) / 10))

# stop the program is q is pressed
def stop(key) :
    if key == 'q' :
        cv2.destroyAllWindows()
        exit()

keyboard.Listener(on_press=stop)

# initialise objects
rod = rod()
sct = mss()

bbox = (240,600,540,900)

cv2.imshow('programs vision', numpy.zeros([480, 640, 1]))
cv2.setWindowProperty('programs vision', cv2.WND_PROP_TOPMOST, 1)

cv2.imshow('binary', numpy.zeros([480, 640, 1]))
cv2.setWindowProperty('binary', cv2.WND_PROP_TOPMOST, 1)

kernel_size = (3,3) # should roughly have the size of the elements you want to remove
kernel_el = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_size)

# main loop
while True :
    # take screenshot and show it
    screen = numpy.array(sct.grab(bbox))
    cv2.imshow('programs vision', screen)

    ###### create a mask that only shows perfect shades of white #####
    binary = numpy.zeros((screen.shape[:-1]))
    # create boolean masks
    a = screen[:, :, 0] == screen[:, :, 1]
    b = screen[:, :, 1] == screen[:, :, 2]
    # this will create the final mask (a and b)
    mask = numpy.logical_and(a, b)
    # make the final assignment
    binary[mask] = 1
    binary = cv2.erode(binary, kernel_el, (-1, -1))

    #show the output of the mask
    cv2.imshow('binary', binary)

    # check for no white particles
    average = numpy.average(binary)
    print(average)

    # if there are none than catch
    if average == 0 :
        rod.catch()

    # close window on q
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
