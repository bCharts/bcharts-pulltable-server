import cv2
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
    # cv2_image = cv2.imread('C:\\Users\\bruce\\Desktop\\ex\\134513245.PNG')
    org_img = cv2.resize(cv2_image, (0, 0), fx=2, fy=2)
    step1_org_img = copy.copy(org_img)

    height, width = org_img.shape[:2]

    result_gt_img = copy.copy(org_img)

    gray_img = cv2.cvtColor(org_img, cv2.COLOR_RGB2GRAY)
    ret1, mono_img = cv2.threshold(gray_img, 200, 255, cv2.THRESH_BINARY)
    for_google_vision_img = copy.copy(mono_img)
    step2_mono_img = copy.copy(mono_img)

    guideaddition.add_guideline(mono_img)
    step3_mono_img_guide_added = copy.copy(mono_img)

    lines = houghtr.get_houghtr(mono_img)

    v_lines = util.get_v_lines(lines)
    lineremoval.remove_extra_vlines(v_lines, width)
    h_lines = util.get_h_lines(lines)
    lineremoval.remove_extra_hlines(h_lines, height)

    tl_coords = []
    for r_line in h_lines:
        r_coords = []
        for c_line in v_lines:
            r_coords.append((c_line[0][0], r_line[0][1]))
            '''
            coor_inter = util.get_intersecting_point(r_line, c_line)
            if coor_inter[0] == 'ok':
                r_coords.append((c_line[0][0], int(coor_inter[2])))

                print(coor_inter[1:], ' ', int(coor_inter[1]), ',', int(coor_inter[2]))
                cv2.circle(result_gt_img, coor_inter[1:], 5, (0,255,0), 3)'''
        tl_coords.append(r_coords)

    cells = []
    for r_idx in range(len(tl_coords) - 1):
        r_cells = []
        for c_idx in range(len(tl_coords[r_idx]) - 1):
            cell_width = tl_coords[r_idx][c_idx + 1][0] - tl_coords[r_idx][c_idx][0] - 1
            cell_height = tl_coords[r_idx + 1][c_idx][1] - tl_coords[r_idx][c_idx][1] - 1
            cell = Cell(tl_coords[r_idx][c_idx], (cell_width, cell_height))
            r_cells.append(cell)
        cells.append(r_cells)

    for r_cells in cells:
        for cell in r_cells:
            rgb = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
            cv2.rectangle(result_gt_img, cell.get_pt1(), cell.get_pt2(), rgb, 1)
    step4_table_detected = copy.copy(result_gt_img)

    gv_result = googlevision.analyze_image(mono_img)
    try:
        gv_result['textAnnotations']
    except KeyError:
        return None

    if len(gv_result['textAnnotations']) > 2:
        for word in gv_result['textAnnotations'][1:]:
            try:
                p1_x = word['boundingPoly']['vertices'][0]['x']
            except KeyError:
                p1_x = None
            try:
                p1_y = word['boundingPoly']['vertices'][0]['y']
            except KeyError:
                p1_y = None
            try:
                p3_x = word['boundingPoly']['vertices'][2]['x']
            except KeyError:
                p3_x = None
            try:
                p3_y = word['boundingPoly']['vertices'][2]['y']
            except KeyError:
                p3_y = None

            try:
                p2_x = word['boundingPoly']['vertices'][1]['x']
            except KeyError:
                p2_x = None
            try:
                p2_y = word['boundingPoly']['vertices'][1]['y']
            except KeyError:
                p2_y = None
            try:
                p4_x = word['boundingPoly']['vertices'][3]['x']
            except KeyError:
                p4_x = None
            try:
                p4_y = word['boundingPoly']['vertices'][3]['y']
            except KeyError:
                p4_y = None

            if p1_x is None:
                p1_x = p4_x
                if p4_x is None:
                    p1_x = 0
            if p1_y is None:
                p1_y = p2_y
                if p2_y is None:
                    p1_y = 0
            if p3_x is None:
                p3_x = p2_x
                if p2_x is None:
                    p3_x = p2_x
            if p3_y is None:
                p3_y = p4_y
                if p4_y is None:
                    p3_y = 0
            if p2_x is None:
                p2_x = p3_x
                if p3_x is None:
                    p3_x = 0
            if p2_y is None:
                p2_y = p1_y
                if p1_y is None:
                    p2_y = 0
            if p4_x is None:
                p4_x = p1_x
                if p1_x is None:
                    p4_x = 0
            if p4_y is None:
                p4_y = p3_y
                if p3_y is None:
                    p4_y = 0

            l1 = ((p1_x, p1_y), (p3_x, p3_y))
            l2 = ((p2_x, p2_y), (p4_x, p4_y))

            cv2.line(result_gt_img, (p1_x, p1_y), (p2_x, p2_y), (0, 255, 0), 1)
            cv2.line(result_gt_img, (p2_x, p2_y), (p3_x, p3_y), (0, 255, 0), 1)
            cv2.line(result_gt_img, (p3_x, p3_y), (p4_x, p4_y), (0, 255, 0), 1)
            cv2.line(result_gt_img, (p4_x, p4_y), (p1_x, p1_y), (0, 255, 0), 1)

            ret, cx, cy = util.get_intersecting_point(l1, l2)
            if ret == 'ok':
                for r_cells in cells:
                    for cell in r_cells:
                        if cell.validate_point_contained((cx, cy)):
                            cell.add_text(word['description'])
                            # print(word['description'] + ' is added')

    step5_words_detected = copy.copy(result_gt_img)

    final_csv = ''
    for r_cells in cells:
        for cell in r_cells:
            final_csv += '"' + cell.get_text() + '",'
            if cell.get_text() != '':
                cv2.rectangle(result_gt_img, cell.get_pt1(), cell.get_pt2(), (255, 0, 0), 2)
        final_csv = final_csv[:-1] + '\n'

    step6_final_result = copy.copy(result_gt_img)

    return (
        'ok',
        final_csv,
        [
            step1_org_img,
            step2_mono_img,
            step3_mono_img_guide_added,
            step4_table_detected,
            step5_words_detected,
            step6_final_result
        ]
    )
