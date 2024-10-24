When I uploaded my python code, I also uploaded a demo video to show that my code can achieve the functions required by Question 12.

This Python code uses OpenCV to detect a laser pointer in real-time using a webcam feed. It works by capturing video frames from the webcam and converting them to HSV color space, which is suitable for color detection.
The program defines multiple HSV ranges to detect different colors of visible la 
ser pointers, including red, green, and blue. By using these HSV ranges, the program creates color masks to identify pixels corresponding to the laser pointer's color.
Once the masks are created, they are combined to detect all possible laser color 
s. The program applies morphological operations (erosion and dilation) to remove noise and find the laser pointer more accurately. It then finds contours in the mask and selects the contour with the highest brightness as the laser pointer to reduce errors.
A minimum enclosing circle is calculated for the brightest contour, and its position is displayed on the video feed as a circle, along with the coordinates of the laser pointer. The program runs continuously until the user presses the 'q' key or closes the window.
