from abc import ABC, abstractmethod
from typing import Type

from src.models.gridNavigationModel import GridNavigationModel
from src.models.gridViewModel import GridViewModel


class Entity(ABC):
    def __init__(self, view_model: Type[GridViewModel], navigation_model: Type[GridNavigationModel], pos=(0, 0)):
        self.pos = pos  # position in Grid
        self.view_model = view_model
        self.data_model = navigation_model

    @abstractmethod
    def move(self):
        """move method has to be implemented"""
        pass

    def get_position(self):
        """returns current position"""
        return self.pos

    def set_position(self, position: tuple[int, int]):
        self.pos = position
