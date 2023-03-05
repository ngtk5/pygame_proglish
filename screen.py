import setting as sg
from button import Button, ArrowButton
from textbox import TextBox
from label import Label, LoopLabel
import pygame
from game_system import StandardMode, EndlessMode, PracticeMode
from sub_screen import OnBorderSubScreen
from surface import Surface
from read_file import read_txt_file


def read_variable_file(file_name):
    with open(file_name, "r") as f:
        data = f.readlines()
    variables = {}
    for line in data:
        line = line.strip()  # 改行文字を削除
        if "=" in line:
            name, value = line.split("=")
            name = name.strip()  # スペースを削除
            value = value.strip()  # スペースを削除
            try:
                # 数値に変換できる場合は数値に変換する
                value = int(value)
            except ValueError:
                try:
                    value = float(value)
                except ValueError:
                    pass  # 数値に変換できない場合はそのままの値を使う
            variables[name] = value
    return variables


def array_disassembly(array):
    return f'{array[0]} {array[1]} {array[2]}'


class BaseScreen:
    """ 画面作成のベースとなるクラス """

    def __init__(self, screen, change_screen_callback, sound_player):
        # ウィンドウ
        self.screen = screen
        # コールバック関数
        self.change_screen_callback = change_screen_callback
        # イベント処理をまとめて行うために格納しておくリスト
        self.EVENT_PARTS = []
        # 難易度(デフォルトはnormal)
        self.difficulty = 'NORMAL'
        # ゲームモード(デフォルトはstandard)
        self.game_mode = 'STANDARD'
        # 現在の問題(何番目か)
        self.current_question = 0
        # SoundPlayerクラスのインスタンス変数
        self.sound_player = sound_player

    def on_event(self, event):
        """ イベント処理を行うメソッド """
        for parts in self.EVENT_PARTS:
            parts.handle_event(event)

    def on_draw(self):
        """ 描画処理を行うメソッド """
        for parts in self.EVENT_PARTS:
            parts.draw(self.screen)

    def go_title_screen(self):
        """ タイトル画面へ遷移するメソッド """
        self.change_screen_callback(TitleScreen(self.screen, self.change_screen_callback, self.sound_player))

    def go_game_setting_screen(self):
        """ ゲーム設定画面へ遷移するメソッド """
        self.change_screen_callback(GameSettingScreen(self.screen, self.change_screen_callback, self.sound_player))

    def go_game_play_screen(self):
        """ GamePlayScreenに切り替えるメソッド """
        self.change_screen_callback(GamePlayScreen(self.screen, self.change_screen_callback,
                                                   self.sound_player, self.difficulty, self.game_mode))

    def go_vocabulary_screen(self):
        """ 単語帳画面へ遷移するメソッド """
        self.change_screen_callback(VocabularyScreen(self.screen, self.change_screen_callback, self.sound_player))

    def go_show_vocabulary_screen(self):
        self.change_screen_callback(ShowVocabularyScreen(self.screen, self.change_screen_callback,
                                                         self.sound_player, self.difficulty))

    def go_system_setting_screen(self):
        """ システム設定画面へ遷移するメソッド """
        self.change_screen_callback(SystemSettingsScreen(self.screen, self.change_screen_callback, self.sound_player))

    def go_game_score_screen(self, game_score, game_mistake, result_text):
        """ スコア画面へ遷移するメソッド """
        self.change_screen_callback(GameScoreScreen(self.screen, self.change_screen_callback,
                                                    self.sound_player,
                                                    game_score, game_mistake, result_text))

    def set_diff_easy(self):
        """ self.difficultyに'EASY'を格納するメソッド """
        self.difficulty = 'EASY'

    def set_diff_normal(self):
        """ self.difficultyに'NORMAL'を格納するメソッド """
        self.difficulty = 'NORMAL'

    def set_diff_hard(self):
        """ self.difficultyに'HARD'を格納するメソッド """
        self.difficulty = 'HARD'

    def set_game_mode_standard(self):
        """ self.game_modeに’STANDARD’を格納するメソッド """
        self.game_mode = 'STANDARD'

    def set_game_mode_practice(self):
        """ self.game_modeに’PRACTICE’を格納するメソッド """
        self.game_mode = 'PRACTICE'

    def set_game_mode_endless(self):
        """ self.game_modeに’ENDLESS’を格納するメソッド """
        self.game_mode = 'ENDLESS'

    def get_current_question(self):
        """ self.current_questionを返すメソッド """
        return self.current_question

    def add_current_question(self):
        """ self.current_questionを+1するメソッド """
        self.current_question += 1


