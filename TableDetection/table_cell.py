
class Cell:
    loc = (0, 0)
    size = (0, 0)

    contents = ''

    def __init__(self, loc, size):
        self.loc = loc
        self.size = size

    def add_text(self, text):
        self.contents += ' ' + text

    def validate_point_contained(self, pt):
        if self.loc[0] <= pt[0] <= self.loc[0] + self.size[0]:
            if self.loc[1] <= pt[1] <= self.loc[1] + self.size[1]:
                return True

        return False

    def get_text(self):
        return self.contents

    def get_location(self):
        return self.loc

    def get_width(self):
        return self.size[0]

    def get_height(self):
        return self.size[1]

    def get_left(self):
        return self.loc[0]

    def get_top(self):
        return self.loc[1]

    def get_pt1(self):
        return self.get_location()

    def get_pt2(self):
        return self.get_left() + self.get_width(), self.get_top() + self.get_height()