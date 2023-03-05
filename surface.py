import pygame


class Surface:
    def __init__(self, surface_size, surface_color, surface_alpha):
        """

        :param surface_size: 大きさ(width, height)
        :param surface_color: 色(r, g, b)
        :param surface_alpha: 透明度(0-255)
        """
        self.surface_width = surface_size[0]
        self.surface_height = surface_size[1]
        self.surface_color = surface_color
        self.surface_alpha = surface_alpha
        self.is_active = False
        self.surface = pygame.Surface((self.surface_width, self.surface_height))
        self.surface.set_alpha(self.surface_alpha)  # 透過度を設定
        self.surface.fill(self.surface_color)

    def draw(self, screen):
        if self.is_active:
            screen.blit(self.surface, (0, 0))
        else:
            pass

    def handle_event(self, event):
        pass

    def is_active_true(self):
        self.is_active = True

    def is_active_false(self):
        self.is_active = False