class TitleScreen(BaseScreen):
    """ タイトル画面を作成するクラス """

    def __init__(self, screen, change_screen_callback, sound_player):
        super().__init__(screen, change_screen_callback, sound_player)
        # 各settingsをtxtファイルから読み込み,辞書型のdata変数に格納
        self.data = read_variable_file('settings/TitleScreen.txt')
        # タイトル
        self.label_title = Label(
            'PROGLISH',
            self.data['label_title_font_size'],
            sg.BLACK,
            (self.data['label_title_x'],
             self.data['label_title_y'])
        )
        # ボタンの作成
        self.button_play = Button(
            (self.data['button_play_x'],
             self.data['button_play_y']),
            (self.data['button_play_width'],
             self.data['button_play_height']),
            'PLAY',
            sg.BUTTON_COLOR,
            sg.BUTTON_HOVER_COLOR,
            sg.WHITE,
            self.data['button_play_font_size'],
            self.go_game_setting_screen,
            self.sound_player
        )
        self.button_vocabulary = Button(
            (self.data['button_vocabulary_x'],
             self.data['button_vocabulary_y']),
            (self.data['button_vocabulary_width'],
             self.data['button_vocabulary_height']),
            '単語帳',
            sg.BUTTON_COLOR,
            sg.BUTTON_HOVER_COLOR,
            sg.WHITE,
            self.data['button_vocabulary_font_size'],
            self.go_vocabulary_screen,
            self.sound_player
        )
        self.button_system_settings = Button(
            (self.data['button_system_settings_x'],
             self.data['button_system_settings_y']),
            (self.data['button_system_settings_width'],
             self.data['button_system_settings_height']),
            '設定',
            sg.BUTTON_COLOR,
            sg.BUTTON_HOVER_COLOR,
            sg.WHITE,
            self.data['button_system_settings_font_size'],
            self.go_system_setting_screen,
            self.sound_player
        )
        self.EVENT_PARTS = [self.label_title,
                            self.button_play,
                            self.button_vocabulary,
                            self.button_system_settings,
                            ]


