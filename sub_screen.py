import pygame


class SubScreen:
    def __init__(self, screen, sub_screen_size, sub_screen_color):
        """
        :param screen: スクリーン
        :param sub_screen_size: サブスクリーンの大きさ
        :param sub_screen_color: サブスクリーンの背景色
        """
        self.screen = screen
        self.width = sub_screen_size[0]
        self.height = sub_screen_size[1]
        self.is_active = False
        # サブスクリーンの作成
        self.sub_screen = pygame.Surface((300, 200))
        self.sub_screen.fill(sub_screen_color)
        self.sub_screen_rect = self.sub_screen.get_rect(center=self.screen.get_rect().center)

    def draw(self, screen):
        if self.is_active:
            screen.blit(self.sub_screen, self.sub_screen_rect)
        else:
            pass

    def handle_event(self, event):
        pass

    def is_active_true(self):
        self.is_active = True

    def is_active_false(self):
        self.is_active = False


class OnBorderSubScreen(SubScreen):
    def __init__(self, screen, sub_screen_size, sub_screen_color, border_width, border_color):
        """
        :param screen: スクリーン
        :param sub_screen_size: サブスクリーンの大きさ
        :param sub_screen_color: サブスクリーンの背景色
        :param border_width: サブスクリーンの外枠の太さ
        :param border_color: サブスクリーンの外枠の色
        """
        super().__init__(screen, sub_screen_size, sub_screen_color)
        self.border_width = border_width
        self.border_color = border_color
        # 枠線の追加
        border_width = self.border_width
        border_color = self.border_color
        pygame.draw.rect(self.sub_screen, border_color, self.sub_screen.get_rect(), border_width)
