import os.path

import pygame
import sys

from src.entities.antCollection import AntCollection
from src.models.allPurposeModel import AllPurposeModel
from src.ui.ui import UI

width, height = 1920, 1080

max_fps = 60

# Grid-Settings
rows, cols = 200, 300
cell_size = 15
line_color = (65, 65, 65)
starting_zoom_factor = 0.4
min_zoom, max_zoom = 0.25, 7.5

# Colony settings
colony_radius = 4
colony_color = (255, 0, 0)
food_radius = 3
food_color = (0, 255, 0)
number_of_ants = 500

# Colors
bg_color = (79, 79, 79)

pygame.init()
screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF)
pygame.display.set_caption("Ant-Simulation")

font_path = os.path.join('src', 'assets', 'fonts', 'default.ttf')

# instantiate model instance
model = AllPurposeModel(rows, cols, cell_size, line_color, colony_color, food_color, starting_zoom_factor,
                        min_zoom, max_zoom)

ui = UI(font_path, (width, height))
ant_collection = None

dragging = False
last_mouse_pos = (0, 0)

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 2:
                dragging = True
                last_mouse_pos = event.pos
            elif event.button == 4:  # Scroll up => Zoom in
                model.zoom(event.pos, zoom_in=True)
            elif event.button == 5:  # Scroll down => Zoom out
                model.zoom(event.pos, zoom_in=False)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 2:
                dragging = False

        elif event.type == pygame.MOUSEMOTION and dragging:
            dx = event.pos[0] - last_mouse_pos[0]
            dy = event.pos[1] - last_mouse_pos[1]
            model.pan(dx, dy)
            last_mouse_pos = event.pos

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h and model.colony_pos == ():
                model.mark_colony(pygame.mouse.get_pos(), colony_radius)
                ant_collection = AntCollection(number_of_ants, cell_size, model,
                                               model.colony_pos,
                                               model.get_colony_border(model.colony_pos, colony_radius))
                ant_collection.start_spawning()
                ui.stopwatch.start()

            if event.key == pygame.K_g:
                model.mark_food(pygame.mouse.get_pos(), food_radius)

    screen.fill(bg_color)
    model.draw(screen)
    if ant_collection is not None:
        ant_collection.render(screen)
        ui.draw(screen, int(clock.get_fps()), ant_collection.get_spawned_ants())
    else:

        ui.draw(screen, int(clock.get_fps()), None)
    pygame.display.flip()

    clock.tick(max_fps)
