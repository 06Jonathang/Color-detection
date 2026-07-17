MOTIVATION:
I was solving a rubiks cube in the relatively dark environment and I mixed up the color red and orange. Than it hit me, why dont I just make a program that can detect colors, just because I can.

In the util.py file, it contains a function. This function, get_limits(), takes a single BGR color as input and converts it into a usable HSV detection range. It disguises the color as a tiny fake image so OpenCV's cvtColor function can convert it from BGR to HSV. From that HSV value, it builds a lower and upper bound by subtracting/adding 10 from the hue (for tolerance) while fixing wide saturation/value ranges to handle lighting variation. Finally, it converts both bounds into properly formatted NumPy arrays and returns them, ready to be plugged directly into cv2.inRange() for color detection.

Below is the 1st phase; Detects anything with the color yellow from the webcam.

