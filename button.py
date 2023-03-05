import setting as sg
import pygame


class BaseButton:
    """  各種ボタンのベースとなるBaseButtonクラス """

    def __init__(self, pos, button_size, text,
                 color, hover_color, font_size, font_color, on_click, sound_player):
        """
        :param pos: ボタンの座標(x, y)
        :param button_size: ボタンの大きさ(width, height)
        :param text: ボタンに表示する内容
        :param color: ボタンの色
        :param hover_color: ボタンにマウスホバーした時の色
        :param font_size: 文字の大きさ
        :param font_color: 文字の色
        :param on_click: コールバック関数
        :param sound_player: sound_playerインスタンス変数
        """
        self.x = pos[0]
        self.y = pos[1]
        self.width = button_size[0]
        self.height = button_size[1]
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.on_click = on_click
        # 日本語フォントを使用する場合、フォントファイルのパスを指定する
        self.font = pygame.font.Font(sg.FONT_FILE_PATH, font_size)
        self.font_color = font_color
        # ボタンがホバー状態かどうか判定するフラグ
        self.is_hovered = False
        self.current_color = self.color
        self.is_event = True
        self.is_draw = True
        # SoundPlayerクラスのインスタンス変数
        self.sound_player = sound_player

    def select_color(self):
        """
        ボタンの色を設定
        """
        if self.is_hovered and self.hover_color is not None:
            self.current_color = self.hover_color
        else:
            self.current_color = self.color

    def draw_button(self, screen):
        self.select_color()
        # ボタンの背景を描画
        pygame.draw.rect(screen, self.current_color, self.rect)

    def draw_text(self, screen):
        """
        ボタン上にテキストを描画するメソッド

        :param screen: ウィンドウサイズ
        :return: None
        """
        text_surface = self.font.render(self.text, True, self.font_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def judge_is_hovered(self, event):
        if event.type == pygame.MOUSEMOTION:
            # マウスがボタンの上に乗ったかどうかを判定
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                if not self.is_hovered:
                    self.is_hovered = True
                    # ホバー音を鳴らす
                    self.sound_player.play_sound('button_hover_sound')
            else:
                self.is_hovered = False

    def judge_on_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # ボタンがクリックされたかどうかを判定
            if self.rect.collidepoint(event.pos):
                # クリック音を鳴らす
                self.sound_player.play_sound('click_sound')
                # 関数実行
                self.on_click()

    def is_event_true(self):
        self.is_event = True

    def is_event_false(self):
        self.is_event = False

    def is_draw_true(self):
        self.is_draw = True

    def is_draw_false(self):
        self.is_draw = False


class Button(BaseButton):
    def __init__(self, pos, button_size, text,
                 color, hover_color, font_color, font_size, on_click, sound_player):
        """
        :param pos: ボタンの座標(x,y)
        :param button_size: ボタンの大きさ(width, height)
        :param text: テキスト
        :param color: 基本色
        :param hover_color: ホバー時の色
        :param font_color: 文字色
        :param font_size: 文字サイズ
        :param on_click: コールバック関数
        :param sound_player: sound_playerインスタンス変数
        """
        super().__init__(pos, button_size, text,
                         color, hover_color,
                         font_size, font_color, on_click, sound_player)

    def draw(self, screen):
        """ 描画処理メソッド """
        if self.is_draw:
            self.draw_button(screen)
            self.draw_text(screen)
        else:
            pass

    def handle_event(self, event):
        """ イベント処理メソッド """
        if self.is_event:
            self.judge_is_hovered(event)
            self.judge_on_click(event)
        else:
            pass


class ArrowButton(BaseButton):
    def __init__(self, pos, button_size, text,
                 color, hover_color, font_color, font_size, on_click, sound_player):
        """
        :param pos: ボタンの座標(x,y)
        :param button_size: ボタンの大きさ(width, height)
        :param text: テキスト
        :param color: 基本色
        :param hover_color: ホバー時の色
        :param font_color: 文字色
        :param font_size: 文字サイズ
        :param on_click: コールバック関数
        :param sound_player: sound_playerインスタンス変数
        """
        super().__init__(pos, button_size, text,
                         color, hover_color,
                         font_size, font_color, on_click, sound_player)

    def draw(self, screen):
        """ 描画処理メソッド """
        if self.is_draw:
            self.create_left_arrow(screen)
            self.draw_text(screen)
        else:
            pass

    def handle_event(self, event):
        """ イベント処理メソッド """
        if self.is_draw:
            self.judge_is_hovered(event)
            self.judge_on_click(event)
        else:
            pass

    def create_left_arrow(self, screen):
        """
        左向き矢印を作成するメソッド
        :param screen: ウィンドウサイズ
        """
        self.draw_button(screen)
        # 大きさ
        arrow_size = self.y + 10
        # x座標
        arrow_x = self.x - 30
        # y座標
        arrow_y = self.y + (self.height - arrow_size) // 2
        # 頂点座標
        arrow_points = [(arrow_x, arrow_y + arrow_size // 2), (arrow_x + arrow_size, arrow_y),
                        (arrow_x + arrow_size, arrow_y + arrow_size)]
        # 左向き矢印を描画
        pygame.draw.polygon(screen, self.current_color, arrow_points)


if __name__ == '__main__':
    pass
