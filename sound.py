import pygame
import decimal
from read_file import load_settings, save_settings


class SoundPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.settings_se = load_settings("se")
        self.se_volume = decimal.Decimal(str(self.settings_se))
        self.sounds = {}
        self.sounds_list = [
            ('click_sound', 'sound/click_sound.mp3'),
            ('button_hover_sound', 'sound/button_hover_sound.mp3'),
            ('正解', 'sound/正解.mp3'),
            ('不正解', 'sound/不正解.mp3')
        ]
        self.add_sound()
        self.set_sounds_volume()

    def save_json(self):
        """ jsonファイルに書き込みするメソッド """
        save_settings("se", float(self.get_se_volume()))

    def add_sound(self):
        """ 各サウンドに音量を設定するメソッド """
        for name, path in self.sounds_list:
            self.sounds[name] = pygame.mixer.Sound(path)
            self.sounds[name].set_volume(float(self.settings_se))

    def set_sounds_volume(self):
        """ se_volumeを設定するメソッド """
        for name in self.sounds:
            self.sounds[name].set_volume(float(self.get_se_volume()))

    def sub_se_volume(self):
        if self.get_se_volume() > 0.0:
            self.se_volume -= decimal.Decimal('0.1')
            self.set_sounds_volume()

    def add_se_volume(self):
        if self.get_se_volume() < 1.0:
            self.se_volume += decimal.Decimal('0.1')
            self.set_sounds_volume()

    def get_se_volume(self):
        """ se_volumeを返すメソッド """
        return self.se_volume

    def play_sound(self, name):
        """
        音を鳴らすメソッド
        :param name: 鳴らしたい音の名前
        """
        if name in self.sounds:
            self.sounds[name].play()
        else:
            print(f"{name} is not registered as a sound.")


if __name__ == '__main__':
    pass
