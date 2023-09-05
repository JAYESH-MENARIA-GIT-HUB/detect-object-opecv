import cv2
import math
import numpy as np


# Variables to store the coordinates of the rectangle's starting and ending points
start_x, start_y = -1, -1
end_x, end_y = -1, -1
drawing = False


# Mouse callback function
def draw_rectangle(event, x, y, flags, param):
    global start_x, start_y, end_x, end_y, drawing

    if event == cv2.EVENT_LBUTTONDOWN:
        # Left mouse button pressed - start drawing the rectangle
        start_x, start_y = x, y
        end_x, end_y = x, y
        drawing = True

    elif event == cv2.EVENT_MOUSEMOVE:
        # Mouse is moved - update the ending point
        if drawing:
            end_x, end_y = x, y

    elif event == cv2.EVENT_LBUTTONUP:
        # Left mouse button released - stop drawing the rectangle
        end_x, end_y = x, y
        drawing = False


def impliment_draw_rect(image: np.array):
    # Create a window and set the mouse callback function
    cv2.namedWindow("Image")
    cv2.setMouseCallback("Image", draw_rectangle)

    while True:
        # Display the image with the current rectangle
        img_copy = image.copy()
        if not drawing:
            cv2.rectangle(img_copy, (start_x, start_y), (end_x, end_y), (0, 0, 255), 2)
        cv2.imshow("Image", img_copy)

        # Check for key press
        key = cv2.waitKey(1) & 0xFF

        # Exit when 'q' is pressed
        if key == ord("q"):
            break
    cv2.destroyAllWindows()
    return start_x, start_y, end_x, end_y


def check_int_rect(rectangle, centroid):
    start_x, start_y, end_x, end_y = rectangle
    x, y = centroid

    x_axis = start_x < x < end_x
    y_axis = start_y < y < end_y

    if x_axis and y_axis:
        return True

    return False


def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def find_contours(Edges:list):
    
    contours, _ = cv2.findContours(Edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # # Draw contours on the black background
    # image = cv2.drawContours(image, contours, -1, (0, 255, 0), 2)

    # Initialize variables to keep track of the biggest contour and its area
    max_contour = None
    max_area = 50

    # Find the biggest contour
    for contour in contours:
        # area = cv2.contourArea(contour)
        x, y, w, h = cv2.boundingRect(contour)
        area = w * h
        if area > max_area:
            max_area = area
            max_contour = contour
    x, y, w, h = cv2.boundingRect(max_contour)
    x, y = int(x + w / 2), int(y + h / 2)
    return [x, y, w, h], w * h


def draw(bounding_box: list, image: np.array, label:str):
    ''' This function is for drawing the all the necessary things'''
    x, y, w, h = bounding_box[0]
    
    # check the label of object
    text = bounding_box[1]
    if text != "Pen":
        text = f"IT IS A PENCILS"
        color = (0,255,0)
    else:
        text = f"IT IS A PEN"
        color = (255,0,0)

    # Draw center of the object
    cv2.circle(image, (x, y), 5, (255, 200, 100), -1)

    # convert to x_min, y_min
    x, y = x - w // 2, y - h // 2
    
    image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Draw object name
    image = cv2.putText(
        image,
        text,
        (20, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        color,
        2,
        cv2.LINE_AA,
    )
    # Draw object condition
    image = cv2.putText(
        image,
        label,
        (10, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 2, 55),
        2,
        cv2.LINE_AA,
    )

    return image
