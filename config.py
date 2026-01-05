"""
Конфигурационные параметры игры
"""

# Пути к файлам
SAVE_DIR = "data/saves/"
ARTIFACTS_FILE = "data/artifacts.json"
PASSWORDS_FILE = "data/passwords.txt"

# Игровые константы
PLAYER_HP = 100
PLAYER_DAMAGE = 20
PLAYER_DEFENSE = 10

BOSS_HP = 300
BOSS_DAMAGE = 30
BOSS_DEFENSE = 15

# Доступные артефакты
ARTIFACTS = {
    "Меч Посейдона": {"damage": 15, "defense": 5},
    "Щит Тритона": {"damage": 5, "defense": 20},
    "Компас судьбы": {"damage": 10, "defense": 10},
    "Кристалл глубины": {"damage": 20, "defense": 0},
    "Накидка тумана": {"damage": 0, "defense": 25}
}

# Ключевые решения
DECISIONS = {
    1: "Путь Учёного (контроль силы)",
    2: "Путь Консерватора (уничтожение силы)",
    3: "Путь Тирана (использование силы)",
    4: "Путь Симбиоза (баланс)"
}