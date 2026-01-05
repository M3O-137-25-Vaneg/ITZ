"""
Система сохранений игры
"""

import os
import json
from datetime import datetime
from config import SAVE_DIR, PASSWORDS_FILE, ARTIFACTS_FILE
from utils.helpers import save_json, load_json, get_choice

class SaveSystem:
    """Класс для управления сохранениями"""

    def __init__(self):
        self.saves_dir = SAVE_DIR
        self.passwords_file = PASSWORDS_FILE
        self.artifacts_file = ARTIFACTS_FILE
        self.ensure_directories()

    def ensure_directories(self):
        """Создание необходимых директорий"""
        os.makedirs(self.saves_dir, exist_ok=True)
        os.makedirs(os.path.dirname(self.passwords_file), exist_ok=True)
        os.makedirs(os.path.dirname(self.artifacts_file), exist_ok=True)

    def check_login_available(self, login):
        """Проверка, доступен ли логин"""
        save_path = os.path.join(self.saves_dir, f"{login}.json")
        return not os.path.exists(save_path)

    def verify_password(self, login, password):
        """Проверка пароля"""
        try:
            with open(self.passwords_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if ':' in line:
                        saved_login, saved_pass = line.split(':', 1)
                        if saved_login == login and saved_pass == password:
                            return True
        except FileNotFoundError:
            return False
        return False

    def save_password(self, login, password):
        """Сохранение пароля"""
        with open(self.passwords_file, 'a', encoding='utf-8') as f:
            f.write(f"{login}:{password}\n")

    def create_new_save(self, login, password, player_data):
        """Создание нового сохранения"""
        save_data = {
            "login": login,
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "last_saved": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "player": player_data,
            "story_progress": {
                "chapter": 1,
                "path": None,
                "decisions": [],
                "visited_locations": []
            },
            "artifacts_collected": [],
            "boss_defeated": False
        }

        save_path = os.path.join(self.saves_dir, f"{login}.json")
        save_json(save_data, save_path)
        self.save_password(login, password)

        return save_data

    def load_save(self, login):
        """Загрузка сохранения"""
        save_path = os.path.join(self.saves_dir, f"{login}.json")
        return load_json(save_path)

    def update_save(self, login, save_data):
        """Обновление сохранения"""
        save_data["last_saved"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_path = os.path.join(self.saves_dir, f"{login}.json")
        save_json(save_data, save_path)

    def return_artifacts_to_storage(self, artifacts):
        """Возврат артефактов в хранилище"""
        storage = load_json(self.artifacts_file)
        if "available" not in storage:
            storage["available"] = []

        for artifact in artifacts:
            if artifact not in storage["available"]:
                storage["available"].append(artifact)

        save_json(storage, self.artifacts_file)

    def get_save_list(self):
        """Получение списка сохранений"""
        saves = []
        if os.path.exists(self.saves_dir):
            for filename in os.listdir(self.saves_dir):
                if filename.endswith('.json'):
                    saves.append(filename[:-5])
        return saves