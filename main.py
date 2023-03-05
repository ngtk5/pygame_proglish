import setting as sg
from screen import TitleScreen
import sys
import pygame
from sound import SoundPlayer


class Game:
    """ 指定されている画面を表示するクラス """
    def __init__(self):
        # pygame初期化
        pygame.init()
        # ウィンドウサイズ指定
        self.screen = pygame.display.set_mode((sg.SCREEN_WIDTH, sg.SCREEN_HEIGHT))
        # Clock()オブジェクトを作成
        self.clock = pygame.time.Clock()
        # SoundPlayerクラスのインスタンス化
        self.sound_player = SoundPlayer()
        # TitleScreenクラスのインスタンス化
        self.title_screen = TitleScreen(self.screen, self.change_screen, self.sound_player)
        # 現在表示されている画面
        self.current_screen = self.title_screen

    def change_screen(self, new_screen):
        # 画面を切り替える
        self.current_screen = new_screen

    def run(self):
        while True:
            # フレームレート制御
            self.clock.tick(sg.FPS)
            # イベント処理
            self.handle_events()
            # 描画処理
            self.draw()

    def handle_events(self):
        for event in pygame.event.get():
            # 終了イベント確認
            if event.type == pygame.QUIT:
                self.sound_player.save_json()
                pygame.quit()
                sys.exit()
            # 各イベント確認
            self.current_screen.on_event(event)

    def draw(self):
        # 描画処理
        self.screen.fill(sg.WHITE)
        self.current_screen.on_draw()
        # 画面アップデート処理
        pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
