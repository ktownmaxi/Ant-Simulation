import os.path
import random
import time
from typing import Type
import threading

import pygame

from src.entities.ant import Ant
from src.models.allPurposeModel import AllPurposeModel


class AntCollection:
    def __init__(self, number_of_ants, cell_size, view_model: Type[AllPurposeModel], pos=(0, 0), spawnable_positions=None):
        if spawnable_positions is None:
            self.spawnable_positions = []
        else:
            self.spawnable_positions = spawnable_positions
        self.view_model = view_model
        self.ant_collection = self.create_ant_collection(number_of_ants, pos)

        self.cell_size = cell_size

        self.ant_image = self.load_assets()

    def load_assets(self):
        path = os.path.join("src", "assets", "ant.png")
        img = pygame.image.load(path).convert_alpha()
        return img

    def create_ant_collection(self, number_of_ants, pos):
        ant_collection = []
        for i in range(number_of_ants):
            ant_collection.append(Ant(self.view_model, pos))

        return ant_collection

    def getAntCollection(self):
        return self.ant_collection

    def render(self, screen):
        true_img_size = self.cell_size * self.view_model.zoom_factor * 2
        ant_img = pygame.transform.scale(self.ant_image, (true_img_size, true_img_size))
        for ant in self.ant_collection:
            image_rect = ant_img.get_rect(center=ant.get_absolute_position_of_ant())
            screen.blit(ant_img, image_rect)

    def spawnAnts(self):
        spawnable_positions_copy = list(self.spawnable_positions)
        for ant in self.ant_collection:
            if len(spawnable_positions_copy) <= 0:
                spawnable_positions_copy = list(self.spawnable_positions)

            random_spawnable_position = random.choice(spawnable_positions_copy)
            spawnable_positions_copy.remove(random_spawnable_position)
            ant.set_position(random_spawnable_position)
            ant.set_visible()

            time.sleep(0.1)

    def start_spawning(self):
        thread = threading.Thread(target=self.spawnAnts, daemon=True)
        thread.start()
