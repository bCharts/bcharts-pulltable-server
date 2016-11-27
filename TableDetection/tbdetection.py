import cv2
from matplotlib import pyplot as plt
import TableDetection.houghtr as houghtr
import copy
import TableDetection.tbdutil as util
from pprint import pprint
import random
import TableDetection.guideaddition as guideaddition
import TableDetection.lineremoval as lineremoval
import TableDetection.googlevision as googlevision
from TableDetection.table_cell import Cell

def get_csv(cv2_image):
    # org_img = cv2.imread('C:\\Users\\bruce\\Desktop\\ex\\134513245.PNG')
    org_img = cv2.resize(cv2_image, (0,0), fx=2, fy=2)
    height, width = org_img.shape[:2]
    print(width, height)

    gray_img = cv2.cvtColor(org_img, cv2.COLOR_RGB2GRAY)
    result_gt_img = copy.copy(org_img)
    ret1, th1 = cv2.threshold(gray_img, 200, 255, cv2.THRESH_BINARY)
    guideaddition.add_guideline(th1)
    # plt.imshow(th1, 'gray')
    # plt.show()

    lines = houghtr.get_houghtr(th1)
    # n_cols = util.get_num_v(lines) - 1
    # n_rows = util.get_num_h(lines) - 1
    # print('number of cols: ' + str(n_cols))
    # print('number of rows: ' + str(n_rows))

    v_lines = util.get_v_lines(lines)
    lineremoval.remove_extra_vlines(v_lines, width)
    h_lines = util.get_h_lines(lines)
    lineremoval.remove_extra_hlines(h_lines, height)

    # pprint(v_lines)

    tl_coords = []
    for r_line in h_lines:
        r_coords = []
        for c_line in v_lines:
            coor_inter = util.get_intersecting_point(r_line, c_line)
            if coor_inter[0] == 'ok':
                r_coords.append(coor_inter[1:])
                # cv2.circle(result_gt_img, coor_inter[1:], 5, (0,255,0), 3)
        tl_coords.append(r_coords)

    cells = []
    for r_idx in range(len(tl_coords)-1):
        r_cells = []
        for c_idx in range(len(tl_coords[r_idx])-1):
            cell_width = tl_coords[r_idx][c_idx+1][0] - tl_coords[r_idx][c_idx][0] - 1
            cell_height = tl_coords[r_idx+1][c_idx][1] - tl_coords[r_idx][c_idx][1] - 1
            cell = Cell(tl_coords[r_idx][c_idx], (cell_width, cell_height))
            r_cells.append(cell)
        cells.append(r_cells)

    gv_result = googlevision.analyze_image(org_img)
    if len(gv_result['textAnnotations']) > 2:
        for word in gv_result['textAnnotations'][1:]:
            l1 = ((word['boundingPoly']['vertices'][0]['x'], word['boundingPoly']['vertices'][0]['y']), (word['boundingPoly']['vertices'][2]['x'], word['boundingPoly']['vertices'][2]['y']))
            l2 = ((word['boundingPoly']['vertices'][1]['x'], word['boundingPoly']['vertices'][1]['y']), (word['boundingPoly']['vertices'][3]['x'], word['boundingPoly']['vertices'][3]['y']))
            ret, cx, cy = util.get_intersecting_point(l1, l2)
            if ret == 'ok':
                for r_cells in cells:
                    for cell in r_cells:
                        if cell.validate_point_contained((cx, cy)):
                            cell.add_text(word['description'])
                            print(word['description'] + ' is added')

    final_csv = ''
    for r_cells in cells:
        for cell in r_cells:
            final_csv += '"' + cell.get_text() + '",'
        final_csv = final_csv[:-1] + '\n'


    for r_cells in cells:
        for cell in r_cells:
            rgb = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
            cv2.rectangle(result_gt_img, cell.get_pt1(), cell.get_pt2(), rgb, 1)

    # plt.xticks([]), plt.yticks([])
    # plt.imshow(result_gt_img)
    # plt.show()

    return final_csv