import setting as sg
import pygame


class TextBox:
    def __init__(self, pos, box_size, font_size, box_color, text_color):
        """

        :param pos: 描画位置
        :param box_size: テキストボックスの大きさ
        :param font_size: 文字の大きさ
        :param box_color: テキストボックスの色
        :param text_color: 文字色
        """
        self.rect = pygame.Rect(pos, box_size)
        # 日本語フォントを使用する場合、フォントファイルのパスを指定する
        self.font = pygame.font.Font(sg.FONT_FILE_PATH, font_size)
        self.box_color = box_color
        self.text_color = text_color
        self.text = ''
        self.is_active = True

    def handle_event(self, event):
        """ イベント処理を行うメソッド """
        if self.is_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Enterキーを押した場合は何もしない
                    pass
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
        else:
            pass

    def draw(self, screen):
        """ 描画処理を行うメソッド """
        pygame.draw.rect(screen, self.box_color, self.rect, 2)
        text_surface = self.font.render(self.text, True, self.text_color)
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))

    def get_text(self):
        """ textの中身を返すメソッド """
        return self.text

    def clear_text(self):
        """ textの中身をクリアするメソッド """
        self.text = ''

    def is_active_true(self):
        """ is_activeにTrueを格納するメソッド """
        self.is_active = True

    def is_active_false(self):
        """ is_activeにFalseを格納するメソッド """
        self.is_active = False


if __name__ == '__main__':
    pass
