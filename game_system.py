import random
import setting as sg
from read_file import read_txt_file


def check_value(var, var_name):
    """
    値が格納されているかどうか判定する関数
    :param var: チェックしたい値
    :param var_name: チェックしたい変数名
    """
    # varがNoneの場合
    if var is None:
        # ValueErrorを発生させる
        raise ValueError(f"{var_name} is None")
    # varに値が格納されている場合
    else:
        # 何もしない
        pass


def check_type(var, var_name, expected_type):
    """
    :param var: チェックしたい値
    :param var_name: チェックしたい変数名
    :param expected_type: チェックしたい型
    """
    check_value(var, var_name)
    # varの型がexpected_typeで指定された型以外の場合
    if not isinstance(var, expected_type):
        # TypeErrorを発生させる
        raise TypeError(f"{var_name} should be {expected_type} type")
    # varの型がexpected_typeで指定された型の場合
    else:
        # 何もしない
        pass


class GameSystem:
    """ ゲームシステムに使用するクラス """

    def __init__(self, difficulty, init_life, sound_player):
        """
        :param difficulty: 選択された難易度
        :param init_life:  初期ライフ(数値)
        """
        # SoundPlayerクラスのインスタンス変数
        self.sound_player = sound_player
        # 難易度を保持する変数
        self.difficulty = difficulty
        # ゲームスコアを保持する変数(初期値は0)
        self.score = 0
        # 誤答した回数を保持する変数(初期値は0)
        self.mistake = 0
        # 初期ライフを保持する変数(初期値はゲームモード次第)
        self.life = init_life
        # プラクティスモードのみTrueにする
        self.practice_flg = False
        # 選択された難易度に対応した問題リスト
        self.questions_list = self.select_difficulty()
        # ランダムに抽出した問題リスト
        self.random_q_list = self.make_random_list()

    def select_difficulty(self):
        """ 選択された難易度に応じてリストを選ぶメソッド """
        file_name = ''
        if self.difficulty == 'EASY':
            file_name = 'vocabulary/easy.txt'
        elif self.difficulty == 'NORMAL':
            file_name = 'vocabulary/normal.txt'
        elif self.difficulty == 'HARD':
            file_name = 'vocabulary/hard.txt'
        with open(file_name, encoding='utf-8') as f:
            return read_txt_file(file_name)

    def get_random_list(self):
        """ random_q_listを返すメソッド """
        check_type(self.random_q_list, 'self.random_q_list', list)
        return self.random_q_list

    def add_score(self):
        """ scoreを+1するメソッド """
        check_type(self.score, 'self.score', int)
        self.score += 1

    def add_mistake(self):
        """ mistakeを+1するメソッド """
        check_type(self.mistake, 'self.mistake', int)
        self.mistake += 1

    def get_score(self):
        """ scoreを返すメソッド """
        check_type(self.score, 'self.score', int)
        return self.score

    def get_mistake(self):
        """ mistakeを返すメソッド """
        check_type(self.score, 'self.mistake', int)
        return self.mistake

    def get_life(self):
        """ lifeを返すメソッド """
        check_type(self.life, 'self.life', int)
        return self.life

    def sub_life(self):
        """ lifeを-1するメソッド """
        check_type(self.life, 'self.life', int)
        # lifeが0より大きい場合
        if self.life > 0:
            # lifeを-1する
            self.life -= 1
        # 想定された条件以外の場合
        else:
            # 何もしない
            pass

    def check_life(self):
        """ lifeの値を確認するメソッド """
        check_type(self.life, 'self.life', int)
        # lifeが0より大きい場合
        if self.life > 0:
            return False
        # lifeが0の場合
        elif self.life == 0:
            return True
        # 想定されたの条件以外の場合
        else:
            raise ValueError("self.lifeは0以上でなければならない")

    def check_answer(self, answer, current_num):
        """
        正誤判定をするメソッド

        :param answer: ユーザの回答
        :param current_num: 現在の問題番号
        """
        # 正解の場合
        if answer == self.get_random_list()[current_num][sg.WORD_NUM]:
            # 正解音を鳴らす
            self.sound_player.play_sound('正解')
            # スコアを+1する
            self.add_score()
        # 不正解の場合
        else:
            # 不正解音を鳴らす
            self.sound_player.play_sound('不正解')
            # ミスを+1する
            self.add_mistake()
            if not self.practice_flg:
                # ライフを-1する
                self.sub_life()
            else:
                pass

    def practice_flg_true(self):
        self.practice_flg = True

    def get_practice_flg(self):
        return self.practice_flg

    def make_random_list(self):
        raise NotImplementedError

    def check_next_question(self, current_num):
        """
        次の問題があるかどうか判定するメソッド
        :param current_num: 現在の問題番号
        :return 次の問題があればTrue,なければFalse
        """
        # 次の問題があればTrue
        if not current_num == len(self.get_random_list()):
            return True
        # エラー処理
        elif current_num > len(self.get_random_list()):
            raise ValueError('current_numが想定より大きい数値です')
        # 次の問題がなければFalse
        else:
            return False


class StandardMode(GameSystem):
    """ スタンダードモードのクラス """

    def __init__(self, difficulty, sound_player):
        super().__init__(difficulty, sg.STANDARD_LIFE, sound_player)

    def make_random_list(self):
        """ ランダムに10個の要素を取り出して、被りがないリストを作成 """
        return random.sample(self.questions_list, 10)


class EndlessMode(GameSystem):
    """ エンドレスモードのクラス """

    def __init__(self, difficulty, sound_player):
        super().__init__(difficulty, sg.ENDLESS_LIFE, sound_player)

    def make_random_list(self):
        """ ランダムに要素を取り出して、被りがないリストを作成 """
        return random.sample(self.questions_list, len(self.questions_list))


class PracticeMode(GameSystem):
    """ プラクティスモードのクラス """

    def __init__(self, difficulty, sound_player):
        super().__init__(difficulty, sg.PRACTICE_LIFE, sound_player)
        self.practice_flg_true()

    def make_random_list(self):
        """ ランダムに10個の要素を取り出して、被りがないリストを作成 """
        return random.sample(self.questions_list, 10)


if __name__ == '__main__':
    pass
