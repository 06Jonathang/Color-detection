import cv2                                                  # OpenCV, for video capture, color conversion, and drawing
import numpy as np                                          # NumPy, for building the red HSV range arrays
from PIL import Image                                       # Pillow's Image class, used to get bounding boxes from the mask

from util import get_limits                                 # your custom function that converts a BGR color into an HSV range

colors = {                                                  # dictionary mapping a key press to (color name, BGR value)
    'y': ('yellow', [0, 255, 255]),                         # pressing 'y' selects yellow
    'b': ('blue', [255, 0, 0]),                             # pressing 'b' selects blue
    'g': ('green', [0, 255, 0]),                            # pressing 'g' selects green
}

current_key = 'y'  # default starting color                 # tracks which color is currently active; starts on yellow

cap = cv2.VideoCapture(0)                                   # opens the default webcam (device index 0)
while True:                                                 # infinite loop, runs once per frame until manually broken
    ret, frame = cap.read()                                 # grabs one frame from the webcam; ret = success flag, frame = image data

    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)       # converts the frame from BGR to HSV for reliable color matching

    if current_key == 'r':                                  # special case: red needs different handling than other colors
        color_name = 'red'                                  # sets the label text to 'red'
        bgr_value = (0, 0, 255)                             # sets red's BGR value, used for drawing the box/text
        lowerRed1 = np.array([0, 150, 150], dtype=np.uint8)    # lower bound of red's first hue range (near 0)
        upperRed1 = np.array([5, 255, 255], dtype=np.uint8)    # upper bound of red's first hue range
        lowerRed2 = np.array([175, 150, 150], dtype=np.uint8)  # lower bound of red's second hue range (near 179, the wraparound)
        upperRed2 = np.array([179, 255, 255], dtype=np.uint8)  # upper bound of red's second hue range

        mask1 = cv2.inRange(hsvImage, lowerRed1, upperRed1)    # mask for pixels matching red's first hue range
        mask2 = cv2.inRange(hsvImage, lowerRed2, upperRed2)    # mask for pixels matching red's second hue range
        mask = cv2.bitwise_or(mask1, mask2)                     # combines both red masks into one, since red spans two ranges
    else:                                                 # for every other color (yellow, blue, green)
        color_name, bgr_value = colors[current_key]        # looks up the name and BGR value for the currently selected color
        lowerLimit, upperLimit = get_limits(color=bgr_value)   # calculates the HSV range for that color using your util function
        mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)   # builds the mask: white where the color is detected, black elsewhere

    mask_ = Image.fromarray(mask)                          # converts the NumPy mask into a Pillow Image object
    bbox = mask_.getbbox()                                 # finds the bounding box of all non-black pixels in the mask (or None if empty)

    if bbox is not None:                                   # only proceed if something was actually detected
        x1, y1, x2, y2 = bbox                               # unpacks the bounding box into individual coordinates
        area = (x2 - x1) * (y2 - y1)                        # calculates the box's area in pixels, used to filter out tiny noise
        if area > 2000:                                     # only draw if the detected area is big enough to be a real object
            frame = cv2.rectangle(frame, (x1, y1), (x2, y2), bgr_value, 5)   # draws a rectangle around the detected object
            cv2.putText(frame, color_name, (x1, y2 + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.9, bgr_value, 2)  # labels the box with the color's name

    cv2.putText(frame, f"Detecting: {color_name} (press y/b/g/r to switch)", (10, 30),   # displays current mode in the top-left corner
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)                        # (font, scale, white color, thickness)

    cv2.imshow('frame', frame)                             # displays the current frame (with any drawn box/text) in a window

    key = cv2.waitKey(1) & 0xFF                             # waits 1ms for a key press, extracts the key code
    if key == ord('q'):                                     # if 'q' was pressed...
        break                                               # ...exit the while loop
    elif chr(key) in ['y', 'b', 'g', 'r']:                  # if the pressed key matches one of the valid color keys...
        current_key = chr(key)                              # ...switch detection to that color

cap.release()                                             # releases the webcam so other programs can use it
cv2.destroyAllWindows()                                   # closes any OpenCV display windows still open