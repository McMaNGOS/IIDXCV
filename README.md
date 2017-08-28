# IIDXCV
A (currently proof-of-concept) OpenCV-powered IIDX-style rhythm game playing bot.

Right now capable of processing IIDX gameplay videos, detecting notes, and hitting the corresponding keys on the keyboard when the notes reach the bottom of the screen.

*building for educational purposes only, cheating is Bad™*

## Setup
To run this, you'll need the following installed and configured properly on your system:

* Python 2.7.10+
* OpenCV 3.3.0 (with relevant packages, numpy etc)
* [PyUserInput](https://github.com/PyUserInput/PyUserInput) (with dependencies needed for your OS)
* [imutils](https://github.com/jrosebr1/imutils) (for video processing, won't be needed later)

## Usage
*Do note that the bot currently cannot play anything; it is only capable of processing gameplay footage and pressing keys (it is a proof-of-concept, after all).*

### Prepare a Beatmania IIDX video to use as input

The video should have a resolution of 1280x720, and should preferrably have a framerate of 60 FPS. Any format that OpenCV can process (most of them, I'd imagine) works fine here.

For reference, [this](https://www.youtube.com/watch?v=NoR0qqmfm3s) is the video I used when writing this bot (720p@60FPS).

Place it in the same directory as the script.

### Modify frame cropping coordinates 

*If you're using the video I linked in the previous step, you can skip this.*

The script needs to semi-accurately crop out the note lane, from width-to-width, in order to work properly. Depending on your input video, you'll need to adjust the part of the code which does the cropping. Trial-and-error is key here, so run the script first to see if it works.

If it looks weird by default, this is the line you'll need to modify:
```
cropped_frame = frame[0:100, 49:336]
```
Right now, this line crops out 100px from the top of the note lane (at least with the video I tested it with). The coordinates are formatted as [y:y+h, x:x+w]. So the default coordinates will result in a frame which is 287x100.

### Modify pixel coordinates for keys (if needed)

If you've messed around with the cropping coordinates (especially if you've modified the height), you may need to change the key pixel coordinate values as well. 

By default, the pixel coordinates for each key is at the center & bottom of its respective note lane.

### Run script with video
```
python IIDXCV.py -v yourvideo.mp4
```
The video should start, and you should start seeing keystrokes in the console window. Giving another window focus may send keystrokes to that window instead, so be careful here.

You can cancel the execution of the bot by pressing CTRL+C.

## TODO (in order of priority)

### ~~Add button-hitting capabilities~~ (DONE)

~~Self-explanatory, probably simple to implement since there are Python libraries available for this purpose (inputs, pygame, etc).~~

This is now implemented. The bot uses PyUserInput to press keys (simple, cross-platform solution). To use this bot with a gamepad, one would have to use an application to bind keystrokes to gamepad presses.

### Read from screen instead of video

Currently investigating solutions for this. A screenshot library like [mss](https://github.com/BoboTiG/python-mss) could work, if the resulting framerate is acceptable. 

Reading from screen recording software/"fake webcam" is also an option, although latency may be a problem in that case.

### Make it work with LR2 (or other BMS player)

The visual effects near the bottom of the note lanes in IIDX (lanes lighting up, explosions, etc) make it impossible to place the detection area near the hit area, at least with the current method I'm using to detect notes (background subtraction). 

Placing it at the top and hitting keys with a delay is a solution to this, but it won't work for songs with tempo changes.

In LR2, such effects can (probably?) be removed using a custom skin, so making it work with that would be good for the time being.

### Make it work with long notes

Probably possible by simply making the script hold down a key while a white pixel is present in the detection area for that key. 

May require some logic restructuring (e.g. if pixel is found in frame, press and hold key, save array of pressed keys for current frame, if pixel is found in next frame and key is present in saved array from last frame, keep key held, else release key).

### Improve detection/accuracy

While the stuff it prints to console looks pretty accurate, I can't actually be sure until the bot is actually functional. Especially for charts with very dense note patterns.

Once it's working with LR2, fine-tuning can begin.

### Make it work with IIDX

*For the record, we're talking INFINITAS here, alternatively console IIDX if sending keys to a PS2 controller is viable.*

As stated above, visual effects make this a problem. Using a different method to detect notes is the solution here.

Color thresholding is a possible solution, although when I attempted to implement that, it required far too much processing to be viable (it wasn't 100% reliable, either).

### Implement neural network for machine learning

Long-term plan, but using this bot to have a neural network learn to play rhythm games is a pretty neat concept.

## Credits
[PyImageSearch](http://www.pyimagesearch.com/) was an invaluable resource when putting this together, given that I'm a complete beginner when it comes to computer vision. Would highly recommend said site if you're interested in this stuff.

If you have experience with OpenCV, machine learning, or have any other relevant skill to contribute to this project with, go right ahead! I'm very new to this stuff so any help is appreciated. Doing this to learn.
