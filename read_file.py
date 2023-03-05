import json


def save_settings(name, volume):
    settings = {name: volume}
    with open("settings.json", "w", encoding="utf-8") as f:
        json.dump(settings, f)


def load_settings(name):
    with open("settings.json", "r", encoding='utf-8') as f:
        settings = json.load(f)
        return settings.get(name)


def read_txt_file(file_name):
    with open(file_name, "r", encoding='utf-8') as f:
        return [line.strip().split(',') for line in f]
