from imutils.video import FileVideoStream
from pykeyboard import PyKeyboard
import cv2
import numpy as np
import argparse
import imutils
import time

# argument parser (for video, will use stream/live frames in future)
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", required=True,
    help="Path to video file")
args = vars(ap.parse_args())

# start threaded video stream, give buffer time to fill
print("Initializing video stream...")
fvs = FileVideoStream(args["video"]).start()
time.sleep(1.0)

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

# define keys (8 for IIDX-style games)
scratch = Key(16, 99, "SCRATCH", 'X')
key1 = Key(70, 99, "KEY 1", 'C')
key2 = Key(104, 99, "KEY 2", 'F')
key3 = Key(135, 99, "KEY 3", 'V')
key4 = Key(169, 99, "KEY 4", 'G')
key5 = Key(199, 99, "KEY 5", 'B')
key6 = Key(232, 99, "KEY 6", 'H')
key7 = Key(263, 99, "KEY 7", 'N')

# put keys in array
keyArray = [scratch, key1, key2, key3, key4, key5, key6, key7]

# initialize keyboard
keyboard = PyKeyboard()

# create background subtractor
bgSub = cv2.createBackgroundSubtractorMOG2()

# array for checking which keys were pressed on a frame
keysPressed = []

# loop over frames from the video file stream
while fvs.more():

    # grab current frame from video stream
    frame = fvs.read()

    # crop the grabbed frame
    cropped_frame = frame[0:100, 49:336]

    # old crop value (for whole note field):
    # cropped_frame = frame[0:484, 49:336]

    # apply mask to frame
    mask = bgSub.apply(cropped_frame)

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
    cv2.imshow("output", mask)
    cv2.waitKey(1)

# cleanup
cv2.destroyAllWindows()
fvs.stop()
