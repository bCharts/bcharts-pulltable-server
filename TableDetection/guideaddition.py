import cv2
from settingsmanager import get_settings

def add_guideline(bi_img):
    vnoise = float(get_settings('allowed_vnoise'))
    hnoise = float(get_settings('allowed_hnoise'))
    hblank = float(get_settings('hblank_gap'))

    print(vnoise)
    print(hnoise)
    print(hblank)

    height, width = bi_img.shape[:2]
    lines = []

    blank_row_start_idx = -1
    blank_row_finish_idx = -1
    for y in range(height):
        black_found = 0
        for x in range(width):
            if bi_img[y,x] == 0:
                black_found += 1

        if black_found / width <= vnoise:
            if blank_row_start_idx == -1:
                blank_row_start_idx = y
        else:
            if blank_row_start_idx != -1:
                blank_row_finish_idx = y - 1

        # 라인 그리기
        if blank_row_start_idx != -1 and blank_row_finish_idx != -1:
            g_y = int((blank_row_finish_idx - blank_row_start_idx) / 2) + blank_row_start_idx
            g_x1, g_x2 = 0, width
            lines.append(((g_x1, g_y), (g_x2, g_y)))
            blank_row_start_idx = -1
            blank_row_finish_idx = -1

        if blank_row_start_idx != -1 and y == height - 1 and x == width - 1:
            blank_row_finish_idx = y
            g_y = int((blank_row_finish_idx - blank_row_start_idx) / 2) + blank_row_start_idx
            g_x1, g_x2 = 0, width
            lines.append(((g_x1, g_y), (g_x2, g_y)))


    blank_col_start_idx = -1
    blank_col_finish_idx = -1
    for x in range(width):
        black_found = 0
        for y in range(height):
            if bi_img[y, x] == 0:
                black_found += 1

        if black_found / height <= hnoise:
            if blank_col_start_idx == -1:
                blank_col_start_idx = x
        else:
            if blank_col_start_idx != -1:
                blank_col_finish_idx = x

        # 라인 그리기
        if blank_col_start_idx != -1 and blank_col_finish_idx != -1:
            gap_ratio = (blank_col_finish_idx - blank_col_start_idx) / width
            # print(gap_ratio)
            if gap_ratio >= hblank:
                g_x = int((blank_col_finish_idx - blank_col_start_idx) / 2) + blank_col_start_idx
                g_y1, g_y2 = 0, height
                lines.append(((g_x, g_y1), (g_x, g_y2)))
            blank_col_start_idx = -1
            blank_col_finish_idx = -1

        if blank_col_start_idx != -1 and y == height - 1 and x == width - 1:
            blank_col_finish_idx = x
            gap_ratio = (blank_col_finish_idx - blank_col_start_idx) / width
            # print(gap_ratio)
            if gap_ratio >= hblank:
                g_x = int((blank_col_finish_idx - blank_col_start_idx) / 2) + blank_col_start_idx
                g_y1, g_y2 = 0, height
                lines.append(((g_x, g_y1), (g_x, g_y2)))

    for line in lines:
        cv2.line(bi_img, line[0], line[1], 0, 1)

