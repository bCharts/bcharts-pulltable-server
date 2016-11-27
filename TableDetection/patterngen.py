from PIL import Image

def create_pattern(dr, p_width, l_width):
    pt_width = p_width
    pt_line_width = l_width

    eg_left_top = Image.new('1', (pt_width, pt_width), color=1)
    px = eg_left_top.load()

    if dr == 'tl':
        for r in range(0, pt_line_width):
            for c in range(0, pt_width):
                px[c,r] = 0

        for r in range(0, pt_width):
            for c in range(0, pt_line_width):
                px[c,r] = 0

    if dr == 'tr':
        for r in range(0, pt_line_width):
            for c in range(0, pt_width):
                px[c,r] = 0

        for r in range(0, pt_width):
            for c in range(pt_width - pt_line_width - 1, pt_width):
                px[c,r] = 0

    if dr == 'bl':
        for r in range(0, pt_width):
            for c in range(0, pt_line_width):
                px[c,r] = 0

        for r in range(pt_width - pt_line_width - 1, pt_width):
            for c in range(0, pt_width):
                px[c,r] = 0

    if dr == 'br':
        for r in range(0, pt_width):
            for c in range(pt_width - pt_line_width - 1, pt_width):
                px[c,r] = 0

        for r in range(pt_width - pt_line_width - 1, pt_width):
            for c in range(0, pt_width):
                px[c,r] = 0

    return eg_left_top