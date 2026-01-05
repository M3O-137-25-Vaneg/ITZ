"""
Управление артефактами и коллекцией
"""

import json
import os
from config import ARTIFACTS
from utils.helpers import print_header, save_json, load_json

class ArtifactCollection:
    """Коллекция артефактов игрока"""

    def __init__(self, player):
        self.player = player
        self.collected = []
        self.storage_file = "data/artifacts.json"
        self.load_collection()

    def load_collection(self):
        """Загрузка коллекции из файла"""
        data = load_json(self.storage_file)
        if "collected" in data:
            self.collected = data["collected"]

    def save_collection(self):
        """Сохранение коллекции в файл"""
        data = {
            "collected": self.collected,
            "player": self.player.name
        }
        save_json(data, self.storage_file)

    def add_artifact(self, artifact_name):
        """Добавление артефакта в коллекцию"""
        if artifact_name in ARTIFACTS and artifact_name not in self.collected:
            self.collected.append(artifact_name)
            self.save_collection()
            return True
        return False

    def show_collection(self):
        """Показ коллекции артефактов"""
        if not self.collected:
            print("Ваша коллекция артефактов пуста.")
            return

        print_header("КОЛЛЕКЦИЯ АРТЕФАКТОВ")
        for i, artifact in enumerate(self.collected, 1):
            stats = ARTIFACTS.get(artifact, {})
            print(f"{i}. {artifact}")
            if stats:
                bonuses = []
                if "damage" in stats and stats["damage"] > 0:
                    bonuses.append(f"Урон: +{stats['damage']}")
                if "defense" in stats and stats["defense"] > 0:
                    bonuses.append(f"Защита: +{stats['defense']}")
                if bonuses:
                    print(f"   ({', '.join(bonuses)})")

        print(f"\nВсего артефактов: {len(self.collected)}/{len(ARTIFACTS)}")

        # Показываем экипированные артефакты
        if self.player.artifacts:
            print(f"\nЭкипированные артефакты: {', '.join(self.player.artifacts)}")

    def get_artifact_stats(self):
        """Получение общей статистики от артефактов"""
        total_damage = 0
        total_defense = 0

        for artifact in self.player.artifacts:
            if artifact in ARTIFACTS:
                stats = ARTIFACTS[artifact]
                total_damage += stats.get("damage", 0)
                total_defense += stats.get("defense", 0)

        return {
            "damage_bonus": total_damage,
            "defense_bonus": total_defense
        }

    def return_all_to_storage(self):
        """Возврат всех артефактов в хранилище"""
        returned = self.collected.copy()
        self.collected.clear()
        self.save_collection()
        print("Все артефакты возвращены в хранилище.")
        return returned