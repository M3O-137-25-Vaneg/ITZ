"""
Класс игрока
"""

from config import PLAYER_HP, PLAYER_DAMAGE, PLAYER_DEFENSE, ARTIFACTS

class Player:
    """Класс игрока (Элиас Шоу)"""

    def __init__(self, name="Элиас Шоу"):
        self.name = name
        self.max_hp = PLAYER_HP
        self.hp = PLAYER_HP
        self.base_damage = PLAYER_DAMAGE
        self.base_defense = PLAYER_DEFENSE
        self.damage = PLAYER_DAMAGE
        self.defense = PLAYER_DEFENSE
        self.artifacts = []
        self.chosen_path = None
        self.morality = 50  # 0-100, где 50 - нейтрально
        self.crew_loyalty = 70  # 0-100
        self.morvanna_trust = 30  # 0-100

    def equip_artifact(self, artifact_name):
        """Экипировка артефакта"""
        if artifact_name in ARTIFACTS and artifact_name not in self.artifacts:
            self.artifacts.append(artifact_name)
            artifact = ARTIFACTS[artifact_name]
            self.damage += artifact.get("damage", 0)
            self.defense += artifact.get("defense", 0)
            print(f"Артефакт '{artifact_name}' экипирован!")
            return True
        elif artifact_name in self.artifacts:
            print(f"Артефакт '{artifact_name}' уже экипирован!")
            return False
        else:
            print(f"Артефакт '{artifact_name}' не найден!")
            return False

    def take_damage(self, damage):
        """Получение урона"""
        actual_damage = max(1, damage - self.defense // 2)
        self.hp -= actual_damage
        if self.hp < 0:
            self.hp = 0
        return actual_damage

    def heal(self, amount):
        """Лечение"""
        old_hp = self.hp
        self.hp = min(self.max_hp, self.hp + amount)
        healed = self.hp - old_hp
        if healed > 0:
            print(f"Вы исцелились на {healed} HP. Теперь у вас {self.hp}/{self.max_hp} HP.")
        return healed

    def is_alive(self):
        """Проверка, жив ли игрок"""
        return self.hp > 0

    def get_stats(self):
        """Получение статистики игрока"""
        return {
            "name": self.name,
            "hp": f"{self.hp}/{self.max_hp}",
            "damage": self.damage,
            "defense": self.defense,
            "artifacts": self.artifacts,
            "path": self.chosen_path,
            "morality": self.morality,
            "crew_loyalty": self.crew_loyalty,
            "morvanna_trust": self.morvanna_trust
        }

    def update_morality(self, change):
        """Изменение морали"""
        old_morality = self.morality
        self.morality = max(0, min(100, self.morality + change))
        if change != 0:
            direction = "увеличилась" if change > 0 else "уменьшилась"
            print(f"Ваша мораль {direction} на {abs(change)}. Теперь: {self.morality}/100")

    def update_crew_loyalty(self, change):
        """Изменение лояльности команды"""
        old_loyalty = self.crew_loyalty
        self.crew_loyalty = max(0, min(100, self.crew_loyalty + change))
        if change != 0:
            direction = "увеличилась" if change > 0 else "уменьшилась"
            print(f"Лояльность команды {direction} на {abs(change)}. Теперь: {self.crew_loyalty}/100")

    def update_morvanna_trust(self, change):
        """Изменение доверия Морванны"""
        old_trust = self.morvanna_trust
        self.morvanna_trust = max(0, min(100, self.morvanna_trust + change))
        if change != 0:
            direction = "увеличилось" if change > 0 else "уменьшилось"
            print(f"Доверие Морванны {direction} на {abs(change)}. Теперь: {self.morvanna_trust}/100")

    def choose_path(self, path):
        """Выбор пути развития"""
        self.chosen_path = path

        # Бонусы в зависимости от пути
        if path == 1:  # Учёный
            self.damage += 10
            self.morvanna_trust += 20
            print("Вы выбрали Путь Учёного: контроль над силой!")
            print("Получено: +10 к урону, +20 к доверию Морванны")
        elif path == 2:  # Консерватор
            self.defense += 15
            self.crew_loyalty += 20
            print("Вы выбрали Путь Консерватора: уничтожение силы!")
            print("Получено: +15 к защите, +20 к лояльности команды")
        elif path == 3:  # Тиран
            self.damage += 20
            self.morality -= 30
            print("Вы выбрали Путь Тирана: использование силы!")
            print("Получено: +20 к урону, -30 к морали")
        elif path == 4:  # Симбиоз
            self.hp += 50
            self.max_hp += 50
            self.morality += 20
            print("Вы выбрали Путь Симбиоза: поиск баланса!")
            print("Получено: +50 к максимальному здоровью, +20 к морали")