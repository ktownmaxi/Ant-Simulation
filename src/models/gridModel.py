import numpy as np


class GridModel:
    def __init__(self, rows, cols, default_value=0):
        self.rows = rows
        self.cols = cols
        self.default_value = default_value
        self.data = np.zeros((rows, cols), dtype=object)

    def __str__(self):
        return str(self.data)

    def get_cell(self, row, col):
        return self.data[row, col]

    def mark_cell(self, row, col, value=1):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.data[row, col] = value

    def getDimensions(self):
        return self.rows, self.cols
