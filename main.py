import cv2
import os
import numpy as np
import time
import math
from centroid_tracker import CentroidTracker
from collections import deque
from utils import *


# intialize the color which we want to detect
color_ranges = {
    "Red": [[156, 48, 128], [180, 255, 243]],
    "Yellow": [[15, 94, 108], [161, 207, 203]],
    "Orange": [[5, 148, 122], [14, 225, 255]],
    "Green": [
        [54, 64, 61],
        [89, 255, 112],
    ],  # "Light Blue":[[81, 41, 130],[117, 255, 242]],
    "Pen": [[76, 77, 31], [116, 255, 183]],
}

# Create a VideoCapture object to capture video from the default camera (0)
cap = cv2.VideoCapture(0)
tracker = CentroidTracker(max_distance=50)

# initial veriabels
area_list = {}
draw_rect = True
fps_rate = 3

while True:
    # Capture a frame from the video stream
    ret, frame = cap.read()

    if not ret:
        print("The video has No frames")
        break

    # Flip the frame
    frame = cv2.flip(frame, 1)

    # Draw the area in which we want to perform the detection
    if draw_rect:
        rectangle = impliment_draw_rect(frame)
        start_x, start_y, end_x, end_y = rectangle
        draw_rect = False

    # Define start time to set the fps rate
    start_time = time.time()

    image = frame
    # change the color mode
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Create a blanck frame
    blank_frame = np.zeros(frame.shape)
    # Past the rectangular area on blank frame
    blank_frame[start_y:end_y,start_x:end_x] = hsv[start_y:end_y,start_x:end_x]

    contor_dict = {}
    # Loop throught the colors
    for colors_name in color_ranges.keys():
        # Select particular color
        color = color_ranges[colors_name]

        # Define lower and upper bounds for red color in HSV
        lower_red = np.array(color[0])
        upper_red = np.array(color[1])

        # Create a mask for red pixels
        mask = cv2.inRange(blank_frame, lower_red, upper_red)

        # Apply morphological operations to the mask
        erosion_kernel = np.ones((5, 5), np.uint8)
        dilation_kernal = np.ones((13, 13), np.uint8)

        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, erosion_kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, dilation_kernal)

        # Apply Canny edge detection
        edges = cv2.Canny(mask, threshold1=50, threshold2=100)

        # Find contors and return bounding boxes
        bounding_box, area = find_contours(edges)

        contor_dict[area] = bounding_box, colors_name

    # Take only max area contour
    max_area = max(contor_dict.keys())
    centroids = contor_dict[max_area][0][:2]
    # Draw center of the object
    cv2.circle(image, centroids, 5, (255, 255, 255), -1)
    # Check if the object is in the rectangle
    if check_int_rect(rectangle=rectangle, centroid=centroids):

        centroid = contor_dict[max_area][0]

        # Update tracker based on centroid
        tracker_dict = tracker.update([centroid])

        # To check on which object we have do further analysis
        for ids in tracker_dict.keys():

            # calculate area of the box
            area = tracker_dict[ids][0][-2] * tracker_dict[ids][0][-1]

            if ids not in area_list.keys():
                area_list[ids] = deque(maxlen=3)
                area_list[ids].append(area)
            else:
                area_list[ids].append(area)

        unused_ids = []
        # Remove the objects if those are not in frame
        for ids in area_list.keys():
            if ids not in tracker_dict.keys():
                unused_ids.append(ids)
        for ids in unused_ids:
            area_list.pop(ids)

        # Now check if the object is getting closer or moving away
        for ids in area_list.keys():

            areas = area_list[ids]
            label = ""
            area_diffrence = areas[-1] - areas[0]

            if area_diffrence > 100:
                label = "object is moving closer"

            if area_diffrence < -100:
                label = "object is moving away"            
        # Draw centorid label
        image = draw(contor_dict[max_area], image, label)

    # Draw rectangle which we have created
    cv2.rectangle(image, (start_x, start_y), (end_x, end_y), (0, 0, 255), 2)

    # Display the result
    cv2.imshow("orignal pencil", image)
    # cv2.imshow('Red Panicle', red_panicle)
    if cv2.waitKey(1) == ord("q"):
        break

    sleep_time = 1 / (fps_rate - (time.time() - start_time))
    time.sleep(sleep_time)
cv2.destroyAllWindows()
