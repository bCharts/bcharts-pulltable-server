import cv2
from matplotlib import pyplot as plt
import houghtr
import copy
import util

# org_img = cv2.imread('C:\\Users\\bruce\\Desktop\\ex\\5544.jpg')
org_img = util.url_to_image('http://www.hopestart.or.kr/wp-content/uploads/2013/01/%ED%91%9C11.jpg')
org_img = cv2.resize(org_img, (0,0), fx=2, fy=2)
height, width = org_img.shape[:2]
print(width, height)

gray_img = cv2.cvtColor(org_img, cv2.COLOR_RGB2GRAY)

# global thresholding
result_gt_img = copy.copy(org_img)
ret1, th1 = cv2.threshold(gray_img, 200, 255, cv2.THRESH_BINARY)

lines = houghtr.get_houghtr(th1)
n_cols = util.get_num_v(lines) + 1
n_rows = util.get_num_h(lines) + 1
print('number of cols: ' + str(n_cols))
print('number of rows: ' + str(n_rows))

v_lines = util.get_v_lines(lines)
print(v_lines)
h_lines = util.get_h_lines(lines)
print(h_lines)



for p in lines:
    cv2.line(result_gt_img, p[1], p[2], (255,0,0), 1)

plt.xticks([]), plt.yticks([])
plt.imshow(result_gt_img)
plt.show()