class GameSettingScreen(BaseScreen):
    """ ゲーム開始前の設定画面を作成するクラス """

    def __init__(self, screen, change_screen_callback, sound_player):
        super().__init__(screen, change_screen_callback, sound_player)
        # 各settingsをtxtファイルから読み込み,辞書型のdata変数に格納
        self.data = read_variable_file('settings/GameSettingScreen.txt')
        # 現在選択されている難易度を表示するラベルの作成
        self.label_current_difficulty = Label(
            f'選択されている難易度：{self.difficulty}',
            self.data['label_current_difficulty_font_size'],
            sg.BLACK,
            (self.data['label_current_difficulty_x'],
             self.data['label_current_difficulty_y'])
        )
        # 現在選択されているゲームモードを表示するラベルの作成
        self.label_current_game_mode = Label(
            f'選択されているゲームモード：{self.game_mode}',
            self.data['label_current_game_mode_font_size'],
            sg.BLACK,
            (self.data['label_current_game_mode_x'],
             self.data['label_current_game_mode_y'])
        )
        # 難易度ラベルの作成
        self.label_difficulty = Label(
            '難易度',
            self.data['label_difficulty_font_size'],
            sg.BLACK,
            (self.data['label_difficulty_x'],
             self.data['label_difficulty_y'])
        )
        # EASYボタンの作成
        self.button_easy = Button(
            (self.data['button_easy_x'],
             self.data['button_easy_y']),
            (self.data['button_diff_width'],
             self.data['button_diff_height']),
            'EASY',
            sg.BUTTON_COLOR,
            sg.BUTTON_HOVER_COLOR,
            sg.WHITE,
            self.data['button_diff_font_size'],
            self.change_diff_easy,
            self.sound_player
        )
        # NORMALボタンの作成
        self.button_normal = Button(
            (self.data['button_normal_x'],
             self.data['button_normal_y']),
            (self.data['button_diff_width'],
             self.data['button_diff_height']),
            'NORMAL',
            sg.BUTTON_COLOR,
            sg.BUTTON_HOVER_COLOR,
            sg.WHITE,
            self.data['button_diff_font_size'],
            self.change_diff_normal,
            self.sound_player
        )
        # HARDボタンの作成
        self.button_hard = Button(
            (self.data['button_hard_x'],
             self.data['button_hard_y']),
            (self.data['button_diff_width'],
             self.data['button_diff_height']),
            'HARD',
            sg.BUTTON_COLOR,
            sg.BUTTON_HOVER_COLOR,
            sg.WHITE,
            self.data['button_diff_font_size'],
            self.change_diff_hard,
            self.sound_player
        )
        # ゲームモードラベルの作成
        self.label_game_mode = Label(
            'ゲームモード',
            self.data['label_game_mode_font_size'],
            sg.BLACK,
            (self.data['label_game_mode_x'],
             self.data['label_game_mode_y'])
        )
        # PRACTICEボタンの作成
        self.button_practice = Button(
            (self.data['button_practice_x'],
             self.data['button_practice_y']),
            (self.data['button_game_mode_width'],
             self.data['button_game_mode_height']),
            'PRACTICE',
            sg.BUTTON_COLOR,
            sg.BUTTON_HOVER_COLOR,
            sg.WHITE,
            self.data['button_game_mode_font_size'],
            self.change_game_mode_practice,
            self.sound_player
        )
        # STANDARDボタンの作成
        self.button_standard = Button(
            (self.data['button_standard_x'],
             self.data['button_standard_y']),
            (self.data['button_game_mode_width'],
             self.data['button_game_mode_height']),
            'STANDARD',
            sg.BUTTON_COLOR,
            sg.BUTTON_HOVER_COLOR,
            sg.WHITE,
            self.data['button_game_mode_font_size'],
            self.change_game_mode_standard,
            self.sound_player
        )
        # ENDLESSボタンの作成
        self.button_endless = Button(
            (self.data['button_endless_x'],
             self.data['button_endless_y']),
            (self.data['button_game_mode_width'],
             self.data['button_game_mode_height']),
            'ENDLESS',
            sg.BUTTON_COLOR,
            sg.BUTTON_HOVER_COLOR,
            sg.WHITE,
            self.data['button_game_mode_font_size'],
            self.change_game_mode_endless,
            self.sound_player
        )
        # GAME PLAYボタンの作成
        self.button_game_play = Button(
            (self.data['button_game_play_x'],
             self.data['button_game_play_y']),
            (self.data['button_game_play_width'],
             self.data['button_game_play_height']),
            'GAME PLAY',
            sg.BUTTON_COLOR,
            sg.BUTTON_HOVER_COLOR,
            sg.WHITE,
            self.data['button_game_play_font_size'],
            self.go_game_play_screen,
            self.sound_player
        )
        # 戻るボタンの作成
        self.button_back_title_screen = ArrowButton(
            sg.BUTTON_BACK_POS,
            sg.BUTTON_BACK_SIZE,
            sg.BUTTON_BACK_TEXT,
            sg.BUTTON_COLOR,
            sg.BUTTON_HOVER_COLOR,
            sg.WHITE,
            sg.BUTTON_BACK_FONT_SIZE,
            self.go_title_screen,
            self.sound_player
        )

        self.EVENT_PARTS = [self.label_current_difficulty,
                            self.label_current_game_mode,
                            self.label_difficulty,
                            self.button_easy,
                            self.button_normal,
                            self.button_hard,
                            self.label_game_mode,
                            self.button_standard,
                            self.button_practice,
                            self.button_endless,
                            self.button_game_play,
                            self.button_back_title_screen,
                            ]

    def change_diff_easy(self):
        """ 難易度に変更するメソッド """
        self.set_diff_easy()
        self.label_current_difficulty.update_text(f'選択されている難易度：{self.difficulty}')

    def change_diff_normal(self):
        """ 難易度に変更するメソッド """
        self.set_diff_normal()
        self.label_current_difficulty.update_text(f'選択されている難易度：{self.difficulty}')

    def change_diff_hard(self):
        """ 難易度に変更するメソッド """
        self.set_diff_hard()
        self.label_current_difficulty.update_text(f'選択されている難易度：{self.difficulty}')

    def change_game_mode_standard(self):
        """ ゲームモードをスタンダードモードに変更するメソッド """
        self.set_game_mode_standard()
        self.label_current_game_mode.update_text(f'選択されているゲームモード：{self.game_mode}')

    def change_game_mode_practice(self):
        """ ゲームモードをプラクティスモード変更するメソッド """
        self.set_game_mode_practice()
        self.label_current_game_mode.update_text(f'選択されているゲームモード：{self.game_mode}')

    def change_game_mode_endless(self):
        """ ゲームモードをエンドレスモードに変更するメソッド """
        self.set_game_mode_endless()
        self.label_current_game_mode.update_text(f'選択されているゲームモード：{self.game_mode}')


