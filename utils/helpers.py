"""
Вспомогательные функции
"""

import os
import json
import sys

def clear_screen():
    """Очистка экрана"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(text):
    """Печать заголовка"""
    print("\n" + "="*60)
    print(f" {text}")
    print("="*60 + "\n")

def print_menu(options):
    """Печать меню с вариантами"""
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")

def get_choice(min_val, max_val):
    """Получение выбора пользователя с валидацией"""
    while True:
        try:
            choice = input("Ваш выбор: ").strip()
            if not choice:
                print("Пожалуйста, введите число")
                continue

            choice = int(choice)
            if min_val <= choice <= max_val:
                return choice
            else:
                print(f"Пожалуйста, введите число от {min_val} до {max_val}")
        except ValueError:
            print("Пожалуйста, введите число")

def load_json(filepath):
    """Загрузка JSON файла"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_json(data, filepath):
    """Сохранение в JSON файл"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)