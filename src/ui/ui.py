import pygame


class UI:
    def __init__(self, font_path: str, screen_dimensions: tuple[int, int]):
        self.font_path = font_path
        self.screen_dimensions = screen_dimensions

    def draw(self, surface: pygame.Surface, fps: int):
        SIDEBAR_COLOR = (50, 50, 50, 90)
        WHITE = (255, 255, 255)

        SIDEBAR_WIDTH = 200
        SIDEBAR_PADDING = 10
        sidebar_surface = pygame.Surface((SIDEBAR_WIDTH, self.screen_dimensions[1]), pygame.SRCALPHA)

        sidebar_surface.fill(SIDEBAR_COLOR)

        label_text = pygame.font.Font(self.font_path, 45).render("Sidemenu", True, WHITE)
        fps_text = pygame.font.Font(self.font_path, 30).render(f"FPS {fps}", True, WHITE)
        sidebar_surface.blit(label_text, (SIDEBAR_PADDING, SIDEBAR_PADDING))

        y_fps = SIDEBAR_PADDING + label_text.get_height() + 5

        sidebar_surface.blit(fps_text, (SIDEBAR_PADDING, y_fps))

        surface.blit(sidebar_surface, (self.screen_dimensions[0] - SIDEBAR_WIDTH, 0))
