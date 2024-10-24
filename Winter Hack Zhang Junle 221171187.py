import cv2
import numpy as np
import sys

# Set up webcam feed
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    sys.exit()

while True:
    # Capture frame from the webcam
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    # Resize frame for better performance (optional)
    frame = cv2.resize(frame, (640, 480))

    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define multiple HSV ranges for detecting different laser colors
    # Red color range
    red_lower_hsv_1 = np.array([0, 100, 100])
    red_upper_hsv_1 = np.array([10, 255, 255])
    red_lower_hsv_2 = np.array([160, 100, 100])
    red_upper_hsv_2 = np.array([180, 255, 255])

    # Green color range
    green_lower_hsv = np.array([40, 100, 100])
    green_upper_hsv = np.array([80, 255, 255])

    # Blue color range
    blue_lower_hsv = np.array([100, 100, 100])
    blue_upper_hsv = np.array([140, 255, 255])

    # Create masks for each color
    red_mask_1 = cv2.inRange(hsv, red_lower_hsv_1, red_upper_hsv_1)
    red_mask_2 = cv2.inRange(hsv, red_lower_hsv_2, red_upper_hsv_2)
    green_mask = cv2.inRange(hsv, green_lower_hsv, green_upper_hsv)
    blue_mask = cv2.inRange(hsv, blue_lower_hsv, blue_upper_hsv)

    # Combine all masks
    mask = cv2.bitwise_or(red_mask_1, red_mask_2)
    mask = cv2.bitwise_or(mask, green_mask)
    mask = cv2.bitwise_or(mask, blue_mask)

    # Apply some morphological operations to reduce noise
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Check if any contour is detected
    if contours:
        # Find the largest contour with the highest brightness
        brightest_contour = max(contours, key=lambda c: cv2.mean(hsv, mask=cv2.drawContours(np.zeros_like(mask), [c], -1, 255, thickness=cv2.FILLED))[2])

        # Calculate the minimum enclosing circle for the brightest contour
        ((x, y), radius) = cv2.minEnclosingCircle(brightest_contour)

        # Define a threshold for the size of the detected laser pointer
        if radius > 3:  # Radius threshold to filter out noise
            # Draw the circle and centroid on the frame
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 0), 2)
            cv2.circle(frame, (int(x), int(y)), 5, (0, 0, 255), -1)

            # Display the coordinates of the laser pointer
            cv2.putText(frame, f"Laser Pointer: ({int(x)}, {int(y)})", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Display the resulting frame
    cv2.imshow('Laser Pointer Detection', frame)

    # Exit the loop if 'q' is pressed or the window is closed
    if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty('Laser Pointer Detection', cv2.WND_PROP_VISIBLE) < 1:
        break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()
sys.exit()
