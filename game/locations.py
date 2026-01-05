"""
Локации и их описание
"""

from utils.helpers import print_header, get_choice, print_menu

class Location:
    """Базовый класс локации"""

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.visited = False
        self.events = []
        self.artifacts = []
        self.enemies = []

    def visit(self, player):
        """Посещение локации"""
        print_header(self.name)
        print(self.description)
        self.visited = True
        return self.handle_events(player)

    def handle_events(self, player):
        """Обработка событий локации"""
        if self.events:
            print("\nСобытия:")
            for event in self.events:
                event(player)
        return True


class GameLocations:
    """Управление всеми локациями игры"""

    def __init__(self):
        self.locations = {}
        self.current_location = None
        self.initialize_locations()

    def initialize_locations(self):
        """Инициализация всех локаций"""

        # Начальная локация
        shore = Location(
            "Берег Блуждающего Рифа",
            "Вы очнулись на песчаном берегу. Вокруг разбросаны обломки кораблей разных эпох. "
            "Воздух пропитан солью и тайной. Вдали виднеются джунгли и горы."
        )
        shore.events.append(self.event_find_survivor)
        self.locations["shore"] = shore

        # Джунгли
        jungle = Location(
            "Густые джунгли острова",
            "Плотная тропическая растительность скрывает древние руины. "
            "Слышны странные звуки, не похожие на обычных животных."
        )
        jungle.events.append(self.event_ancient_ruins)
        jungle.artifacts.append("Компас судьбы")
        self.locations["jungle"] = jungle

        # Пиратская бухта
        bay = Location(
            "Пиратская бухта",
            "Скрытая бухта, служащая пристанищем для пиратов всех мастей. "
            "Здесь можно найти информацию, нанять команду или попасть в неприятности."
        )
        bay.events.append(self.event_pirate_tavern)
        self.locations["bay"] = bay

        # Храм Моря
        temple = Location(
            "Храм Забытого Моря",
            "Древний храм, построенный из кораллов и камня. "
            "Фрески изображают морское божество и три кристалла."
        )
        temple.events.append(self.event_temple_puzzle)
        temple.artifacts.append("Кристалл глубины")
        self.locations["temple"] = temple

        # Лаборатория Учёного
        lab = Location(
            "Лаборатория Учёного",
            "Современная лаборатория, контрастирующая с древностью острова. "
            "Приборы гудит, изучая энергию Песни Бездны."
        )
        lab.events.append(self.event_scientist_dialogue)
        self.locations["lab"] = lab

        # Крепость Тирана
        fortress = Location(
            "Крепость Морского Тирана",
            "Неприступная крепость на скалах. Стражники бдительно несут службу. "
            "Здесь правит страх и сила."
        )
        fortress.events.append(self.event_tyrant_challenge)
        self.locations["fortress"] = fortress

        # Убежище Консерватора
        sanctuary = Location(
            "Убежище Консерватора",
            "Тайное убежище в пещерах. Здесь хранятся знания и артефакты, "
            "которые Консерватор хочет защитить от мира."
        )
        sanctuary.events.append(self.event_conservator_test)
        sanctuary.artifacts.append("Щит Тритона")
        self.locations["sanctuary"] = sanctuary

        # Сердце Бездны
        abyss = Location(
            "Сердце Бездны",
            "Эпицентр аномалии. Вода здесь искрится странной энергией. "
            "Песнь Бездны звучит настолько громко, что сводит с ума."
        )
        abyss.events.append(self.event_final_confrontation)
        self.locations["abyss"] = abyss

    def event_find_survivor(self, player):
        """Событие: встреча с Морванной"""
        print("\nСреди обломков вы замечаете движение...")
        print("К вам приближается женщина в потрёпанной, но изысканной одежде.")
        print("Морванна: 'Ты тоже попал в ловушку Рифа? Я ищу способ остановить Песнь...'")

        responses = [
            "Кто ты такая?",
            "Что такое Песнь Бездны?",
            "Как отсюда выбраться?"
        ]

        print_menu(responses)
        choice = get_choice(1, 3)

        if choice == 1:
            print("Морванна: 'Я... выжившая. Из команды призрачного корабля.'")
            player.update_morvanna_trust(10)
        elif choice == 2:
            print("Морванна: 'Древняя сила, что заманивает корабли. Нужны Кристаллы Хорала.'")
            player.update_morvanna_trust(15)
        elif choice == 3:
            print("Морванна: 'Собери три кристалла. Они у пиратских лидеров.'")
            player.update_morvanna_trust(5)

    def event_ancient_ruins(self, player):
        """Событие: древние руины"""
        print("\nСреди руин вы находите древний артефакт!")
        if "Компас судьбы" not in player.artifacts:
            player.equip_artifact("Компас судьбы")
        else:
            print("Но у вас уже есть этот артефакт.")

    def event_pirate_tavern(self, player):
        """Событие: пиратский таверн"""
        print("\nВ таверне 'Пьяный кракен' кипит жизнь.")
        print("Вы можете:")

        options = [
            "Найти информацию о кристаллах (требуется лояльность > 30)",
            "Нанять новых членов команды",
            "Устроить драку",
            "Уйти"
        ]

        print_menu(options)
        choice = get_choice(1, 4)

        if choice == 1:
            if player.crew_loyalty > 30:
                print("Старый моряк рассказывает о трёх лидерах...")
                player.update_morality(5)
                player.update_morvanna_trust(5)
            else:
                print("Команда недостаточно лояльна для этого.")
        elif choice == 2:
            print("Вы нанимаете нескольких опытных моряков.")
            player.update_crew_loyalty(10)
            player.update_morality(5)
        elif choice == 3:
            print("Драка заканчивается плохо для всех...")
            player.take_damage(20)
            player.update_morality(-10)
            player.update_crew_loyalty(-5)
        elif choice == 4:
            print("Вы покидаете таверн.")

    def event_temple_puzzle(self, player):
        """Событие: головоломка храма"""
        print("\nПеред вами древняя головоломка с тремя символами.")
        print("Морванна: 'Это карта показывает расположение кристаллов...'")

        puzzle_answer = 2
        print("Сколько лидеров ищут кристаллы?")
        print_menu(["2", "3", "4", "5"])

        choice = get_choice(1, 4)
        if choice == puzzle_answer:
            print("Головоломка решена! Открывается тайник.")
            if "Кристалл глубины" not in player.artifacts:
                player.equip_artifact("Кристалл глубины")
            else:
                print("Но у вас уже есть этот артефакт.")
        else:
            print("Головоломка не решена. Нужно больше информации.")
            player.update_morvanna_trust(-5)

    def event_scientist_dialogue(self, player):
        """Событие: диалог с Учёным"""
        print("\nУчёный: 'А, новый подопытный! Хочешь помочь с исследованиями?'")

        options = [
            "Согласиться помочь",
            "Требовать кристалл",
            "Атаковать",
            "Уйти"
        ]

        print_menu(options)
        choice = get_choice(1, 4)

        if choice == 1:
            print("Учёный: 'Отлично! Возьми этот прибор.'")
            player.update_morality(-5)
            player.update_morvanna_trust(-10)
            player.damage += 5
            print("Вы получили +5 к урону от исследований.")
        elif choice == 2:
            print("Учёный: 'Кристалл? Докажи, что достоин его!'")
            # Здесь будет битва в story.py
        elif choice == 3:
            print("Учёный: 'Так сразу? Ну что ж...'")
            player.update_morality(-15)
            # Здесь будет битва в story.py
        elif choice == 4:
            print("Вы решаете уйти и вернуться позже.")

    def event_tyrant_challenge(self, player):
        """Событие: испытание Тирана"""
        print("\nТиран: 'Сильный... Но достаточно ли силён для кристалла?'")
        print("Он предлагает испытание:")

        options = [
            "Принять вызов на поединок",
            "Предложить союз",
            "Попытаться украсть кристалл",
            "Отказаться"
        ]

        print_menu(options)
        choice = get_choice(1, 4)

        if choice == 1:
            print("Тиран: 'Отлично! Покажи свою силу!'")
            player.update_morality(-5)
            player.update_crew_loyalty(10)
        elif choice == 2:
            print("Тиран: 'Союз? Интересно...'")
            player.update_morality(-20)
            player.update_morvanna_trust(-10)
        elif choice == 3:
            print("Попытка кражи обнаружена!")
            player.update_morality(-10)
            player.take_damage(15)
        elif choice == 4:
            print("Тиран: 'Слабак! Уходи!'")
            player.update_crew_loyalty(-5)

    def event_conservator_test(self, player):
        """Событие: испытание Консерватора"""
        print("\nКонсерватор: 'Кристаллы слишком опасны. Докажи, что не злоупотребишь силой.'")

        test_questions = [
            ("Что важнее: сила или мудрость?", ["Сила", "Мудрость", "Баланс"]),
            ("Спасёшь ли одного ценой многих?", ["Да", "Нет", "Зависит от ситуации"]),
            ("Уничтожить ли силу, если она опасна?", ["Да", "Нет", "Контролировать"])
        ]

        morality_score = 0
        for i, (question, answers) in enumerate(test_questions):
            print(f"\nВопрос {i+1}: {question}")
            print_menu(answers)
            choice = get_choice(1, 3)

            if i == 0:
                if choice == 3:
                    morality_score += 10
            elif i == 1:
                if choice == 2:
                    morality_score += 10
            elif i == 2:
                if choice == 3:
                    morality_score += 10

        if morality_score >= 20:
            print("Консерватор: 'Ты понимаешь суть. Возьми кристалл.'")
            if "Щит Тритона" not in player.artifacts:
                player.equip_artifact("Щит Тритона")
            player.update_morality(20)
            player.update_morvanna_trust(10)
        else:
            print("Консерватор: 'Ты не готов. Уходи.'")
            player.update_morality(-5)

    def event_final_confrontation(self, player):
        """Событие: финальная конфронтация"""
        print("\nМорванна: 'Пора сделать выбор, Элиас. Что мы сделаем с Песнью?'")
        print("Перед вами три кристалла пульсируют энергией.")

        final_options = [
            "Освободить силу (Путь Консерватора)",
            "Контролировать силу (Путь Учёного)",
            "Использовать силу (Путь Тирана)",
            "Найти баланс (Путь Симбиоза)"
        ]

        print_menu(final_options)
        choice = get_choice(1, 4)

        player.choose_path(choice)
        return choice

    def get_location(self, location_id):
        """Получение локации по ID"""
        return self.locations.get(location_id)

    def set_current_location(self, location_id):
        """Установка текущей локации"""
        self.current_location = self.locations.get(location_id)
        return self.current_location