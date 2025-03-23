import numpy as np


class GridModel:
    def __init__(self, rows, cols, default_value=0):
        self.rows = rows
        self.cols = cols
        self.default_value = default_value
        self.data = self.build_numpy_model()

    def __str__(self):
        return str(self.data)

    def build_numpy_model(self):
        grid_model = np.zeros((self.rows, self.cols), dtype=object)
        for i in range(self.rows):
            for j in range(self.cols):
                grid_model[i, j] = {
                    'food': 0,
                    'colony': 0,
                    'toFood': [],
                    'toColony': []
                }
        return grid_model

    def get_cell(self, row, col):
        return self.data[row, col]

    def mark_cell(self, row, col, value=1):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.data[row, col] = value

    def getDimensions(self):
        return self.rows, self.cols
