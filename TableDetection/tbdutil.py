from urllib.request import urlopen
import numpy as np
import cv2
from matplotlib import pyplot as plt
import base64
from io import BytesIO
from PIL import Image


def url_to_image(url):
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    resp = urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype='uint8')
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    # return the image
    return image


def get_intersecting_point(l1, l2):
    x1 = l1[0][0]
    y1 = l1[0][1]
    x2 = l1[1][0]
    y2 = l1[1][1]
    x3 = l2[0][0]
    y3 = l2[0][1]
    x4 = l2[1][0]
    y4 = l2[1][1]

    under_t = ((y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1))
    if under_t == 0:
        return 'error', None, None

    t = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / under_t
    s = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / under_t

    if s < 0 or 1 < s or t < 0 or 1 < t:
        return 'error', None, None

    px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / (
        (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
    py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / (
        (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))

    return 'ok', px, py


def get_num_v(lines):
    cnt = 0
    for l in lines:
        if l[0] == 'v':
            cnt += 1

    return cnt


def get_num_h(lines):
    cnt = 0
    for l in lines:
        if l[0] == 'h':
            cnt += 1

    return cnt


def get_v_lines(lines, width):
    v_lines = []
    for l in lines:
        if l[0] == 'v':
            p1 = l[1]
            p2 = l[2]
            if p1[1] > p2[1]:
                p1 = l[2]
                p2 = l[1]

            if len(v_lines) == 0:
                v_lines.append((p1, p2))
            else:
                wasInserted = False
                for i in range(len(v_lines)):
                    if p1[0] <= v_lines[i][0][0]:
                        v_lines.insert(i, (p1, p2))
                        wasInserted = True
                        break

                if not wasInserted:
                    v_lines.append((p1, p2))

    return v_lines


def get_h_lines(lines, height):
    h_lines = []
    for l in lines:
        if l[0] == 'h':
            p1 = l[1]
            p2 = l[2]
            if p1[0] > p2[0]:
                p1 = l[2]
                p2 = l[1]

            if len(h_lines) == 0:
                h_lines.append((p1, p2))
            else:
                wasInserted = False
                for i in range(len(h_lines)):
                    if p1[1] <= h_lines[i][0][1]:
                        h_lines.insert(i, (p1, p2))
                        wasInserted = True
                        break

                if not wasInserted:
                    h_lines.append((p1, p2))

    return h_lines


def to_cv2(pil_image):
    return np.asarray(pil_image)


def show_img_plot(cv2_img, gray=False):
    plt.xticks([]), plt.yticks([])
    if gray:
        plt.imshow(cv2_img, 'gray')
    else:
        plt.imshow(cv2_img)
    plt.show()


def readb64(base64_string):
    sbuf = BytesIO()
    sbuf.write(base64.b64decode(base64_string))
    pimg = Image.open(sbuf)

    return cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)
