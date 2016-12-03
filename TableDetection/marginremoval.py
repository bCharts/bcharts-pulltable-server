import copy


def get_margin(bi_img):
    height, width = bi_img.shape[:2]

    h_lines = []
    blank_row_start_idx = -1
    blank_row_finish_idx = -1
    for y in range(height):
        black_found = 0
        for x in range(width):
            if bi_img[y, x] == 0:
                black_found += 1

        if black_found == 0:
            if blank_row_start_idx == -1:
                blank_row_start_idx = y
        else:
            if blank_row_start_idx != -1:
                blank_row_finish_idx = y - 1

        if blank_row_start_idx != -1 and blank_row_finish_idx != -1:
            g_y = int((blank_row_finish_idx - blank_row_start_idx) / 2) + blank_row_start_idx
            g_x1, g_x2 = 0, width - 1
            h_lines.append(((g_x1, g_y), (g_x2, g_y)))
            blank_row_start_idx = -1
            blank_row_finish_idx = -1

        if blank_row_start_idx != -1 and y == height - 1 and x == width - 1:
            blank_row_finish_idx = y
            g_y = int((blank_row_finish_idx - blank_row_start_idx) / 2) + blank_row_start_idx
            g_x1, g_x2 = 0, width - 1
            h_lines.append(((g_x1, g_y), (g_x2, g_y)))

    v_lines = []
    blank_col_start_idx = -1
    blank_col_finish_idx = -1
    for x in range(width):
        black_found = 0
        for y in range(height):
            if bi_img[y, x] == 0:
                black_found += 1

        if black_found == 0:
            if blank_col_start_idx == -1:
                blank_col_start_idx = x
        else:
            if blank_col_start_idx != -1:
                blank_col_finish_idx = x

        if blank_col_start_idx != -1 and blank_col_finish_idx != -1:
            g_x = int((blank_col_finish_idx - blank_col_start_idx) / 2) + blank_col_start_idx
            g_y1, g_y2 = 0, height - 1
            v_lines.append(((g_x, g_y1), (g_x, g_y2)))
            blank_col_start_idx = -1
            blank_col_finish_idx = -1

        if blank_col_start_idx != -1 and y == height - 1 and x == width - 1:
            blank_col_finish_idx = x
            g_x = int((blank_col_finish_idx - blank_col_start_idx) / 2) + blank_col_start_idx
            g_y1, g_y2 = 0, height - 1
            v_lines.append(((g_x, g_y1), (g_x, g_y2)))

    # 상하 자르기
    y1 = None
    y2 = None
    if len(h_lines) >= 2:
        first_h_line, last_h_line = h_lines[0], h_lines[len(h_lines) - 1]
        y1 = first_h_line[0][1]
        y2 = last_h_line[0][1]

    # 좌우 자르기
    x1 = None
    x2 = None
    if len(v_lines) >= 2:
        first_v_line, last_v_line = v_lines[0], v_lines[len(v_lines) - 1]
        x1 = first_v_line[0][0]
        x2 = last_v_line[0][0]

    return {
        'top': y1,
        'bottom': y2,
        'left': x1,
        'right': x2
    }


def remove_margin(image, margin):
    ret_img = image

    if margin['top'] is not None and margin['bottom'] is not None:
        ret_img = ret_img[:margin['bottom'], 0:]
        ret_img = ret_img[margin['top']:, 0:]

    if margin['left'] is not None and margin['right'] is not None:
        ret_img = ret_img[0:, :margin['right']]
        ret_img = ret_img[0:, margin['left']:]

    return ret_img
