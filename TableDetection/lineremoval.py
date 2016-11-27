from pprint import pprint

def remove_extra_hlines(h_lines, img_height):
    i = 0
    while i < len(h_lines) - 1:
        gap = h_lines[i+1][0][1] - h_lines[i][0][1]
        if gap / img_height < 0.03:
            del h_lines[i+1]
            i -= 1
        i += 1



def remove_extra_vlines(v_lines, img_width):
    i = 0
    while i < len(v_lines) - 1:
        gap = v_lines[i+1][0][0] - v_lines[i][0][0]
        if gap / img_width < 0.03:
            del v_lines[i+1]
            i -= 1
        i += 1