from pprint import pprint
import threading

def compare_pattern(org_img, offset_x, offset_y, pattern):
    if org_img.size[0] < offset_x + pattern.size[0] or org_img.size[1] < offset_y + pattern.size[1]:
        return 0

    n_equal = 0
    pattern_size = pattern.size[0] * pattern.size[1]

    org_pxs = org_img.load()
    pt_width, pt_height = pattern.size
    pt_px = pattern.load()

    for y in range(0, pt_height):
        for x in range(0, pt_width):
            org_px = 0
            if org_pxs[offset_x + x, offset_y + y] == 255:
                org_px = 1
            if pt_px[x,y] == org_px:
                n_equal += 1

    return n_equal / pattern_size


def compare_seg_pattern(comment, image, offset, pattern):
    corners = []

    for y in range(offset[1], offset[1] + offset[3]):
        limit_y = offset[1] + offset[3]
        for x in range(offset[0], offset[0] + offset[2]):
            limit_x = offset[0] + offset[2]

            equal_rate = compare_pattern(image, x, y, pattern)
            if equal_rate > 0.98:
                # print('limit : ' + str(limit_x) + ', ' + str(limit_y))
                print(comment + '-> ' + str(x) + ',' + str(y) + ' : ' + str(equal_rate))
                corners.append((x, y))

    return corners


def get_segments(width, height, n_units):

    c_unit = int(width / n_units)
    r_unit = int(height / n_units)

    segments = []
    for r in range(n_units):
        for c in range(n_units):
            offset_x = c * c_unit + c
            offset_y = r * r_unit + r
            offset_width = c_unit
            offset_height = r_unit
            if offset_x + c_unit > width:
                offset_width = width - offset_x
            if offset_y + r_unit > height:
                offset_height = height - offset_y
            segments.append((offset_x, offset_y, offset_width, offset_height))

    return segments


class PatternComparing(threading.Thread):
    image = None
    offset = None
    pattern = None
    corners = None
    th_name = None

    def __init__(self, t_name, image, offset, pattern):
        super(PatternComparing, self).__init__()
        self.image = image
        self.offset = offset
        self.pattern = pattern
        self.th_name = t_name

    def run(self):
        self.corners = compare_seg_pattern(self.th_name, self.image, self.offset, self.pattern)

    def get_corners(self):
        return self.corners


class TableCellDetecting(threading.Thread):
    image = None
    offset = None
    pattern = None
    corners = None
    th_name = None

    def __init__(self, t_name, image, offset, pattern):
        super(PatternComparing, self).__init__()
        self.image = image
        self.offset = offset
        self.pattern = pattern
        self.th_name = t_name
