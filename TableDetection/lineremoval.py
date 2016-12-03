from pprint import pprint
from settingsmanager import get_settings

def remove_extra_hlines(h_lines, img_height):
    gap_allowed = float(get_settings('hline_gap'))

    i = 0
    while i < len(h_lines) - 1:
        gap = h_lines[i+1][0][1] - h_lines[i][0][1]
        if gap / img_height <= gap_allowed:
            h_lines[i][0][1] += gap
            del h_lines[i+1]
            i -= 1
        i += 1



def remove_extra_vlines(v_lines, img_width):
    gap_allowed = float(get_settings('vline_gap'))

    i = 0
    while i < len(v_lines) - 1:
        gap = v_lines[i+1][0][0] - v_lines[i][0][0]
        if gap / img_width <= gap_allowed:
            v_lines[i][0][0] += gap
            del v_lines[i+1]
            i -= 1
        i += 1