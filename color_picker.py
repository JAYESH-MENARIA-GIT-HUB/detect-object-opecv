import cv2
import numpy as np

# Initialize values for lower and upper bounds of HSV
lower_hsv = [0, 100, 100]
upper_hsv = [10, 255, 255]

# Create a function to update the lower HSV values
def update_lower_hsv_hue(value):
    lower_hsv[0] = value

def update_lower_hsv_saturation(value):
    lower_hsv[1] = value

def update_lower_hsv_value(value):
    lower_hsv[2] = value

# Create a function to update the upper HSV values
def update_upper_hsv_hue(value):
    upper_hsv[0] = value

def update_upper_hsv_saturation(value):
    upper_hsv[1] = value

def update_upper_hsv_value(value):
    upper_hsv[2] = value

# Create a VideoCapture object to capture video from the default camera (0)
cap = cv2.VideoCapture(0)

# Create a window to display the camera feed
cv2.namedWindow('Camera Feed')

# Create trackbars to adjust lower and upper HSV values
cv2.createTrackbar('Lower H', 'Camera Feed', lower_hsv[0], 180, update_lower_hsv_hue)
cv2.createTrackbar('Lower S', 'Camera Feed', lower_hsv[1], 255, update_lower_hsv_saturation)
cv2.createTrackbar('Lower V', 'Camera Feed', lower_hsv[2], 255, update_lower_hsv_value)

cv2.createTrackbar('Upper H', 'Camera Feed', upper_hsv[0], 180, update_upper_hsv_hue)
cv2.createTrackbar('Upper S', 'Camera Feed', upper_hsv[1], 255, update_upper_hsv_saturation)
cv2.createTrackbar('Upper V', 'Camera Feed', upper_hsv[2], 255, update_upper_hsv_value)

while True:
    # Capture a frame from the video stream
    ret, frame = cap.read()

    if not ret:
        break

    # Convert the frame to the HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create lower and upper HSV arrays based on the trackbar values
    lower = np.array(lower_hsv)
    upper = np.array(upper_hsv)

    # Create a mask using the lower and upper HSV values
    mask = cv2.inRange(hsv, lower, upper)

    # Apply the mask to the original frame
    result = cv2.bitwise_and(frame, frame, mask=mask)
    result = cv2.flip(result,1)
    # Display the resulting frame with the applied mask
    cv2.imshow('Camera Feed', result)

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
print("selcted values", lower, upper)
# This code creates sliders for adjusting the lower and upper HSV values (Hue, Saturation, and Value) interactively. You can adjust these values using the sliders in real-time while viewing the camera feed. Press 'q' to exit the video stream.





