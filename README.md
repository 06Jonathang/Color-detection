MOTIVATION:
I was solving a rubiks cube in the relatively dark environment and I mixed up the color red and orange. Than it hit me, why dont I just make a program that can detect colors, just because I can.

In the util.py file, it contains a function. This function, get_limits(), takes a single BGR color as input and converts it into a usable HSV detection range. It disguises the color as a tiny fake image so OpenCV's cvtColor function can convert it from BGR to HSV. From that HSV value, it builds a lower and upper bound by subtracting/adding 10 from the hue (for tolerance) while fixing wide saturation/value ranges to handle lighting variation. Finally, it converts both bounds into properly formatted NumPy arrays and returns them, ready to be plugged directly into cv2.inRange() for color detection.

Below is the 1st phase; Detects anything with the color yellow from the webcam.

import cv2                                                                      # import OpenCV library
from PIL import Image                                                           # import Image module from the Python Imaging Library (PIL) to work with images
from util import get_limits                                                     # import the get_limits function from the util module to convert BGR colors to HSV limits for color detection

yellow = [0, 255, 255]                                                          # yellow in BGR color space
cap = cv2.VideoCapture(0)                                                       # Open webcam (0 is the default camera index, change it if you have multiple cameras)
while True:
    ret, frame = cap.read()                                                     # Grabs a frame from webcam and returns ret(true/false) & frame(image data as numpy array)
    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)                           # Converts the captured frame from BGR color space to HSV color space using OpenCV's cvtColor function.
    lowerLimit, upperLimit = get_limits(color=yellow)                           # Calls the get_limits function from the util module, passing the yellow color in BGR format. The function returns the lower and upper limits for detecting yellow in HSV color space.
    mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)                        # Creates a binary mask where pixels within the specified HSV range (yellow) are set to 255 (white) and others to 0 (black). This isolates the yellow regions in the frame.
    mask_ = Image.fromarray(mask)                                               # Converts the binary mask (NumPy array) to a PIL Image object, allowing for further image processing using PIL's capabilities.
    bbox = mask_.getbbox()                                                      # Retrieves the bounding box of the non-zero regions in the binary mask. The getbbox() method returns a tuple (x1, y1, x2, y2) representing the coordinates of the bounding box that encloses all non-zero pixels in the mask. If no non-zero pixels are found, it returns None.

    if bbox is not None:
        x1, y1, x2, y2 = bbox                                                   # Unpacks the bounding box coordinates into individual variables for easier access and manipulation. These coordinates represent the top-left (x1, y1) and bottom-right (x2, y2) corners of the bounding box that encloses the detected yellow region in the frame.
        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)        # Draws a rectangle on the original frame using OpenCV's rectangle function. The rectangle is drawn from the top-left corner (x1, y1) to the bottom-right corner (x2, y2) with a green color (0, 255, 0) and a thickness of 5 pixels. This visually highlights the detected yellow region in the video feed.

    cv2.imshow('frame', frame)                                                  # Displays the original frame with the drawn rectangle in a window titled 'frame'. This allows the user to see the live video feed from the webcam along with the detected yellow regions highlighted by the rectangle.

    if cv2.waitKey(1) & 0xFF == ord('q'):                                       # Waits for a key press for 1 millisecond and checks if the 'q' key was pressed. If 'q' is pressed, the loop breaks, allowing the program to exit gracefully. The bitwise AND operation with 0xFF ensures compatibility across different platforms and OpenCV versions when checking for key presses.
        break

cap.release()
cv2.destroyAllWindows()                                                         # closes webcam and all OpenCV windows
