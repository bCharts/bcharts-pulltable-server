import cv2
import numpy as np
import math
from settingsmanager import get_settings

def get_houghtr(source):
    m_thr = False
    if get_settings('hough_manual_thr') == 'TRUE':
        m_thr = True
    m_thr_val = float(get_settings('hough_manual_thr_val'))

    height, width = source.shape[:2]
    thr = min(height / 2, width / 2)
    diagonal = math.sqrt(pow(height, 2) + pow(width, 2))
    coordinates = []
    edges = cv2.Canny(source, 50, 150, apertureSize = 3)

    if m_thr:
        lines = cv2.HoughLines(edges, 1, np.pi / 180, m_thr_val)
    else:
        lines = cv2.HoughLines(edges, 1, np.pi / 180, int(thr))

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
            slope = abs((y2-y1)/slope_under)
            if slope < 0.1:
                d_slope = 'h'
                y2 = y1
            else:
                d_slope = 'v'
                x2 = x1

        coordinates.append((d_slope, [x1, y1], [x2, y2]))

        '''
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
            slope = 1'''

        # print('x0: ' + str(x0) + ' , y0: ' + str(y0) + ' , slop: ' + str(d_slope) + ' , x1: ' + str(x1) + ' , y1: ' + str(y1) + ' , x2: ' + str(x2) + ' , y2: ' + str(y2))

        # coordinates.append((d_slope, [x1, y1], [x2, y2], slope))

    return coordinates