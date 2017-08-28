from imutils.video import FileVideoStream
from pykeyboard import PyKeyboard
import cv2
import numpy as np
import argparse
import imutils
import time

# class for constructing key objects
class Key:
    'Data for each key (detection pixel x/y location, name)'

    def __init__(self, x, y, name, keyButton):

        # x and y axis of pixel to check for
        self.x = x
        self.y = y

        # name of key (to print in console)
        self.name = name

        # keyboard button to press
        self.keyButton = keyButton

# presses and holds input key, adds key to array
def pressKey(key, pressedArray):
    keyboard.press_key(key.keyButton)
    pressedArray.append(key)

# releases input key, removes key from array
def releaseKey(key, pressedArray):
    keyboard.release_key(key.keyButton)
    pressedArray.remove(key)

# since y is always the same value (bottom of screen), it's defined here
y = 99

# define keys (8 for IIDX-style games)
scratch = Key(16, y, "SCRATCH", 'X')
key1 = Key(70, y, "KEY 1", 'C')
key2 = Key(104, y, "KEY 2", 'F')
key3 = Key(135, y, "KEY 3", 'V')
key4 = Key(169, y, "KEY 4", 'G')
key5 = Key(199, y, "KEY 5", 'B')
key6 = Key(232, y, "KEY 6", 'H')
key7 = Key(263, y, "KEY 7", 'N')

# put keys in array
keyArray = [scratch, key1, key2, key3, key4, key5, key6, key7]

# initialize video capture (fake webcam)
cap = cv2.VideoCapture(0)

# initialize keyboard
keyboard = PyKeyboard()

# create background subtractor
bgSub = cv2.createBackgroundSubtractorMOG2()

# array for checking which keys were pressed on a frame
keysPressed = []

# create and resize cv2 window
cv2.namedWindow('output', cv2.WINDOW_NORMAL)

# loop over frames from the video file stream
while (True):

    # grab current frame from video stream
    _, frame = cap.read()

    # crop the grabbed frame
    # cropped_frame = frame[0:100, 49:336]

    # old crop value (for whole note field):
    # cropped_frame = frame[0:484, 49:336]

    # apply mask to frame
    mask = bgSub.apply(frame)

    # keys to print (underscores by default, for readability) [for debugging]
    # printArray = ['_______', '_____', '_____', '_____', '_____', '_____', '_____', '_____']
    # initialPrintArray = printArray

    # loop through keys in array
    for idx, Key in enumerate(keyArray):

        # detect pixel at given coordinates
        pixel = mask[Key.y, Key.x]

        # if white pixel found, pressKey
        if pixel == 255 and Key not in keysPressed:
            pressKey(Key, keysPressed)
            # printArray[idx] = Key.name

        # if white pixel not found & key is in keysPressed, releaseKey
        if pixel != 255 and Key in keysPressed:
            releaseKey(Key, keysPressed)

    # print if array is different from default (= key detected)
    # if printArray != initialPrintArray:
    #    print printArray

    # display frame with mask
    maskSmall = cv2.resize(mask, (320, 240))
    cv2.imshow("output", maskSmall)
    cv2.waitKey(1)

# cleanup
cv2.destroyAllWindows()
fvs.stop()
