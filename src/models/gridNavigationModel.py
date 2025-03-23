import numpy as np
from typing import Type

from src.models.areaOperator import AreaOperator
from src.models.gridModel import GridModel
from src.models.modelHelper import sync_model_data


class GridNavigationModel(GridModel):
    def __init__(self, viewModel: Type[GridModel]):
        super().__init__(*viewModel.getDimensions())
        sync_model_data(viewModel, self)

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

