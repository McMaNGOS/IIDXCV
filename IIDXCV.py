from imutils.video import FileVideoStream
import cv2
import numpy as np
import argparse
import imutils
import time

# class for constructing key objects
class Key:
    'Data for each key (detection pixel x/y location, name)'

    def __init__(self, x, y, name):

        # x and y axis of pixel to check for
        self.x = x
        self.y = y

        # name of key (to print in console)
        self.name = name

        # TODO: add actual key value (for input)

# define keys (8 for IIDX-style games)
key1 = Key(16, 99, "SCRATCH")
key2 = Key(70, 99, "KEY 1")
key3 = Key(104, 99, "KEY 2")
key4 = Key(135, 99, "KEY 3")
key5 = Key(169, 99, "KEY 4")
key6 = Key(199, 99, "KEY 5")
key7 = Key(232, 99, "KEY 6")
key8 = Key(263, 99, "KEY 7")

# put keys in array
keyArray = [key1, key2, key3, key4, key5, key6, key7, key8]

# argument parser (for video, will use stream/live frames in future)
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", required=True,
    help="Path to video file")
args = vars(ap.parse_args())

# start threaded video stream, give buffer time to fill
print("Initializing video stream...")
fvs = FileVideoStream(args["video"]).start()
time.sleep(1.0)

# create background subtractor
bgSub = cv2.createBackgroundSubtractorMOG2()

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
    initialPrintArray = ['_______', '_____', '_____', '_____', '_____', '_____', '_____', '_____']

    # loop through keys in array
    for idx, Key in enumerate(keyArray):

        # detect pixel at given coordinates
        pixel = mask[Key.y, Key.x]

        # if white pixel found, add key to printArray
        if pixel == 255:
            printArray[idx] = Key.name

    # print if array is different from default (key detected)
    if printArray != initialPrintArray:
        print printArray

    # display frame with mask
    cv2.imshow("output", mask)
    cv2.waitKey(1)

# cleanup
cv2.destroyAllWindows()
fvs.stop()