class VocabularyScreen(BaseScreen):
    """ 単語帳の画面を作成するクラス """

    def __init__(self, screen, change_screen_callback, sound_player):
        super().__init__(screen, change_screen_callback, sound_player)
        # 各settingsをtxtファイルから読み込み,辞書型のdata変数に格納
        self.data = read_variable_file('settings/VocabularyScreen.txt')
        # 戻るボタン
        self.button_back_title_screen = ArrowButton(
            sg.BUTTON_BACK_POS,
            sg.BUTTON_BACK_SIZE,
            sg.BUTTON_BACK_TEXT,
            sg.BUTTON_COLOR,
            sg.BUTTON_HOVER_COLOR,
            sg.WHITE,
            sg.BUTTON_BACK_FONT_SIZE,
            self.go_title_screen,
            self.sound_player
        )
        # 説明ラベル
        self.label_description = Label(
            '各難易度に登場する単語を確認することができます。',
            self.data['label_description_font_size'],
            sg.BLACK,
            (self.data['label_description_x'],
             self.data['label_description_y'])
        )
        # EASYボタンの作成
        self.button_easy = Button(
            (self.data['button_easy_x'],
             self.data['button_easy_y']),
            (self.data['button_diff_width'],
             self.data['button_diff_height']),
            'EASY',
            sg.BUTTON_COLOR,
            sg.BUTTON_HOVER_COLOR,
            sg.WHITE,
            self.data['button_diff_font_size'],
            self.set_diff_easy,
            self.sound_player
        )
        # NORMALボタンの作成
        self.button_normal = Button(
            (self.data['button_normal_x'],
             self.data['button_normal_y']),
            (self.data['button_diff_width'],
             self.data['button_diff_height']),
            'NORMAL',
            sg.BUTTON_COLOR,
            sg.BUTTON_HOVER_COLOR,
            sg.WHITE,
            self.data['button_diff_font_size'],
            self.set_diff_normal,
            self.sound_player
        )
        # HARDボタンの作成
        self.button_hard = Button(
            (self.data['button_hard_x'],
             self.data['button_hard_y']),
            (self.data['button_diff_width'],
             self.data['button_diff_height']),
            'HARD',
            sg.BUTTON_COLOR,
            sg.BUTTON_HOVER_COLOR,
            sg.WHITE,
            self.data['button_diff_font_size'],
            self.set_diff_hard,
            self.sound_player
        )
        self.EVENT_PARTS = [self.button_back_title_screen,
                            self.label_description,
                            self.button_easy,
                            self.button_normal,
                            self.button_hard,
                            ]

    def set_diff_easy(self):
        super().set_diff_easy()
        self.go_show_vocabulary_screen()

    def set_diff_normal(self):
        super().set_diff_normal()
        self.go_show_vocabulary_screen()

    def set_diff_hard(self):
        super().set_diff_hard()
        self.go_show_vocabulary_screen()


