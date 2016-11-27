import cv2
import numpy as np
import math

def get_houghtr(source):
    height, width = source.shape[:2]
    thr = min(height / 2, width / 2)
    diagonal = math.sqrt(pow(height, 2) + pow(width, 2))
    coordinates = []
    edges = cv2.Canny(source, 50, 150, apertureSize = 3)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, int(thr))
    # lines = cv2.HoughLines(edges, 1, np.pi / 180, 500)
    for line in lines:
        rho, theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        '''
        x1 = int(x0 + diagonal * (-b))
        if x1 < 0: x1 = 0
        if x1 > width: x1 = width
        y1 = int(y0 + diagonal * (a))
        if y1 < 0: y1 = 0
        if y1 > height: y1 = height
        x2 = int(x0 - diagonal * (-b))
        if x2 < 0: x2 = 0
        if x2 > width: x2 = width
        y2 = int(y0 - diagonal * (a))
        if y2 < 0: y2 = 0
        if y2 > height: y2 = height

        d_slope = ''
        slope_under = x2 - x1
        slope = None
        if slope_under != 0:
            slope = abs((y2-y1)/slope_under)
            if slope < 0.1:
                d_slope = 'h'
            elif slope > 10:
                d_slope = 'v'
        else:
            d_slope = 'v'

        if d_slope == 'h' or d_slope == 'v':
            coordinates.append((d_slope, (x1, y1), (x2, y2), slope))'''

        # print(str(x0) + ' ' + str(y0))
        d_slope = ''
        slope = 0
        if x0 <= 0:
            x1 = 0
            y1 = int(y0)
            x2 = width - 1
            y2 = int(y0)
            d_slope = 'h'
        if y0 <= 0:
            x1 = int(x0)
            y1 = 0
            x2 = int(x0)
            y2 = height - 1
            d_slope = 'v'
            slope = 1

        # print(str(x1) + ' ' + str(y1) + ' , ' + str(x2) + ' ' + str(y2))

        coordinates.append((d_slope, (x1, y1), (x2, y2), slope))

    return coordinates