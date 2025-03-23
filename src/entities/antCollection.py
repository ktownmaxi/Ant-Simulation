import os.path
from typing import Type

import pygame

from src.entities.ant import Ant
from src.models.gridNavigationModel import GridNavigationModel
from src.models.gridViewModel import GridViewModel


class AntCollection:
    def __init__(self, number_of_ants, cell_size, view_model: Type[GridViewModel],
                 navigation_model: Type[GridNavigationModel], pos=(0, 0)):
        self.view_model = view_model
        self.navigation_model = navigation_model
        self.cell_size = cell_size
        self.ant_collection = self.create_ant_collection(number_of_ants, pos)

        self.ant_image = self.load_assets()

    def load_assets(self):
        path = os.path.join("src", "assets", "ant.png")
        img = pygame.image.load(path)
        return img

    def create_ant_collection(self, number_of_ants, pos):
        ant_collection = []
        for i in range(number_of_ants):
            ant_collection.append(Ant(self.view_model, self.navigation_model, pos))

        return ant_collection

    def getAntCollection(self):
        return self.ant_collection

    def render(self, screen):
        true_img_size = self.cell_size * self.view_model.zoom_factor * 2
        ant_img = pygame.transform.scale(self.ant_image, (true_img_size, true_img_size))
        for ant in self.ant_collection:
            image_rect = ant_img.get_rect(center=ant.get_absolute_position_of_ant())
            screen.blit(ant_img, image_rect)