class ShowVocabularyScreen(BaseScreen):
    def __init__(self, screen, change_screen_callback, sound_player, diff):
        super().__init__(screen, change_screen_callback, sound_player)
        self.vocabulary = read_txt_file(f'vocabulary/{diff}.txt')
        self.data = read_variable_file('settings/ShowVocabularyScreen.txt')
        # 大文字に変換して保持
        self.diff = diff.upper()
        # 現在のページ(初期値は1)
        self.current_page = 1
        # 戻るボタンの作成
        self.button_back_vocabulary_screen = ArrowButton(
            sg.BUTTON_BACK_POS,
            sg.BUTTON_BACK_SIZE,
            sg.BUTTON_BACK_TEXT,
            sg.BUTTON_COLOR,
            sg.BUTTON_HOVER_COLOR,
            sg.WHITE,
            sg.BUTTON_BACK_FONT_SIZE,
            self.go_vocabulary_screen,
            self.sound_player
        )
        # 難易度ラベル
        self.label_diff = Label(
            self.diff,
            self.data['label_diff_font_size'],
            sg.BLACK,
            (self.data['label_diff_x'],
             self.data['label_diff_y'])
        )
        self.label_words_1 = Label(
            '更新されていません',
            self.data['label_words_font_size'],
            sg.BLACK,
            (self.data['label_words_1_x'],
             self.data['label_words_1_y'])
        )
        self.label_words_2 = Label(
            '更新されていません',
            self.data['label_words_font_size'],
            sg.BLACK,
            (self.data['label_words_2_x'],
             self.data['label_words_2_y'])
        )
        self.label_words_3 = Label(
            '更新されていません',
            self.data['label_words_font_size'],
            sg.BLACK,
            (self.data['label_words_3_x'],
             self.data['label_words_3_y'])
        )
        self.label_words_4 = Label(
            '更新されていません',
            self.data['label_words_font_size'],
            sg.BLACK,
            (self.data['label_words_4_x'],
             self.data['label_words_4_y'])
        )
        self.label_words_5 = Label(
            '更新されていません',
            self.data['label_words_font_size'],
            sg.BLACK,
            (self.data['label_words_5_x'],
             self.data['label_words_5_y'])
        )
        self.label_words_6 = Label(
            '更新されていません',
            self.data['label_words_font_size'],
            sg.BLACK,
            (self.data['label_words_6_x'],
             self.data['label_words_6_y'])
        )
        self.label_words_7 = Label(
            '更新されていません',
            self.data['label_words_font_size'],
            sg.BLACK,
            (self.data['label_words_7_x'],
             self.data['label_words_7_y'])
        )
        self.label_words_8 = Label(
            '更新されていません',
            self.data['label_words_font_size'],
            sg.BLACK,
            (self.data['label_words_8_x'],
             self.data['label_words_8_y'])
        )
        self.label_words_9 = Label(
            '更新されていません',
            self.data['label_words_font_size'],
            sg.BLACK,
            (self.data['label_words_9_x'],
             self.data['label_words_9_y'])
        )
        self.label_words_10 = Label(
            '更新されていません',
            self.data['label_words_font_size'],
            sg.BLACK,
            (self.data['label_words_10_x'],
             self.data['label_words_10_y'])
        )
        # 前のページボタン
        self.button_back_page = Button(
            (self.data['button_back_page_x'],
             self.data['button_back_page_y']),
            (self.data['button_back_page_width'],
             self.data['button_back_page_height']),
            '前のページ',
            sg.BUTTON_COLOR,
            sg.BUTTON_HOVER_COLOR,
            sg.BLACK,
            self.data['button_back_page_font_size'],
            self.sub_current_page,
            self.sound_player
        )
        # 次のページボタン
        self.button_next_page = Button(
            (self.data['button_next_page_x'],
             self.data['button_next_page_y']),
            (self.data['button_next_page_width'],
             self.data['button_next_page_height']),
            '次のページ',
            sg.BUTTON_COLOR,
            sg.BUTTON_HOVER_COLOR,
            sg.BLACK,
            self.data['button_next_page_font_size'],
            self.add_current_page,
            self.sound_player
        )
        self.label_page = Label(
            '更新されてません',
            self.data['label_page_font_size'],
            sg.BLACK,
            (self.data['label_page_x'],
             self.data['label_page_y'])
        )
        self.EVENT_PARTS = [self.button_back_vocabulary_screen,
                            self.label_diff,
                            self.label_words_1,
                            self.label_words_2,
                            self.label_words_3,
                            self.label_words_4,
                            self.label_words_5,
                            self.label_words_6,
                            self.label_words_7,
                            self.label_words_8,
                            self.label_words_9,
                            self.label_words_10,
                            self.button_back_page,
                            self.button_next_page,
                            self.label_page
                            ]
        self.labels_words = [self.label_words_1,
                             self.label_words_2,
                             self.label_words_3,
                             self.label_words_4,
                             self.label_words_5,
                             self.label_words_6,
                             self.label_words_7,
                             self.label_words_8,
                             self.label_words_9,
                             self.label_words_10,
                             ]

    def on_event(self, event):
        super().on_event(event)
        # 1ページ目なら「前のページ」ボタンのイベント処理をしない
        if self.get_current_page() == 1:
            self.button_back_page.is_event_false()
        # 最後のページなら「次のページ」ボタンのイベント処理をしない
        elif self.get_current_page() == len(self.vocabulary) // 10:
            self.button_next_page.is_event_false()
        # それ以外のページならイベント処理をする
        else:
            self.button_next_page.is_event_true()
            self.button_back_page.is_event_true()

    def on_draw(self):
        super().on_draw()
        self.update_label_words()
        self.update_label_page()

    def update_label_words(self):
        """ labels_words内のlabel変数のテキストを更新するメソッド """
        for i, label in enumerate(self.labels_words):
            label.update_text(array_disassembly(self.vocabulary[(self.get_current_page()-1) * 10 + i]))

    def update_label_page(self):
        """ label_pageのテキストを更新するメソッド """
        self.label_page.update_text(
            f'{self.get_current_page()}/{(len(self.vocabulary)//10)}ページ')

    def get_current_page(self):
        """ current_pageを返すメソッド """
        return self.current_page

    def add_current_page(self):
        """ current_pageを+1するメソッド """
        if len(self.vocabulary) == self.get_current_page()*10:
            pass
        else:
            self.current_page += 1

    def sub_current_page(self):
        """ current_pageを-1するメソッド """
        if self.get_current_page() == 1:
            pass
        else:
            self.current_page -= 1


