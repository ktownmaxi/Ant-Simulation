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

        self.alreadyMarkedCircle = False

        self.numpy_grid = self.build_numpy_model()  # NumPy model to compute data

    def build_numpy_model(self):
        grid_model = np.zeros((self.rows, self.cols), dtype=int)
        return grid_model

    def draw(self, surface):
        # True size of grid
        grid_width = self.cols * self.cell_size * self.zoom_factor
        grid_height = self.rows * self.cell_size * self.zoom_factor

        # Zuerst alle gefärbten Zellen rendern
        for row in range(self.rows):
            for col in range(self.cols):
                if self.numpy_grid[row, col] == 1:
                    # Berechne die Position und Größe der Zelle
                    cell_x = self.offset_x + col * self.cell_size * self.zoom_factor
                    cell_y = self.offset_y + row * self.cell_size * self.zoom_factor
                    cell_w = self.cell_size * self.zoom_factor
                    cell_h = self.cell_size * self.zoom_factor
                    pygame.draw.rect(surface, (0, 255, 0), (cell_x, cell_y, cell_w, cell_h))

        # Zeichne horizontale Linien
        for row in range(self.rows + 1):
            y = self.offset_y + row * self.cell_size * self.zoom_factor
            start_x = self.offset_x
            end_x = self.offset_x + grid_width
            lw = self.outer_width if row == 0 or row == self.rows else self.normal_width
            pygame.draw.line(surface, self.line_color, (start_x, y), (end_x, y), lw)

        # Zeichne vertikale Linien
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

    def mark_circle(self, mouse_pos, radius):
        """
        Marks a circle of radius radius on the grid by placing 1s in the numpy model
        """
        mouse_x, mouse_y = mouse_pos
        col_center = int((mouse_x - self.offset_x) / (self.cell_size * self.zoom_factor))
        row_center = int((mouse_y - self.offset_y) / (self.cell_size * self.zoom_factor))

        if not self.alreadyMarkedCircle:
            # Iterate over a Quadrat with dx radius and dy radius
            for row in range(row_center - radius, row_center + radius + 1):
                for col in range(col_center - radius, col_center + radius + 1):
                    # Prüfe, ob (row, col) im Gitter liegt
                    if 0 <= row < self.rows and 0 <= col < self.cols:
                        # Check if cell is in circle radius
                        if (row - row_center) ** 2 + (col - col_center) ** 2 <= radius ** 2:
                            self.numpy_grid[row, col] = 1

            self.alreadyMarkedCircle = True
