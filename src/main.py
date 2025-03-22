import pygame
import sys

from grid import Grid

width, height = 1920, 1080

# Grid-Settings
rows, cols = 150, 150
cell_size = 15
line_color = (65, 65, 65)

# Colors
bg_color = (79, 79, 79)

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ant-Simulation")

# instantiate grid instance
grid = Grid(rows, cols, cell_size, line_color)

dragging = False
last_mouse_pos = (0, 0)

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
                grid.zoom(event.pos, zoom_in=True)
            elif event.button == 5:  # Scroll down => Zoom out
                grid.zoom(event.pos, zoom_in=False)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 2:
                dragging = False

        elif event.type == pygame.MOUSEMOTION and dragging:
            dx = event.pos[0] - last_mouse_pos[0]
            dy = event.pos[1] - last_mouse_pos[1]
            grid.pan(dx, dy)
            last_mouse_pos = event.pos

    screen.fill(bg_color)
    grid.draw(screen)
    pygame.display.flip()
