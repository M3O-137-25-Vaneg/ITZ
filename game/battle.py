"""
Система битвы
"""

import random
import time
from utils.helpers import print_header, get_choice, clear_screen, print_menu

class BattleSystem:
    """Система проведения битв"""

    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.turn = 1

    def start_battle(self):
        """Начало битвы"""
        clear_screen()
        print_header(f"БИТВА: {self.player.name} vs {self.enemy.name}")

        enemy_max_hp = getattr(self.enemy, 'max_hp', self.enemy.hp)
        print(f"\n{self.player.name}: {self.player.hp}/{self.player.max_hp} HP")
        print(f"{self.enemy.name}: {self.enemy.hp}/{enemy_max_hp} HP")

        input("\nНажмите Enter чтобы начать битву...")

        while self.player.is_alive() and self.enemy.is_alive():
            print(f"\n--- Ход {self.turn} ---")
            print(f"{self.player.name}: {self.player.hp}/{self.player.max_hp} HP")
            print(f"{self.enemy.name}: {self.enemy.hp}/{enemy_max_hp} HP")

            # Ход игрока
            self.player_turn()
            if not self.enemy.is_alive():
                break

            # Ход врага
            self.enemy_turn()
            if not self.player.is_alive():
                break

            self.turn += 1
            time.sleep(1)

        return self.check_victory()

    def player_turn(self):
        """Ход игрока"""
        print(f"\n--- Ваш ход ---")
        print_menu(["Атаковать", "Защищаться", "Использовать артефакт"])

        choice = get_choice(1, 3)

        if choice == 1:
            damage = random.randint(self.player.damage - 5, self.player.damage + 5)
            actual_damage = self.enemy.take_damage(damage)
            print(f"Вы нанесли {actual_damage} урона {self.enemy.name}!")

        elif choice == 2:
            # Увеличение защиты на этот ход
            defense_boost = self.player.defense // 2
            original_defense = self.player.defense
            self.player.defense += defense_boost
            print(f"Вы защищаетесь! Защита увеличена на {defense_boost}")

            # Враг атакует с уменьшенным уроном
            enemy_attack = self.enemy.attack()
            if isinstance(enemy_attack, dict):
                damage = enemy_attack["damage"] // 2
            else:
                damage = enemy_attack // 2

            actual_damage = self.player.take_damage(damage)
            print(f"{self.enemy.name} атакует, но вы защищаетесь! Получено {actual_damage} урона")

            # Возврат защиты к исходному значению
            self.player.defense = original_defense

        elif choice == 3:
            if self.player.artifacts:
                print("Доступные артефакты:")
                for i, artifact in enumerate(self.player.artifacts, 1):
                    print(f"{i}. {artifact}")
                print(f"{len(self.player.artifacts) + 1}. Отмена")

                art_choice = get_choice(1, len(self.player.artifacts) + 1)
                if art_choice <= len(self.player.artifacts):
                    artifact = self.player.artifacts[art_choice - 1]
                    result = self.use_artifact(artifact)
                    if result == "dodge":
                        # Пропускаем следующую атаку врага
                        print("Вы успешно уклонились от следующей атаки!")
                        # Пропускаем ход врага
                        return
                else:
                    print("Отменено.")
                    self.player_turn()
            else:
                print("У вас нет артефактов!")
                self.player_turn()

    def use_artifact(self, artifact_name):
        """Использование артефакта"""
        from config import ARTIFACTS

        if artifact_name not in ARTIFACTS:
            print("Артефакт не найден!")
            return None

        effects = {
            "Меч Посейдона": {"damage_mult": 2.0, "message": "Меч Посейдона светится синим светом!"},
            "Щит Тритона": {"defense_boost": 30, "message": "Щит Тритона создаёт защитный барьер!"},
            "Компас судьбы": {"heal": 50, "message": "Компас судьбы исцеляет ваши раны!"},
            "Кристалл глубины": {"damage": 40, "message": "Кристалл глубины выпускает сокрушительный луч!"},
            "Накидка тумана": {"dodge": True, "message": "Накидка тумана делает вас невидимым!"}
        }

        if artifact_name in effects:
            effect = effects[artifact_name]
            print(effect["message"])

            if "damage_mult" in effect:
                damage = self.player.damage * effect["damage_mult"]
                actual_damage = self.enemy.take_damage(damage)
                print(f"Вы нанесли {actual_damage} урона!")
                return "damage"

            elif "defense_boost" in effect:
                self.player.defense += effect["defense_boost"]
                print(f"Защита увеличена на {effect['defense_boost']} на 3 хода!")
                # Временный эффект защиты
                return "defense"

            elif "heal" in effect:
                healed = self.player.heal(effect["heal"])
                if healed > 0:
                    print(f"Вы исцелились на {healed} HP!")
                return "heal"

            elif "damage" in effect:
                actual_damage = self.enemy.take_damage(effect["damage"])
                print(f"Вы нанесли {actual_damage} урона!")
                return "damage"

            elif "dodge" in effect:
                return "dodge"

        return None

    def enemy_turn(self):
        """Ход врага"""
        print(f"\n--- Ход {self.enemy.name} ---")

        if hasattr(self.enemy, 'attack') and callable(self.enemy.attack):
            attack_result = self.enemy.attack()

            if isinstance(attack_result, dict):
                # Особые атаки босса
                if attack_result["type"] == "whirlpool":
                    damage = attack_result["damage"]
                    print(f"{self.enemy.name} использует {attack_result['name']}!")
                    actual_damage = self.player.take_damage(damage)
                    print(f"Вы получаете {actual_damage} урона от водоворота!")

                elif attack_result["type"] == "song":
                    damage = attack_result["damage"]
                    print(f"{self.enemy.name} использует {attack_result['name']}!")
                    actual_damage = self.player.take_damage(damage)
                    print(f"Вы получаете {actual_damage} урона и чувствуете замешательство!")
                    # Эффект замешательства (шанс промаха в следующем ходу)
                    if random.random() < 0.3:
                        print("Вы сбиты с толку и можете промахнуться в следующем ходу!")

                elif attack_result["type"] == "tentacles":
                    damage = attack_result["damage"]
                    print(f"{self.enemy.name} использует {attack_result['name']}!")
                    actual_damage = self.player.take_damage(damage)
                    print(f"Щупальца наносят {actual_damage} урона!")
                else:
                    # Обычная атака из словаря
                    damage = attack_result.get("damage", self.enemy.damage)
                    actual_damage = self.player.take_damage(damage)
                    print(f"{self.enemy.name} атакует и наносит {actual_damage} урона!")

            else:
                # Обычная атака (число)
                damage = attack_result
                actual_damage = self.player.take_damage(damage)
                print(f"{self.enemy.name} атакует и наносит {actual_damage} урона!")

    def check_victory(self):
        """Проверка победы"""
        if self.player.is_alive():
            print(f"\n🎉 ПОБЕДА! {self.enemy.name} повержен!")
            return True
        else:
            print(f"\n💀 ПОРАЖЕНИЕ! {self.player.name} пал в бою...")
            return False