#!/usr/bin/env python3
"""
Главный файл игры "Пиратские сражения: Песнь Бездны"
"""

import os
import sys

# Добавление пути к модулям
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from game.save_system import SaveSystem
from game.player import Player
from game.story import StoryManager
from game.locations import GameLocations
from game.artifacts import ArtifactCollection
from utils.helpers import (
    clear_screen, print_header,
    print_menu, get_choice
)

class PirateGame:
    """Основной класс игры"""

    def __init__(self):
        # Создаём необходимые директории
        os.makedirs("data/saves", exist_ok=True)

        self.save_system = SaveSystem()
        self.player = None
        self.story = None
        self.locations = None
        self.artifacts = None
        self.current_save = None
        self.game_active = False

    def main_menu(self):
        """Главное меню игры"""
        clear_screen()
        print_header("ПИРАТСКИЕ СРАЖЕНИЯ: ПЕСНЬ БЕЗДНЫ")

        print("Добро пожаловать в игру, капитан!")
        print("Вы - Элиас Шоу, пират с прошлым офицера.")
        print("Ваш корабль потерпел крушение на Блуждающем Рифе...")

        print("\nВыберите действие:")
        print_menu([
            "Новая игра",
            "Загрузить игру",
            "Об игре",
            "Выход"
        ])

        choice = get_choice(1, 4)

        if choice == 1:
            self.new_game()
        elif choice == 2:
            self.load_game()
        elif choice == 3:
            self.show_about()
        elif choice == 4:
            self.exit_game()

    def new_game(self):
        """Создание новой игры"""
        clear_screen()
        print_header("НОВАЯ ИГРА")

        print("Введите логин для нового сохранения:")
        login = input("Логин: ").strip()

        if not login:
            print("Логин не может быть пустым!")
            input("Нажмите Enter для продолжения...")
            self.new_game()
            return

        # Проверка доступности логина
        if not self.save_system.check_login_available(login):
            print(f"Логин '{login}' уже занят!")
            print("Выберите другой или загрузите существующее сохранение.")
            input("Нажмите Enter для продолжения...")
            self.main_menu()
            return

        print("\nВведите пароль для сохранения:")
        password = input("Пароль: ").strip()

        if not password:
            print("Пароль не может быть пустым!")
            input("Нажмите Enter для продолжения...")
            self.new_game()
            return

        # Создание игрока
        self.player = Player()
        self.story = StoryManager()
        self.locations = GameLocations()
        self.artifacts = ArtifactCollection(self.player)

        # Создание сохранения
        player_data = self.player.get_stats()
        story_progress = self.story.get_story_progress()

        save_data = {
            "login": login,
            "player": player_data,
            "story": story_progress,
            "artifacts_collected": self.artifacts.collected,
            "locations_visited": []
        }

        self.current_save = self.save_system.create_new_save(login, password, save_data)
        self.game_active = True

        print(f"\nИгра создана для логина: {login}")
        print("Запомните пароль для загрузки игры!")
        input("\nНажмите Enter чтобы начать приключение...")

        self.start_game()

    def load_game(self):
        """Загрузка существующей игры"""
        clear_screen()
        print_header("ЗАГРУЗКА ИГРЫ")

        saves = self.save_system.get_save_list()

        if not saves:
            print("Нет доступных сохранений!")
            input("Нажмите Enter для возврата в меню...")
            self.main_menu()
            return

        print("Доступные сохранения:")
        for i, save in enumerate(saves, 1):
            print(f"{i}. {save}")

        print(f"\n{len(saves) + 1}. Назад в меню")

        choice = get_choice(1, len(saves) + 1)

        if choice == len(saves) + 1:
            self.main_menu()
            return

        login = saves[choice - 1]

        print(f"\nВведите пароль для сохранения '{login}':")
        password = input("Пароль: ").strip()

        # Проверка пароля
        if not self.save_system.verify_password(login, password):
            print("Неверный пароль!")
            input("Нажмите Enter для продолжения...")
            self.load_game()
            return

        # Загрузка сохранения
        self.current_save = self.save_system.load_save(login)

        if not self.current_save:
            print("Ошибка загрузки сохранения!")
            input("Нажмите Enter для продолжения...")
            self.main_menu()
            return

        # Восстановление состояния игры
        self.player = Player()
        player_data = self.current_save.get("player", {})

        # Восстановление данных игрока
        if "hp" in player_data:
            hp_str = player_data["hp"]
            if "/" in hp_str:
                current_hp, max_hp = map(int, hp_str.split("/"))
                self.player.hp = current_hp
                self.player.max_hp = max_hp

        if "damage" in player_data:
            self.player.damage = player_data["damage"]
        if "defense" in player_data:
            self.player.defense = player_data["defense"]
        if "artifacts" in player_data:
            for artifact in player_data["artifacts"]:
                self.player.equip_artifact(artifact)
        if "path" in player_data:
            self.player.chosen_path = player_data["path"]
        if "morality" in player_data:
            self.player.morality = player_data["morality"]
        if "crew_loyalty" in player_data:
            self.player.crew_loyalty = player_data["crew_loyalty"]
        if "morvanna_trust" in player_data:
            self.player.morvanna_trust = player_data["morvanna_trust"]

        self.story = StoryManager()
        self.locations = GameLocations()
        self.artifacts = ArtifactCollection(self.player)

        # Восстановление коллекции артефактов
        if "artifacts_collected" in self.current_save:
            for artifact in self.current_save["artifacts_collected"]:
                self.artifacts.add_artifact(artifact)

        # Восстановление прогресса сюжета
        if "story_progress" in self.current_save:
            story_data = self.current_save["story_progress"]
            if "chapter" in story_data:
                self.story.current_chapter = story_data["chapter"]
            if "decisions" in story_data:
                self.story.decisions = story_data["decisions"]

        self.game_active = True

        print(f"\nИгра загружена: {login}")
        print(f"Прогресс: Глава {self.story.current_chapter}")
        input("\nНажмите Enter чтобы продолжить...")

        self.start_game()

    def start_game(self):
        """Начало игрового процесса"""
        if not self.game_active or not self.player:
            print("Ошибка: игра не инициализирована!")
            self.main_menu()
            return

        # Игровой цикл
        while self.game_active and self.player.is_alive():
            self.game_loop()

    def game_loop(self):
        """Основной игровой цикл"""
        clear_screen()

        # Показ статуса игрока
        self.show_player_status()

        # Меню действий
        print("\nВыберите действие:")
        print_menu([
            "Продолжить историю",
            "Исследовать локации",
            "Показать коллекцию артефактов",
            "Сохранить игру",
            "Выйти в главное меню"
        ])

        choice = get_choice(1, 5)

        if choice == 1:
            self.continue_story()
        elif choice == 2:
            self.explore_locations()
        elif choice == 3:
            self.show_artifact_collection()
        elif choice == 4:
            self.save_game()
        elif choice == 5:
            self.return_to_menu()

    def continue_story(self):
        """Продолжение сюжета"""
        print(f"\nПродолжение главы {self.story.current_chapter}...")
        if self.story.play_chapter(self.story.current_chapter, self.player):
            self.story.current_chapter += 1

            # Обновление сохранения
            if self.current_save:
                self.current_save["story_progress"]["chapter"] = self.story.current_chapter
                self.current_save["story_progress"]["decisions"] = self.story.decisions

            # Проверка на конец игры
            if self.story.current_chapter > 5:
                self.end_game()
                return

        input("\nНажмите Enter чтобы продолжить...")

    def explore_locations(self):
        """Исследование локаций"""
        clear_screen()
        print_header("ИССЛЕДОВАНИЕ ЛОКАЦИЙ")

        location_ids = list(self.locations.locations.keys())

        print("Доступные локации:")
        for i, loc_id in enumerate(location_ids, 1):
            location = self.locations.locations[loc_id]
            visited = " ✓" if location.visited else ""
            print(f"{i}. {location.name}{visited}")

        print(f"\n{len(location_ids) + 1}. Вернуться")

        choice = get_choice(1, len(location_ids) + 1)

        if choice == len(location_ids) + 1:
            return

        selected_id = location_ids[choice - 1]
        location = self.locations.locations[selected_id]

        location.visit(self.player)

        # Добавление в посещенные локации
        if self.current_save and selected_id not in self.current_save.get("locations_visited", []):
            self.current_save.setdefault("locations_visited", []).append(selected_id)

        input("\nНажмите Enter чтобы продолжить...")

    def show_artifact_collection(self):
        """Показ коллекции артефактов"""
        clear_screen()
        self.artifacts.show_collection()
        input("\nНажмите Enter чтобы продолжить...")

    def save_game(self):
        """Сохранение игры"""
        if not self.current_save or not self.player:
            print("Невозможно сохранить игру!")
            input("\nНажмите Enter чтобы продолжить...")
            return

        print("\nСохранить игру?")
        print_menu(["Да", "Нет"])

        choice = get_choice(1, 2)

        if choice == 1:
            # Обновление данных игрока
            self.current_save["player"] = self.player.get_stats()
            self.current_save["artifacts_collected"] = self.artifacts.collected

            # Сохранение
            self.save_system.update_save(self.current_save["login"], self.current_save)
            print("Игра сохранена!")
        else:
            print("Игра не сохранена. Прогресс будет утерян!")
            # Возврат артефактов в хранилище
            returned = self.artifacts.return_all_to_storage()
            self.save_system.return_artifacts_to_storage(returned)

        input("\nНажмите Enter чтобы продолжить...")

    def return_to_menu(self):
        """Возврат в главное меню"""
        print("\nВернуться в главное меню?")
        print("Несохраненный прогресс будет утерян!")
        print_menu(["Да", "Нет"])

        choice = get_choice(1, 2)

        if choice == 1:
            self.game_active = False
            self.main_menu()

    def show_player_status(self):
        """Показ статуса игрока"""
        print_header("СТАТУС ИГРОКА")

        stats = self.player.get_stats()

        print(f"Капитан: {stats['name']}")
        print(f"Здоровье: {stats['hp']}")
        print(f"Урон: {stats['damage']}")
        print(f"Защита: {stats['defense']}")

        if stats['path']:
            from config import DECISIONS
            path_name = DECISIONS.get(stats['path'], "Не выбран")
            print(f"Путь: {path_name}")

        print(f"\nМораль: {stats['morality']}/100")
        print(f"Лояльность команды: {stats['crew_loyalty']}/100")
        print(f"Доверие Морванны: {stats['morvanna_trust']}/100")

        if stats['artifacts']:
            print(f"\nЭкипированные артефакты: {', '.join(stats['artifacts'])}")

    def end_game(self):
        """Завершение игры"""
        clear_screen()
        print_header("КОНЕЦ ИГРЫ")

        print("Ваше приключение подошло к концу, капитан.")
        print("Спасибо за игру!")

        self.game_active = False
        input("\nНажмите Enter чтобы вернуться в главное меню...")
        self.main_menu()

    def show_about(self):
        """Показ информации об игре"""
        clear_screen()
        print_header("ОБ ИГРЕ")

        print("ПИРАТСКИЕ СРАЖЕНИЯ: ПЕСНЬ БЕЗДНЫ")
        print("Текстовая RPG игра с элементами выбора и битв")
        print("\nОсобенности:")
        print("- 4 разные концовки в зависимости от ваших выборов")
        print("- Система сохранений с паролями")
        print("- Коллекция артефактов с уникальными эффектами")
        print("- Динамическая система битв с боссами")
        print("- Ветвящийся сюжет с моральными выборами")

        print("\nУправление:")
        print("Используйте цифры для выбора вариантов")
        print("Регулярно сохраняйте игру!")

        input("\nНажмите Enter чтобы вернуться в меню...")
        self.main_menu()

    def exit_game(self):
        """Выход из игры"""
        clear_screen()
        print("Спасибо за игру! До свидания, капитан!")
        sys.exit(0)


def main():
    """Основная функция запуска"""
    game = PirateGame()
    game.main_menu()


if __name__ == "__main__":
    main()