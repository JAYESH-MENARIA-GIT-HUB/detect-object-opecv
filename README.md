# Object Tracking and Image Manipulation with OpenCV

This repository contains Python code examples and explanations for performing various computer vision tasks using OpenCV. In this README, we'll summarize the tasks we've covered so far.

## Table of Contents
### Objective - 1. Detect if the object is pen or pencile.
###             2. Detect object behavior (moving away or getting closer).

- [Introduction](#introduction)
- [Requirements](#requirements)
- [Tasks](#tasks)
  - [1. Creating Rectangles with Mouse Interaction For selecting The Intresting Region](#1-creating-rectangles-with-mouse-interaction)
  - [2. Define various Color Ranges](#2-detecting-red-green-orange-blue-range)
  - [3. Detecting Color Range](#3-detecting-based-on-color-ranges)
  - [4. Used thresholding for reducing noise](#4-reduce-noise)
  - [5. Detecting Contours around Objects](#5-detecting-contours-around-detected-objects)
  - [6. Getting Bounding Boxes from Contours](#6-getting-bounding-boxes-from-contours)
  - [7. Eliminating Small Bounding Boxes](#7-eliminating-small-bounding-boxes)
  - [8. Keeping Only the Biggest Contour](#8-keeping-only-the-biggest-contour)
  - [9. Implementing a Centroid Tracker and track objects using tracker](#9-using-tracker)
  - [10. Keep track of the area object is occuping](#10-keep-track-of-the-area-object-is-occuping)
  - [11. Make decision based on the area diffrence](#11-make-decision-based-on-the-area-diffrenc)
  - [14. Draw bounding box,center point and lable](#12-draw-bounding-box,center-point-and-lable)

- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This repository provides code examples and explanations for various computer vision tasks using OpenCV in Python. These tasks include color detection, object tracking, distance calculation, and more.

## Requirements

Before running the code examples, you'll need to have the following requirements installed:

- Python (>=3.6)
- OpenCV (>=4.0)
- Numpy

You can install the required libraries using `pip`:

Credit: Jayesh Menaria
