# required for delays
import random
import time

# used to send user input to roblox process
from pynput import mouse, keyboard # command : pip install pynumpyut

# used for image processing
import cv2 # https://pypi.org/project/opencv-python/
import numpy # dependency of opencv so no need to install

#screenshot libs
from mss.windows import MSS as mss # pip install mss

class rod :
    def __init__(self) :
        print('initialised rod')

        # create mouse object
        self.mouse = mouse.Controller()

    def catch(self, *args) :
        # click
        time.sleep(3 + (random.randint(-5, 5) / 10))

# if q is pressed quit program as failsafe
def stop(key) :
    if key == 'q' :
        cv2.destroyAllWindows()
        exit()

keyboard.Listener(on_press=stop)

# initialise some objects
rod = rod()
sct = mss()

# configurable bbox for rod detection
bbox = (2500,1500,3500,2000)

# initialise some windows for opencv
cv2.imshow('programs vision', numpy.zeros([480, 640, 1]))
cv2.setWindowProperty('programs vision', cv2.WND_PROP_TOPMOST, 1)

cv2.imshow('binary', numpy.zeros([480, 640, 1]))
cv2.setWindowProperty('binary', cv2.WND_PROP_TOPMOST, 1)

# configure noise filter
kernel_size = (3,3) # should roughly have the size of the elements you want to remove
kernel_el = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_size)

while True :
    #take screenshot
    screen = numpy.array(sct.grab(bbox))

    # display the screen
    cv2.imshow('programs vision', screen)

    #### process the image to get only shades of white 
    binary = numpy.zeros((screen.shape[:-1]))
    # create boolean masks
    a = screen[:, :, 0] == screen[:, :, 1]
    b = screen[:, :, 1] == screen[:, :, 2]
    # this will create the final mask (a and b)
    mask = numpy.logical_and(a, b)
    # make the final assignment
    binary[mask] = 1

    # apply noise filter
    binary = cv2.erode(binary, kernel_el, (-1, -1))

    # show binary arrary for troubleshooting
    cv2.imshow('binary', binary)

    # check if bober is underwater
    average = numpy.average(binary)
    if average == 0 :
        rod.catch()

    # stuff that fixes opencv
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