class GamePlayScreen(BaseScreen):
    """ ゲーム中の画面を作成するクラス """

    def __init__(self, screen, change_screen_callback, sound_player, difficulty, game_mode):
        super().__init__(screen, change_screen_callback, sound_player)
        # 各settingsをtxtファイルから読み込み,辞書型のdata変数に格納
        self.data = read_variable_file('settings/GamePlayScreen.txt')
        # 難易度セット
        self.judge_diff(difficulty)
        # ゲームモードセット
        self.judge_game_mode(game_mode)
        # メニューボタンのフラグ
        self.button_menu_flg = False
        # インスタンス変数を生成
        self.game_system = self.create_game_mode_inst()
        # 使用する問題リストを格納
        self.random_question_list = self.game_system.get_random_list()
        # 残りライフを表示するラべルの作成
        self.label_current_life = LoopLabel(
            chr(0x2665),
            self.data['label_current_life_font_size'],
            sg.RED,
            (self.data['label_current_life_x'],
             self.data['label_current_life_y']),
            self.game_system.get_life()
        )
        # 回答欄の作成
        self.text_box_answer = TextBox(
            (self.data['text_box_answer_x'],
             self.data['text_box_answer_y']),
            (self.data['text_box_answer_width'],
             self.data['text_box_answer_height']),
            self.data['text_box_answer_font_size'],
            sg.BLACK,
            sg.BLACK
        )
        # 問題文(品詞)の作成
        self.label_parts = Label(
            self.random_question_list[self.get_current_question()][sg.PART_NUM],
            self.data['label_parts_font_size'],
            sg.BLACK,
            (self.data['label_parts_x'],
             self.data['label_parts_y']))
        # 問題文(意味)の作成
        self.label_question = Label(
            self.random_question_list[self.get_current_question()][sg.MEAN_NUM],
            self.data['label_question_font_size'],
            sg.BLACK,
            (self.data['label_question_x'],
             self.data['label_question_y']))
        # メニューボタンの作成
        self.button_menu = Button(
            (self.data['button_menu_x'],
             self.data['button_menu_y']),
            (self.data['button_menu_width'],
             self.data['button_menu_height']),
            'Menu',
            sg.BUTTON_COLOR,
            sg.BUTTON_HOVER_COLOR,
            sg.WHITE,
            self.data['button_menu_font_size'],
            self.view_button_menu,
            self.sound_player
        )
        # グレーのサーフェスを作成
        self.gray_surface = Surface(
            (sg.SCREEN_WIDTH, sg.SCREEN_HEIGHT),
            sg.GRAY,
            self.data['gray_surface_alpha']
        )
        # サブスクリーンの作成
        self.sub_screen = OnBorderSubScreen(
            screen,
            (self.data['sub_screen_width'],
             self.data['sub_screen_height']),
            sg.WHITE,
            self.data['sub_screen_border_width'],
            sg.BLACK
        )
        # サブスクリーンに表示するボタン
        # プレイを続けるボタンを作成
        self.button_back_game_play_screen = Button(
            (self.data['button_back_game_play_screen_x'],
             self.data['button_back_game_play_screen_y']),
            (self.data['button_back_game_play_screen_width'],
             self.data['button_back_game_play_screen_height']),
            'プレイを続ける',
            sg.BUTTON_COLOR,
            sg.BUTTON_HOVER_COLOR,
            sg.WHITE,
            self.data['button_back_game_play_screen_font_size'],
            self.button_menu_flg_false,
            self.sound_player
        )
        # ゲーム設定へ戻るボタンを作成
        self.button_back_game_setting_screen = Button(
            (self.data['button_back_game_setting_screen_x'],
             self.data['button_back_game_setting_screen_y']),
            (self.data['button_back_game_setting_screen_width'],
             self.data['button_back_game_setting_screen_height']),
            'ゲーム設定へ戻る',
            sg.BUTTON_COLOR,
            sg.BUTTON_HOVER_COLOR,
            sg.WHITE,
            self.data['button_back_game_setting_screen_font_size'],
            self.go_game_setting_screen,
            self.sound_player
        )
        # タイトルへ戻るボタンを作成
        self.button_back_title_screen = Button(
            (self.data['button_back_title_screen_x'],
             self.data['button_back_title_screen_y']),
            (self.data['button_back_title_screen_width'],
             self.data['button_back_title_screen_height']),
            'タイトルへ戻る',
            sg.BUTTON_COLOR,
            sg.BUTTON_HOVER_COLOR,
            sg.WHITE,
            self.data['button_back_title_screen_font_size'],
            self.go_title_screen,
            self.sound_player
        )
        self.EVENT_PARTS = [self.label_current_life,
                            self.text_box_answer,
                            self.label_parts,
                            self.label_question,
                            self.button_menu,
                            self.gray_surface,
                            self.sub_screen,
                            ]
        # サブスクリーンに表示されるボタンを格納したリスト
        self.SUB_SCREEN_PARTS = [self.button_back_game_play_screen,
                                 self.button_back_game_setting_screen,
                                 self.button_back_title_screen,
                                 ]

    def on_event(self, event):
        """ イベント処理を行うメソッド """
        super().on_event(event)
        # button_menu_flgがTrueの場合
        if self.button_menu_flg:
            # text_boxのイベント処理を停止する(キー入力ができなくなる)
            self.text_box_answer.is_active_false()
            # button_menuのイベント処理を停止する
            self.button_menu.is_event_false()
            # button_back_game_play_screenのイベント処理を受け付ける
            for parts in self.SUB_SCREEN_PARTS:
                parts.is_event_true()
                parts.handle_event(event)
        # button_menu_flgがFalseの場合
        else:
            # text_boxのイベント処理を受け付ける(キー入力を受けつける)
            self.text_box_answer.is_active_true()
            # button_menuのイベント処理を受け付ける(クリック入力を受けつける)
            self.button_menu.is_event_true()
            # button_back_game_play_screenのイベント処理を停止する
            for parts in self.SUB_SCREEN_PARTS:
                parts.is_event_false()

            # キー入力が行われた場合
            if event.type == pygame.KEYDOWN:
                # Enterキーが押された場合
                if event.key == pygame.K_RETURN:
                    # 正誤判定
                    self.game_system.check_answer(
                        self.text_box_answer.get_text(), self.get_current_question())
                    # lifeチェック
                    self.label_current_life.update_loop_num(self.game_system.get_life())
                    # 残りライフ確認
                    if self.game_system.check_life():
                        # ライフが0ならゲームオーバーとしてスコア画面へ遷移する
                        self.go_game_score_screen(
                            self.game_system.get_score(),
                            self.game_system.get_mistake(),
                            'GAME OVER!'
                        )
                    else:
                        pass
                    # 次の問題を参照するためにcurrent_questionを+1する
                    self.add_current_question()
                    # 次の問題の有無によって変える
                    # あるなら次の問題へ
                    if self.game_system.check_next_question(self.get_current_question()):
                        # 回答欄をクリアする
                        self.text_box_answer.clear_text()
                        # 次の問題へ
                        self.update_question()
                    # ないならスコア画面へ
                    else:
                        # プラクティスモードの場合
                        if self.game_system.get_practice_flg():
                            # 練習終了としてスコア画面へ遷移する
                            self.go_game_score_screen(
                                self.game_system.get_score(),
                                self.game_system.get_mistake(),
                                'PRACTICE FINISH!',
                            )
                        # それ以外の場合
                        else:
                            # ゲームクリアとしてスコア画面へ遷移する
                            self.go_game_score_screen(
                                self.game_system.get_score(),
                                self.game_system.get_mistake(),
                                'GAME CLEAR!',
                            )

                # Enterキー以外は何もしない
                else:
                    pass
            # キー入力以外は何もしない
            else:
                pass

    def on_draw(self):
        """
        描画処理を行うメソッド
        button_menu_flgがTrue: button_menuを描画せず,サブスクリーンを描画する
        button_menu_flgがFalse: button_menuを描画して,サブスクリーンは描画しない
        """
        super().on_draw()
        # button_menu_flgがTrueの場合
        if self.button_menu_flg:
            # button_menuを描画
            self.button_menu.is_draw_false()
            # self.gray_surfaceを描画
            self.gray_surface.is_active_true()
            # self.sub_screenを描画
            self.sub_screen.is_active_true()
            # 各種ボタンを描画
            for parts in self.SUB_SCREEN_PARTS:
                parts.is_draw_true()
                parts.draw(self.screen)
        # button_menu_flgがFalseの場合
        else:
            # button_menuを描画
            self.button_menu.is_draw_true()
            # self.gray_surfaceを非表示
            self.gray_surface.is_active_false()
            # self.sub_screenを非表示
            self.sub_screen.is_active_false()
            # 各種ボタンを非表示
            for parts in self.SUB_SCREEN_PARTS:
                parts.is_draw_false()

    def judge_diff(self, diff):
        if diff == 'EASY':
            self.set_diff_easy()
        elif diff == 'NORMAL':
            self.set_diff_normal()
        elif diff == 'HARD':
            self.set_diff_hard()

    def judge_game_mode(self, game_mode):
        if game_mode == 'STANDARD':
            self.set_game_mode_standard()
        elif game_mode == 'PRACTICE':
            self.set_game_mode_practice()
        elif game_mode == 'ENDLESS':
            self.set_game_mode_endless()

    def view_button_menu(self):
        """
        button_menuがクリックされたら
        button_menu_flgのTrue,Falseを切り替えるメソッド
        """
        if self.button_menu_flg:
            self.button_menu_flg_false()
        else:
            self.button_menu_flg_true()

    def button_menu_flg_true(self):
        """ button_menu_flg変数にTrueを格納するメソッド """
        self.button_menu_flg = True

    def button_menu_flg_false(self):
        """ button_menu_flg変数にFalseを格納するメソッド """
        self.button_menu_flg = False

    def create_game_mode_inst(self):
        """
        選択されたgame_modeに沿ったインスタンスを生成し、返すメソッド
        :return: インスタンス
        """
        if self.game_mode == 'STANDARD':
            return StandardMode(self.difficulty, self.sound_player)
        elif self.game_mode == 'PRACTICE':
            return PracticeMode(self.difficulty, self.sound_player)
        elif self.game_mode == 'ENDLESS':
            return EndlessMode(self.difficulty, self.sound_player)

    def update_question(self):
        """ 問題文を更新するメソッド """
        # 問題文を更新する
        # 品詞
        self.label_parts.update_text(
            self.random_question_list[self.get_current_question()][sg.PART_NUM])
        # 意味
        self.label_question.update_text(
            self.random_question_list[self.get_current_question()][sg.MEAN_NUM])


