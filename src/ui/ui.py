import pygame
from src.ui.stopwatch import Stopwatch


class UI:
    def __init__(self, font_path: str, screen_dimensions: tuple[int, int]):
        self.font_path = font_path
        self.screen_dimensions = screen_dimensions

        self.stopwatch = Stopwatch()

    def draw(self, surface: pygame.Surface, fps: int, spawned_ants: int) -> None:
        SIDEBAR_COLOR = (50, 50, 50, 90)
        WHITE = (255, 255, 255)

        SIDEBAR_WIDTH = 200
        SIDEBAR_PADDING = 10
        sidebar_surface = pygame.Surface((SIDEBAR_WIDTH, self.screen_dimensions[1]), pygame.SRCALPHA)

        sidebar_surface.fill(SIDEBAR_COLOR)

        label_text = pygame.font.Font(self.font_path, 45).render("Sidemenu", True, WHITE)
        fps_text = pygame.font.Font(self.font_path, 30).render(f"FPS {fps}", True, WHITE)
        stopwatch_text = pygame.font.Font(self.font_path, 30).render(
            self.stopwatch.format_time(self.stopwatch.get_time()), True, WHITE
        )
        spawned_ants_text = pygame.font.Font(self.font_path, 25).render(
            f"Spawned ants: {spawned_ants}", True, WHITE
        )

        y_stopwatch = SIDEBAR_PADDING + label_text.get_height() + 10
        y_fps = SIDEBAR_PADDING + fps_text.get_height() + label_text.get_height() + 5
        y_spawned_ants = SIDEBAR_PADDING + fps_text.get_height() + label_text.get_height() + stopwatch_text.get_height() + 5

        sidebar_surface.blit(label_text, (SIDEBAR_PADDING, SIDEBAR_PADDING))
        sidebar_surface.blit(fps_text, (SIDEBAR_PADDING, y_fps))
        sidebar_surface.blit(stopwatch_text, (SIDEBAR_PADDING, y_stopwatch))
        sidebar_surface.blit(spawned_ants_text, (SIDEBAR_PADDING, y_spawned_ants))

        surface.blit(sidebar_surface, (self.screen_dimensions[0] - SIDEBAR_WIDTH, 0))
