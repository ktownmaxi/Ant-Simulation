import pygame
import numpy as np


class Grid:
    def __init__(self, rows, cols, cell_size, line_color):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.line_color = line_color

        self.zoom_factor = 0.4
        self.min_zoom, self.max_zoom = 0.25, 7.5
        self.offset_x, self.offset_y = 0, 0

        self.normal_width = 1
        self.outer_width = 3

        self.numpy_grid = self.build_numpy_model()

    def draw(self, surface):
        # true size of grid
        grid_width = self.cols * self.cell_size * self.zoom_factor
        grid_height = self.rows * self.cell_size * self.zoom_factor

        # Horizontal lines
        for row in range(self.rows + 1):
            y = self.offset_y + row * self.cell_size * self.zoom_factor
            start_x = self.offset_x
            end_x = self.offset_x + grid_width
            lw = self.outer_width if row == 0 or row == self.rows else self.normal_width
            pygame.draw.line(surface, self.line_color, (start_x, y), (end_x, y), lw)

        # Vertical lines
        for col in range(self.cols + 1):
            x = self.offset_x + col * self.cell_size * self.zoom_factor
            start_y = self.offset_y
            end_y = self.offset_y + grid_height
            lw = self.outer_width if col == 0 or col == self.cols else self.normal_width
            pygame.draw.line(surface, self.line_color, (x, start_y), (x, end_y), lw)

    def zoom(self, mouse_pos, zoom_in=True):
        mouse_x, mouse_y = mouse_pos
        old_zoom = self.zoom_factor

        if zoom_in:
            self.zoom_factor = min(self.max_zoom, self.zoom_factor * 1.1)
        else:
            self.zoom_factor = max(self.min_zoom, self.zoom_factor / 1.1)

        scale = self.zoom_factor / old_zoom
        self.offset_x = mouse_x - (mouse_x - self.offset_x) * scale
        self.offset_y = mouse_y - (mouse_y - self.offset_y) * scale

    def pan(self, dx, dy):
        """
        Updates offset in the grid object
        """
        self.offset_x += dx
        self.offset_y += dy

    def build_numpy_model(self):
        """
        Creates a NumPy model representing the grid.
        It's filled with zeros
        """
        grid_model = np.zeros((self.rows, self.cols), dtype=int)
        return grid_model
