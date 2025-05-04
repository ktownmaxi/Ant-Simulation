import random
import threading
import time
from typing import Type

from src.entities.entity import Entity
from src.models.gridNavigationModel import GridNavigationModel
from src.models.gridViewModel import GridViewModel
from src.helpers import threeToThreeMatrixToRelativeVector


class Ant(Entity):
    def __init__(self, view_model: Type[GridViewModel], navigation_model: Type[GridNavigationModel],
                 visible=False, pos=(0, 0), turn_cycle_active=True):
        super().__init__(view_model, navigation_model, pos)
        self.visible = visible
        self.food_loaded = False
        self.turn_cycle = None
        self.turn_cycle_active = turn_cycle_active

        self.to_home_value = 1
        self.to_food_value = 1

    def move_relative(self, pos_change):
        self.pos = tuple(a + b for a, b in zip(self.pos, pos_change))

    def move_get_absolute_vector_after_relative_move(self, pos_change):
        return tuple(a + b for a, b in zip(self.pos, pos_change))

    def move_to_absolute(self, pos):
        self.pos = pos

    def check_if_ant_on_food_source(self) -> bool:
        return self.navigation_model.get_cell(*self.get_position())['food'] == 1


    def next_turn(self):
        while self.turn_cycle_active:
            visibleArea = self.navigation_model.get_visible_field(self.get_position())
            if self.food_loaded:
                to_colony_points = visibleArea.find_all_filled_toColony(self)
                largest_to_colony_point_index = visibleArea.find_largest_value(to_colony_points)[0]
                movement_vector = threeToThreeMatrixToRelativeVector(largest_to_colony_point_index)
                self.navigation_model.place_to_food_marker(self.get_position(), self.to_food_value)
                self.to_food_value -= 0.001
                self.move_relative(movement_vector)

            else:
                to_food_points = visibleArea.find_all_filled_toFood(self)
                if len(to_food_points) > 0:  # food value found in surroundings
                    largest_value_index, _ = visibleArea.find_largest_value(to_food_points)
                    movement_vector = threeToThreeMatrixToRelativeVector(largest_value_index)
                    self.move_relative(movement_vector)
                else:
                    possible_cells = visibleArea.find_all_unfilled_toColony(self)
                    chosen_cell = list(random.choice(possible_cells).keys())[0]
                    movement_vector = threeToThreeMatrixToRelativeVector(chosen_cell)
                    self.navigation_model.place_to_home_marker(self.get_position(), self.to_home_value)
                    self.to_home_value -= 0.001
                    self.move_relative(movement_vector)

                    if self.check_if_ant_on_food_source():
                        self.food_loaded = True

            time.sleep(0.2)

    def start_turn_cycle(self):
        self.turn_cycle = threading.Thread(target=self.next_turn, daemon=True)
        self.turn_cycle.start()

    def stop_turn_cycle(self):
        self.turn_cycle_active = False

    def get_absolute_position_of_ant(self):
        cell_x, cell_y, cell_w, cell_h = self.view_model.get_absolute_position_data_of_cell(*self.pos)
        center_x = cell_x + cell_w / 2
        center_y = cell_y + cell_h / 2

        return center_x, center_y

    def set_visible(self):
        self.visible = True
        self.start_turn_cycle()

    def set_invisible(self):
        self.visible = False
        self.stop_turn_cycle()

    def get_visibility(self):
        return self.visible
