import setting as sg
import pygame


class BaseLabel:
    def __init__(self, text, font_size, color):
        """
        :param text: 表示する内容
        :param font_size: 文字の大きさ
        :param color: 文字の色
        """
        self.text = text
        self.font = pygame.font.Font(sg.FONT_FILE_PATH, font_size)
        self.color = color
        self.rendered_text = self.font.render(self.text, True, self.color)
        self.is_active = True

    def update_text(self, new_text):
        """
        表示する内容を更新するメソッド
        :param new_text: 新たに格納する内容
        """
        self.text = new_text
        self.rendered_text = self.font.render(self.text, True, self.color)

    def draw(self, screen):
        """ 描画処理を行うメソッド """
        pass

    def handle_event(self, event):
        """ イベント処理を行うメソッド """
        pass

    def is_active_true(self):
        """ is_activeにTrueを格納するメソッド """
        self.is_active = True

    def is_active_false(self):
        """ is_activeにFalseを格納するメソッド """
        self.is_active = False


class Label(BaseLabel):
    def __init__(self, text, font_size, color, position):
        """
        :param text: 表示する内容
        :param font_size: 文字の大きさ
        :param color: 文字の色
        :param position: 文字の描画位置
        """
        super().__init__(text, font_size, color)
        self.position = position

    def draw(self, screen):
        """ 描画処理を行うメソッド """
        if self.is_active:
            screen.blit(self.rendered_text, self.position)
        else:
            pass


class LoopLabel(BaseLabel):
    def __init__(self, text, font_size, color, position, loop_num):
        """
        :param text: 表示する内容
        :param font_size: 文字の大きさ
        :param color: 文字の色
        :param position: 文字の描画位置
        :param loop_num: ループ回数
        """
        super().__init__(text, font_size, color)
        self.x = position[0]
        self.y = position[1]
        self.font_size = font_size
        self.loop_num = loop_num

    def draw(self, screen):
        """ 描画処理を行うメソッド """
        if self.is_active:
            for i in range(self.loop_num):
                screen.blit(self.rendered_text, ((i * self.font_size)+self.x, self.y))
        else:
            pass

    def update_loop_num(self, new_loop_num):
        """
        loop回数を更新するメソッド

        :param new_loop_num: 新たに設定するloop回数
        """
        self.loop_num = new_loop_num


if __name__ == '__main__':
    pass
