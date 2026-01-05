"""
Класс боссов и врагов
"""

import random
from config import BOSS_HP, BOSS_DAMAGE, BOSS_DEFENSE

class Boss:
    """Класс босса (Песнь Бездны)"""

    def __init__(self, name="Песнь Бездны"):
        self.name = name
        self.max_hp = BOSS_HP
        self.hp = BOSS_HP
        self.damage = BOSS_DAMAGE
        self.defense = BOSS_DEFENSE
        self.phase = 1
        self.special_attack_cooldown = 0

    def take_damage(self, damage):
        """Получение урона боссом"""
        actual_damage = max(1, damage - self.defense // 3)
        self.hp -= actual_damage

        # Смена фазы при 50% HP
        if self.hp <= self.max_hp // 2 and self.phase == 1:
            self.phase = 2
            self.damage += 10
            print(f"{self.name} впадает в ярость! Урон увеличен!")

        return actual_damage

    def attack(self):
        """Атака босса"""
        base_attack = random.randint(self.damage - 5, self.damage + 5)

        # Особые атаки в зависимости от фазы
        if self.phase == 2 and self.special_attack_cooldown <= 0:
            if random.random() < 0.3:  # 30% шанс особой атаки
                self.special_attack_cooldown = 3
                return self.special_attack()

        if self.special_attack_cooldown > 0:
            self.special_attack_cooldown -= 1

        return {"type": "normal", "damage": base_attack}

    def special_attack(self):
        """Особая атака"""
        attacks = [
            {"type": "whirlpool", "damage": self.damage * 2, "name": "Водоворот Бездны"},
            {"type": "song", "damage": self.damage, "name": "Песнь Безумия", "effect": "confusion"},
            {"type": "tentacles", "damage": self.damage * 1.5, "name": "Щупальца Глубин"}
        ]
        return random.choice(attacks)

    def is_alive(self):
        """Проверка, жив ли босс"""
        return self.hp > 0

    def get_stats(self):
        """Получение статистики босса"""
        return {
            "name": self.name,
            "hp": f"{self.hp}/{self.max_hp}",
            "phase": self.phase,
            "damage": self.damage,
            "defense": self.defense
        }


class PirateLord:
    """Класс пиратского лорда"""

    def __init__(self, lord_type):
        self.types = {
            "scientist": {"name": "Учёный", "hp": 150, "damage": 25, "defense": 10},
            "conservator": {"name": "Консерватор", "hp": 200, "damage": 20, "defense": 20},
            "tyrant": {"name": "Тиран", "hp": 180, "damage": 30, "defense": 15}
        }

        if lord_type not in self.types:
            lord_type = "scientist"  # Значение по умолчанию

        self.type = lord_type
        self.stats = self.types[lord_type]
        self.name = self.stats["name"]
        self.max_hp = self.stats["hp"]
        self.hp = self.stats["hp"]
        self.damage = self.stats["damage"]
        self.defense = self.stats["defense"]
        self.dialogue_options = []

    def take_damage(self, damage):
        """Получение урона"""
        actual_damage = max(1, damage - self.defense // 2)
        self.hp -= actual_damage
        if self.hp < 0:
            self.hp = 0
        return actual_damage

    def attack(self):
        """Атака пиратского лорда"""
        return random.randint(self.damage - 5, self.damage + 5)

    def is_alive(self):
        """Проверка, жив ли лорд"""
        return self.hp > 0

    def get_stats(self):
        """Получение статистики лорда"""
        return {
            "name": self.name,
            "hp": f"{self.hp}/{self.max_hp}",
            "damage": self.damage,
            "defense": self.defense,
            "type": self.type
        }