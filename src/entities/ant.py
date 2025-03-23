from typing import Type

from src.entities.entity import Entity
from src.models.gridNavigationModel import GridNavigationModel
from src.models.gridViewModel import GridViewModel


class Ant(Entity):
    def __init__(self, view_model: Type[GridViewModel], navigation_model: Type[GridNavigationModel], pos=(0, 0)):
        super().__init__(view_model, navigation_model, pos)

    def move(self):
        pass

    def get_absolute_position_of_ant(self):
        cell_x, cell_y, cell_w, cell_h = self.view_model.get_absolute_position_data_of_cell(*self.pos)
        center_x = cell_x + cell_w / 2
        center_y = cell_y + cell_h / 2

        return center_x, center_y