class GameScoreScreen(BaseScreen):
    """ スコア画面を作成するクラス """

    def __init__(self, screen, change_screen_callback, sound_player, game_score, game_mistake, result_text):
        super().__init__(screen, change_screen_callback, sound_player)
        # 各settingsをtxtファイルから読み込み,辞書型のdata変数に格納
        self.data = read_variable_file('settings/GameScoreScreen.txt')
        # リザルトラベルを作成
        self.label_result = Label(
            result_text,
            self.data['label_result_font_size'],
            sg.BLACK,
            (self.data['label_result_x'],
             self.data['label_result_y'])
        )
        # 直前のゲームのスコアを表示するラベルを作成
        self.label_game_score = Label(
            f'スコア：{game_score}点',
            self.data['label_game_score_font_size'],
            sg.BLACK,
            (self.data['label_game_score_x'],
             self.data['label_game_score_y'])
        )
        # 直前のゲームのスコアを表示するラベルを作成
        self.label_game_mistake = Label(
            f'失敗した回数：{game_mistake}回',
            self.data['label_game_mistake_font_size'],
            sg.BLACK,
            (self.data['label_game_mistake_x'],
             self.data['label_game_mistake_y'])
        )
        # 「リトライ」ボタンを作成
        self.button_retry = Button(
            (self.data['button_retry_x'],
             self.data['button_retry_y']),
            (self.data['button_retry_width'],
             self.data['button_retry_height']),
            'リトライ',
            sg.BUTTON_COLOR,
            sg.BUTTON_HOVER_COLOR,
            sg.WHITE,
            self.data['button_retry_font_size'],
            self.go_game_setting_screen,
            self.sound_player
        )
        # 「タイトルへ戻る」ボタンを作成
        self.button_back_title = Button(
            (self.data['button_back_title_x'],
             self.data['button_back_title_y']),
            (self.data['button_back_title_width'],
             self.data['button_back_title_height']),
            'タイトルへ戻る',
            sg.BUTTON_COLOR,
            sg.BUTTON_HOVER_COLOR,
            sg.WHITE,
            self.data['button_back_title_font_size'],
            self.go_title_screen,
            self.sound_player
        )
        self.EVENT_PARTS = [self.label_result,
                            self.label_game_score,
                            self.label_game_mistake,
                            self.button_retry,
                            self.button_back_title,
                            ]


