from abc import ABC, abstractmethod
from typing import Type

from src.models.gridNavigationModel import GridNavigationModel
from src.models.gridViewModel import GridViewModel


class Entity(ABC):
    def __init__(self, view_model: Type[GridViewModel], navigation_model: Type[GridNavigationModel], pos=(0, 0)):
        self.pos = pos  # position in Grid
        self.view_model = view_model
        self.navigation_model = navigation_model

    @abstractmethod
    def move_relative(self, pos_change: tuple[int, int]):
        """move method has to be implemented"""
        pass

    @abstractmethod
    def move_to_absolute(self, pos: tuple[int, int]):
        """move method has to be implemented"""
        pass

    def get_position(self) -> tuple[int, int]:
        """returns current position"""
        return self.pos

    def set_position(self, position: tuple[int, int]):
        self.pos = position
