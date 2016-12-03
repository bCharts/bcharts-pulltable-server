import cv2
import numpy as np
import math
from settingsmanager import get_settings


def get_houghtr(source):
    hough_v_thr_ratio = float(get_settings('hough_v_thr_ratio'))
    hough_h_thr_ratio = float(get_settings('hough_h_thr_ratio'))

    height, width = source.shape[:2]
    v_thr = int(height * hough_v_thr_ratio)
    h_thr = int(width * hough_h_thr_ratio)
    diagonal = math.sqrt(pow(height, 2) + pow(width, 2))
    coordinates = []
    edges = cv2.Canny(source, 50, 150, apertureSize=3)

    lines = cv2.HoughLines(edges, 1, np.pi / 180, v_thr)
    for line in lines:
        rho, theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho

        x1 = int(x0 + diagonal * (-b))
        if x1 < 0: x1 = 0
        if x1 > width: x1 = width
        y1 = int(y0 + diagonal * a)
        if y1 < 0: y1 = 0
        if y1 > height: y1 = height
        x2 = int(x0 - diagonal * (-b))
        if x2 < 0: x2 = 0
        if x2 > width: x2 = width
        y2 = int(y0 - diagonal * a)
        if y2 < 0: y2 = 0
        if y2 > height: y2 = height

        slope_under = x2 - x1
        slope_over = y2 - y1
        if slope_under == 0:
            d_slope = 'v'
        elif slope_over == 0:
            d_slope = 'h'
        else:
            slope = abs((y2 - y1) / slope_under)
            if slope < 0.1:
                d_slope = 'h'
                y2 = y1
            else:
                d_slope = 'v'
                x2 = x1

        if d_slope == 'v':
            coordinates.append((d_slope, [x1, y1], [x2, y2]))

    lines = cv2.HoughLines(edges, 1, np.pi / 180, h_thr)
    for line in lines:
        rho, theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho

        x1 = int(x0 + diagonal * (-b))
        if x1 < 0: x1 = 0
        if x1 > width: x1 = width
        y1 = int(y0 + diagonal * a)
        if y1 < 0: y1 = 0
        if y1 > height: y1 = height
        x2 = int(x0 - diagonal * (-b))
        if x2 < 0: x2 = 0
        if x2 > width: x2 = width
        y2 = int(y0 - diagonal * a)
        if y2 < 0: y2 = 0
        if y2 > height: y2 = height

        slope_under = x2 - x1
        slope_over = y2 - y1
        if slope_under == 0:
            d_slope = 'v'
        elif slope_over == 0:
            d_slope = 'h'
        else:
            slope = abs((y2 - y1) / slope_under)
            if slope < 0.1:
                d_slope = 'h'
                y2 = y1
            else:
                d_slope = 'v'
                x2 = x1

        if d_slope == 'h':
            coordinates.append((d_slope, [x1, y1], [x2, y2]))

    return coordinates