class SystemSettingsScreen(BaseScreen):
    """ システム設定画面を作成するクラス """

    def __init__(self, screen, change_screen_callback, sound_player):
        super().__init__(screen, change_screen_callback, sound_player)
        # 各settingsをtxtファイルから読み込み,辞書型のdata変数に格納
        self.data = read_variable_file('settings/SystemSettingsScreen.txt')
        # 戻るボタン
        self.button_back_title = ArrowButton(
            sg.BUTTON_BACK_POS,
            sg.BUTTON_BACK_SIZE,
            sg.BUTTON_BACK_TEXT,
            sg.BUTTON_COLOR,
            sg.BUTTON_HOVER_COLOR,
            sg.WHITE,
            sg.BUTTON_BACK_FONT_SIZE,
            self.go_title_screen,
            self.sound_player
        )
        self.label_volume = Label(
            '音量',
            self.data['label_volume_font_size'],
            sg.BLACK,
            (self.data['label_volume_x'],
             self.data['label_volume_y'])
        )
        self.label_se_volume = Label(
            'SE',
            self.data['label_se_volume_font_size'],
            sg.BLACK,
            (self.data['label_se_volume_x'],
             self.data['label_se_volume_y'])
        )
        # -ボタン
        self.button_se_volume_sub = Button(
            (self.data['button_se_volume_sub_x'],
             self.data['button_se_volume_sub_y']),
            (self.data['button_se_volume_width'],
             self.data['button_se_volume_height']),
            '-',
            sg.BLACK,
            sg.BLACK,
            sg.WHITE,
            self.data['button_se_volume_font_size'],
            self.sound_player.sub_se_volume,
            self.sound_player
        )
        # +ボタン
        self.button_se_volume_add = Button(
            (self.data['button_se_volume_add_x'],
             self.data['button_se_volume_add_y']),
            (self.data['button_se_volume_width'],
             self.data['button_se_volume_height']),
            '+',
            sg.BLACK,
            sg.BLACK,
            sg.WHITE,
            self.data['button_se_volume_font_size'],
            self.sound_player.add_se_volume,
            self.sound_player
        )
        # 設定音量ラベル
        self.label_show_se_volume = Label(
            '',
            self.data['label_show_se_volume_font_size'],
            sg.BLACK,
            (self.data['label_show_se_volume_x'],
             self.data['label_show_se_volume_y'])
        )
        self.EVENT_PARTS = [self.button_back_title,
                            self.label_volume,
                            self.label_se_volume,
                            self.button_se_volume_sub,
                            self.button_se_volume_add,
                            self.label_show_se_volume,
                            ]

    def on_draw(self):
        super().on_draw()
        self.update_label()

    def update_label(self):
        self.label_show_se_volume.update_text(str(self.sound_player.get_se_volume()))


if __name__ == '__main__':
    pass
