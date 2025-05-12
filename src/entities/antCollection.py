import os.path
import random
import time
from typing import Type
import threading

import pygame

from src.entities.ant import Ant
from src.models.allPurposeModel import AllPurposeModel


class AntCollection:
    def __init__(self, number_of_ants, cell_size, model: Type[AllPurposeModel], pos=(0, 0), spawnable_positions=None):
        if spawnable_positions is None:
            self.spawnable_positions = []
        else:
            self.spawnable_positions = spawnable_positions
        self.model = model
        self.ant_collection = self.create_ant_collection(number_of_ants, pos)

        self.cell_size = cell_size

        self.ant_image, self.red_ant_image = self.load_assets()

    def load_assets(self):
        ant_path = os.path.join("src", "assets", "green_ant.png")
        red_ant_path = os.path.join("src", "assets", "red_ant.png")

        ant_img = pygame.image.load(ant_path).convert_alpha()
        red_ant_path = pygame.image.load(red_ant_path).convert_alpha()

        return ant_img, red_ant_path

    def create_ant_collection(self, number_of_ants, pos):
        ant_collection = []
        for i in range(number_of_ants):
            ant_collection.append(Ant(model=self.model, pos=pos, visible=False))

        return ant_collection

    def getAntCollection(self):
        return self.ant_collection

    def render(self, screen):
        true_img_size = self.cell_size * self.model.zoom_factor * 2
        ant_img = pygame.transform.scale(self.ant_image, (true_img_size, true_img_size))
        red_ant_img = pygame.transform.scale(self.red_ant_image, (true_img_size, true_img_size))
        for ant in self.ant_collection:
            if ant.get_visibility():
                if not ant.food_loaded:
                    image_rect = red_ant_img.get_rect(center=ant.get_absolute_position_of_ant())
                    screen.blit(red_ant_img, image_rect)
                else:
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

            time.sleep(0.05)

    def start_spawning(self):
        thread = threading.Thread(target=self.spawnAnts, daemon=True)
        thread.start()
