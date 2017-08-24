from imutils.video import FileVideoStream
import cv2
import numpy as np
import argparse
import imutils
import time
import pyvjoy

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

        # vJoy button to press
        self.keyButton = keyButton

# set key state to on (1)
def pressKey(key):
    global keysPressed
    gamepad.set_button(key.keyButton, 1)
    keysPressed.append(key)

# set key state to off (0)
def releaseKey(key):
    global keysPressed
    gamepad.set_button(key.keyButton, 0)
    keysPressed.remove(key)

# LR2 treats the scratch as two normal keys, while IIDX treats it as a
# rotating axis. Separate function will be needed for IIDX. (pass game as arg?)

# define keys (8 for IIDX-style games)
scratch = Key(16, 99, "SCRATCH", 1)
key1 = Key(70, 99, "KEY 1", 2)
key2 = Key(104, 99, "KEY 2", 3)
key3 = Key(135, 99, "KEY 3", 4)
key4 = Key(169, 99, "KEY 4", 5)
key5 = Key(199, 99, "KEY 5", 6)
key6 = Key(232, 99, "KEY 6", 7)
key7 = Key(263, 99, "KEY 7", 8)

# put keys in array
keyArray = [scratch, key1, key2, key3, key4, key5, key6, key7]

# construct gamepad
gamepad = pyvjoy.VJoyDevice(1)

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

    # keys to print (underscores by default, for readability)
    printArray = ['_______', '_____', '_____', '_____', '_____', '_____', '_____', '_____']
    initialPrintArray = printArray

    # loop through keys in array
    for idx, Key in enumerate(keyArray):

        # detect pixel at given coordinates
        pixel = mask[Key.y, Key.x]

        # if white pixel found, press key, add to keysPressed & print arrays
        if pixel == 255 && Key not in keysPressed:
            pressKey(Key)
            printArray[idx] = Key.name

        # if white pixel not found & key is in keysPressed, release & remove from array
        else if pixel != 255 && Key in keysPressed:
            releaseKey(Key)

        # else don't do anything at all! wow!
        else
            pass

    # print if array is different from default (= key detected)
    if printArray != initialPrintArray:
        print printArray

    # display frame with mask
    cv2.imshow("output", mask)
    cv2.waitKey(1)

# cleanup
cv2.destroyAllWindows()
fvs.stop()
