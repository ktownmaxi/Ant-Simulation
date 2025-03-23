import pygame
import sys

from src.entities.antCollection import AntCollection
from src.models.gridNavigationModel import GridNavigationModel
from src.models.gridViewModel import GridViewModel
from models.modelHelper import sync_model_data

width, height = 1920, 1080

# Grid-Settings
rows, cols = 150, 150
cell_size = 15
line_color = (65, 65, 65)

# Colony settings
colony_radius = 4
colony_color = (255, 0, 0)
food_radius = 3
food_color = (0, 255, 0)
number_of_ants = 50

# Colors
bg_color = (79, 79, 79)

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ant-Simulation")

# instantiate view_model and navigation_model instance
view_model = GridViewModel(rows, cols, cell_size, line_color, colony_color, food_color)
navigation_model = GridNavigationModel(view_model)

dragging = False
last_mouse_pos = (0, 0)

ant_collection = AntCollection(number_of_ants, cell_size, view_model, navigation_model)

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
                view_model.zoom(event.pos, zoom_in=True)
            elif event.button == 5:  # Scroll down => Zoom out
                view_model.zoom(event.pos, zoom_in=False)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 2:
                dragging = False

        elif event.type == pygame.MOUSEMOTION and dragging:
            dx = event.pos[0] - last_mouse_pos[0]
            dy = event.pos[1] - last_mouse_pos[1]
            view_model.pan(dx, dy)
            last_mouse_pos = event.pos

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h:
                view_model.mark_colony(pygame.mouse.get_pos(), colony_radius)
            if event.key == pygame.K_g:
                view_model.mark_food(pygame.mouse.get_pos(), food_radius)

            sync_model_data(view_model, navigation_model)

    screen.fill(bg_color)
    view_model.draw(screen)
    ant_collection.render(screen)
    pygame.display.flip()
