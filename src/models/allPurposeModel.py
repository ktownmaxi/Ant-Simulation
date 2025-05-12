import pygame

from src.models.areaOperator import AreaOperator
from src.models.gridModel import GridModel


class AllPurposeModel(GridModel):
    def __init__(self, rows, cols, cell_size, line_color, colony_color, food_color, starting_zoom_factor, min_zoom,
                 max_zoom, granularity_threshold=0.6):
        super().__init__(rows, cols)
        self.data = self.build_numpy_model()
        self.cell_size = cell_size
        self.line_color = line_color

        self.colony_color = colony_color
        self.food_color = food_color

        self.granularity_threshold = granularity_threshold

        self.zoom_factor = starting_zoom_factor
        self.min_zoom, self.max_zoom = min_zoom, max_zoom
        self.offset_x, self.offset_y = 0, 0

        self.normal_width = 1
        self.outer_width = 3

        self.show_to_colony_markers = False
        self.show_to_food_markers = True

        self.colony_pos = ()

    def get_absolute_position_data_of_cell(self, row: int, col: int):
        """
        Returns the data of a cell
        :param row: integer that describes the row
        :param col: integer that describes the column
        :return:
        """
        cell_x = self.offset_x + col * self.cell_size * self.zoom_factor
        cell_y = self.offset_y + row * self.cell_size * self.zoom_factor
        cell_w = self.cell_size * self.zoom_factor
        cell_h = self.cell_size * self.zoom_factor

        return cell_x, cell_y, cell_w, cell_h

    def draw(self, surface: pygame.Surface):
        cell_size_zoom = self.cell_size * self.zoom_factor
        # True size of grid
        grid_width = self.cols * cell_size_zoom
        grid_height = self.rows * cell_size_zoom

        granularity = 1 if self.zoom_factor >= self.granularity_threshold else 2

        # horizontal lines
        for row in range(0, self.rows + 1, granularity):
            y = self.offset_y + row * cell_size_zoom
            start_x = self.offset_x
            end_x = self.offset_x + grid_width
            lw = self.outer_width if row == 0 or row == self.rows else self.normal_width
            pygame.draw.line(surface, self.line_color, (start_x, y), (end_x, y), lw)

        # vertical lines
        for col in range(0, self.cols + 1, granularity):
            x = self.offset_x + col * cell_size_zoom
            start_y = self.offset_y
            end_y = self.offset_y + grid_height
            lw = self.outer_width if col == 0 or col == self.cols else self.normal_width
            pygame.draw.line(surface, self.line_color, (x, start_y), (x, end_y), lw)

        # render all colored cells
        base_rect = pygame.Rect(0, 0, cell_size_zoom + 1, cell_size_zoom + 1)
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.data[row, col]
                x = self.offset_x + col * cell_size_zoom
                y = self.offset_y + row * cell_size_zoom
                rect = base_rect.move(x, y)

                changed = False

                if cell['colony'] == 1:
                    color = self.colony_color
                    changed = True
                elif cell['food'] == 1:
                    color = self.food_color
                    changed = True
                elif cell['toColony'] and self.show_to_colony_markers:
                    color = (0, 0, 255)
                    changed = True
                elif cell['toFood'] and self.show_to_food_markers:
                    color = (209, 134, 0)
                    rect.size = (cell_size_zoom, cell_size_zoom)
                    changed = True

                if changed:
                    pygame.draw.rect(surface, color, rect)


    def zoom(self, mouse_pos: tuple[int, int], zoom_in=True):
        mouse_x, mouse_y = mouse_pos
        old_zoom = self.zoom_factor

        if zoom_in:
            self.zoom_factor = min(self.max_zoom, self.zoom_factor * 1.1)
        else:
            self.zoom_factor = max(self.min_zoom, self.zoom_factor / 1.1)

        scale = self.zoom_factor / old_zoom
        self.offset_x = mouse_x - (mouse_x - self.offset_x) * scale
        self.offset_y = mouse_y - (mouse_y - self.offset_y) * scale

    def pan(self, dx: int, dy: int):
        """
        Updates offset in the grid object
        """
        self.offset_x += dx
        self.offset_y += dy

    def mark_colony(self, mouse_pos: tuple[int, int], radius: int):
        """
        Marks a circle of radius radius on the grid by placing 1 s in the numpy model
        Used to place the colony
        """
        mouse_x, mouse_y = mouse_pos
        col_center = int((mouse_x - self.offset_x) / (self.cell_size * self.zoom_factor))
        row_center = int((mouse_y - self.offset_y) / (self.cell_size * self.zoom_factor))

        if self.colony_pos == ():
            # Iterate over a Quadrat with dx radius and dy radius
            for row in range(row_center - radius, row_center + radius + 1):
                for col in range(col_center - radius, col_center + radius + 1):
                    # Check if point in board
                    if 0 <= row < self.rows and 0 <= col < self.cols:
                        # Check if cell is in circle radius
                        if (row - row_center) ** 2 + (col - col_center) ** 2 <= radius ** 2:
                            self.data[row, col]['colony'] = 1

            self.colony_pos = (row_center, col_center)

    def get_colony_border(self, circle_center: tuple[int, int], radius: int):
        """
        Calculates all cells, which are outside the circle but have a connection to the circle.
        Returns:
            a list of tuples (row, col) of the border cells.
        """
        (row_center, col_center) = circle_center

        border_cells = []
        # iterate over rect of radius + 2
        for row in range(row_center - radius - 1, row_center + radius + 2):
            for col in range(col_center - radius - 1, col_center + radius + 2):
                # checks if cell in grid
                if 0 <= row < self.rows and 0 <= col < self.cols:
                    # cell is outside the circle
                    if (row - row_center) ** 2 + (col - col_center) ** 2 > radius ** 2:
                        # checks all neighbor cells (inc. diagonals)
                        for d_row in (-1, 0, 1):
                            for d_col in (-1, 0, 1):
                                if d_row == 0 and d_col == 0:
                                    continue  # current cell
                                n_row = row + d_row
                                n_col = col + d_col
                                # checks if the neighbor cell is outside the grid
                                if 0 <= n_row < self.rows and 0 <= n_col < self.cols:
                                    # checks if the neighbor cell is inside the circle
                                    if (n_row - row_center) ** 2 + (n_col - col_center) ** 2 <= radius ** 2:
                                        border_cells.append((row, col))
                                        # a valid neighbor cell is found
                                        break
                            else:
                                continue
                            break

        return border_cells

    def mark_food(self, mouse_pos: tuple[int, int], radius: int):
        """
        Marks a circle of radius radius on the grid by placing 1 s in the numpy model
        Used to place the food for the colony
        """
        mouse_x, mouse_y = mouse_pos
        col_center = int((mouse_x - self.offset_x) / (self.cell_size * self.zoom_factor))
        row_center = int((mouse_y - self.offset_y) / (self.cell_size * self.zoom_factor))

        # Iterate over a Quadrat with dx radius and dy radius
        for row in range(row_center - radius, row_center + radius + 1):
            for col in range(col_center - radius, col_center + radius + 1):
                # Check if point in board
                if 0 <= row < self.rows and 0 <= col < self.cols:
                    # Check if cell is in circle radius
                    if (row - row_center) ** 2 + (col - col_center) ** 2 <= radius ** 2:
                        if self.data[row, col] != 1:
                            self.data[row, col]['food'] = 1

    def place_to_home_marker(self, pos: tuple[int, int], value: float):
        self.data[*pos]['toColony'].append(value)

    def place_to_food_marker(self, pos: tuple[int, int], value: float):
        self.data[*pos]['toFood'].append(value)

    def get_visible_field(self, pos: tuple[int, int]):
        """
        Method to get an array with the values that can be seen from that position
        :param pos: grid position
        :return: array with the visible area
        """
        visibleArea = []
        rows = [pos[0] - 1, pos[0], pos[0] + 1]
        for i in range(len(rows)):
            row = self.data[rows[i]]
            left = pos[1] - 1 if pos[1] - 1 >= 0 else None
            right = pos[1] + 1 if pos[1] + 1 < len(row) else None
            visibleArea.append(row[left:right + 1])

        area = AreaOperator(visibleArea, self)

        return area
