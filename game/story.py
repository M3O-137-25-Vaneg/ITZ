"""
Управление сюжетом и диалогами
"""

from utils.helpers import print_header, get_choice, print_menu

class StoryManager:
    """Менеджер сюжета игры"""

    def __init__(self):
        self.current_chapter = 1
        self.decisions = []
        self.branches = {}
        self.initialize_story_branches()

    def initialize_story_branches(self):
        """Инициализация сюжетных ветвей"""

        # Глава 1: Пробуждение
        self.branches["chapter1"] = {
            "meet_morvanna": self.chapter1_meet_morvanna,
        }

        # Глава 2: Первый кристалл
        self.branches["chapter2"] = {
            "scientist_path": self.chapter2_scientist,
            "tyrant_path": self.chapter2_tyrant,
            "conservator_path": self.chapter2_conservator
        }

        # Глава 3: Второй кристалл
        self.branches["chapter3"] = {
            "choose_second_target": self.chapter3_choose_target,
        }

        # Глава 4: Третий кристалл
        self.branches["chapter4"] = {
            "morvanna_revelation": self.chapter4_morvanna_truth
        }

        # Глава 5: Финальная битва
        self.branches["chapter5"] = {
            "final_choice": self.chapter5_final_choice,
        }

    def play_chapter(self, chapter_num, player):
        """Проигрывание главы"""
        if chapter_num == 1:
            return self.play_chapter1(player)
        elif chapter_num == 2:
            return self.play_chapter2(player)
        elif chapter_num == 3:
            return self.play_chapter3(player)
        elif chapter_num == 4:
            return self.play_chapter4(player)
        elif chapter_num == 5:
            return self.play_chapter5(player)
        return True

    def play_chapter1(self, player):
        """Глава 1: Пробуждение"""
        print_header("ГЛАВА 1: ПРОБУЖДЕНИЕ НА РИФЕ")

        print("Вы открываете глаза. Вокруг - обломки вашего корабля 'Морской Призрак'.")
        print("Голова раскалывается от боли, но выжить - уже победа.")
        print("Память возвращается обрывками: шторм, странный свет, крики команды...")

        print("\nЧто вы делаете?")
        options = [
            "Осмотреть ближайшие обломки",
            "Позвать на помощь",
            "Попытаться вспомнить, что произошло",
            "Направиться вглубь острова"
        ]

        print_menu(options)
        choice = get_choice(1, 4)
        self.decisions.append(("chapter1_initial", choice))

        if choice == 1:
            print("\nСреди обломков вы находите ящик с припасами.")
            player.heal(20)
        elif choice == 2:
            print("\nВаш крик эхом разносится по пляжу. Ответа нет.")
        elif choice == 3:
            print("\nВспоминается лицо предателя-офицера... и странная песня.")
            player.update_morvanna_trust(5)
        elif choice == 4:
            print("\nВы идёте по берегу, замечая странные следы.")

        # Встреча с Морванной
        self.chapter1_meet_morvanna(player)
        return True

    def chapter1_meet_morvanna(self, player):
        """Встреча с Морванной"""
        print("\n\nСреди пальм вы замечаете фигуру. Это женщина в синих одеждах.")
        print("Она смотрит на вас без страха, скорее с интересом.")
        print("Морванна: 'Ты продержался дольше большинства. Песнь выбрала тебя.'")

        print("\nВаш ответ:")
        options = [
            "Что за Песнь? И кто ты?",
            "Как отсюда выбраться?",
            "Где моя команда?",
            "Молча осмотреть женщину"
        ]

        print_menu(options)
        choice = get_choice(1, 4)
        self.decisions.append(("chapter1_morvanna_response", choice))

        if choice == 1:
            print("Морванна: 'Песнь Бездны... древняя сила этого места. Я её хранитель.'")
            player.update_morvanna_trust(10)
        elif choice == 2:
            print("Морванна: 'Нужны три Хоральных Кристалла. Они у пиратских лидеров.'")
        elif choice == 3:
            print("Морванна: 'Мертвы или безумны. Песнь не щадит слабых.'")
            player.update_morality(-5)
        elif choice == 4:
            print("Морванна улыбается: 'Осторожный. Это умно в этом месте.'")
            player.update_morvanna_trust(5)

        print("\nМорванна: 'Выбирай, капитан. Поможешь мне собрать кристаллы?'")
        print_menu(["Согласиться", "Отказаться", "Потребовать объяснений"])

        choice = get_choice(1, 3)
        if choice == 1:
            print("Морванна: 'Хорошо. Начнём с поиска корабля в бухте.'")
            player.update_morvanna_trust(15)
        elif choice == 2:
            print("Морванна: 'Как знаешь. Но без меня ты не выживешь здесь.'")
            player.update_morvanna_trust(-10)
        elif choice == 3:
            print("Морванна рассказывает о трёх лидерах и их целях...")
            player.update_morvanna_trust(5)

        print("\nГлава завершена. Вы готовы к приключению!")
        return True

    def play_chapter2(self, player):
        """Глава 2: Первый кристалл"""
        print_header("ГЛАВА 2: ВЫБОР ПУТИ")

        print("Собрав команду из выживших, вы стоите перед выбором:")
        print("У какого из трёх пиратских лидеров забрать первый кристалл?")

        print("\nВаши варианты:")
        options = [
            "Учёный - изучает Песнь в своей лаборатории",
            "Тиран - правит крепостью на скалах",
            "Консерватор - скрывается в древнем храме",
            "Искать другой способ"
        ]

        print_menu(options)
        choice = get_choice(1, 4)
        self.decisions.append(("chapter2_first_crystal", choice))

        if choice == 1:
            result = self.chapter2_scientist(player)
        elif choice == 2:
            result = self.chapter2_tyrant(player)
        elif choice == 3:
            result = self.chapter2_conservator(player)
        else:
            print("Вы решаете сначала разведать ситуацию...")
            player.update_morality(5)
            result = "explore"

        # Проверяем результат
        if result in ["crystal_obtained", "negotiation", "test", "retreat", "explore"]:
            print("\nГлава 2 завершена!")
            return True
        elif result == "failed":
            print("\nВы не смогли получить кристалл. Попробуйте ещё раз.")
            return False
        else:
            return True

    def chapter2_scientist(self, player):
        """Ветка Учёного"""
        print_header("ЛАБОРАТОРИЯ УЧЁНОГО")

        print("Лаборатория поражает сочетанием древних артефактов и современных приборов.")
        print("Учёный: 'А, новый субъект! Поможешь с экспериментом?'")

        print("\nОн предлагает:")
        options = [
            "Согласиться на эксперимент",
            "Потребовать кристалл",
            "Атаковать",
            "Предложить сотрудничество"
        ]

        print_menu(options)
        choice = get_choice(1, 4)

        if choice == 1:
            print("\nЭксперимент даёт вам новые знания, но отнимает часть души...")
            player.update_morality(-15)
            player.damage += 10
            print("Получено: +10 к урону")
            if "Меч Посейдона" not in player.artifacts:
                player.equip_artifact("Меч Посейдона")
            return "crystal_obtained"
        elif choice == 2:
            print("\nУчёный смеётся: 'Сначала докажи, что выдержишь силу!'")
            # Битва с учёным
            from game.boss import PirateLord
            from game.battle import BattleSystem
            scientist = PirateLord("scientist")
            battle = BattleSystem(player, scientist)
            if battle.start_battle():
                print("\nУчёный повержен! Вы получаете кристалл.")
                player.update_morality(-10)
                if "Меч Посейдона" not in player.artifacts:
                    player.equip_artifact("Меч Посейдона")
                return "crystal_obtained"
            else:
                print("\nВы проиграли битву...")
                player.hp = max(1, player.max_hp // 2)
                return "failed"
        elif choice == 3:
            player.update_morality(-10)
            print("\nВы атакуете Учёного!")
            # Битва с учёным
            from game.boss import PirateLord
            from game.battle import BattleSystem
            scientist = PirateLord("scientist")
            battle = BattleSystem(player, scientist)
            if battle.start_battle():
                print("\nУчёный повержен! Вы получаете кристалл.")
                if "Меч Посейдона" not in player.artifacts:
                    player.equip_artifact("Меч Посейдона")
                return "crystal_obtained"
            else:
                print("\nВы проиграли битву...")
                player.hp = max(1, player.max_hp // 2)
                return "failed"
        elif choice == 4:
            print("\nУчёный заинтересован: 'Что ты предлагаешь?'")
            player.update_morvanna_trust(-5)

            if player.morality < 40:
                print("Учёный: 'Ты амбициозен... Мне это нравится. Возьми кристалл.'")
                if "Меч Посейдона" not in player.artifacts:
                    player.equip_artifact("Меч Посейдона")
                return "negotiation"
            else:
                print("Учёный: 'Ты слишком мягок для таких дел. Уходи.'")
                return "failed"

        return True

    def chapter2_tyrant(self, player):
        """Ветка Тирана"""
        print_header("КРЕПОСТЬ ТИРАНА")

        print("Крепость возвышается на скалах. Стражники смотрят на вас с подозрением.")
        print("Тиран: 'Мало кто решается прийти ко мне без приглашения. Зачем пожаловал?'")

        options = [
            "Требовать кристалл",
            "Предложить союз против других лидеров",
            "Попытаться проникнуть тайно",
            "Уйти"
        ]

        print_menu(options)
        choice = get_choice(1, 4)

        if choice == 1:
            print("\nТиран смеётся: 'Ха! Смелый. Но смелости мало. Докажи силу!'")
            # Битва с тираном
            from game.boss import PirateLord
            from game.battle import BattleSystem
            tyrant = PirateLord("tyrant")
            battle = BattleSystem(player, tyrant)
            if battle.start_battle():
                print("\nТиран повержен! Вы получаете кристалл.")
                player.update_morality(-5)
                if "Накидка тумана" not in player.artifacts:
                    player.equip_artifact("Накидка тумана")
                return "crystal_obtained"
            else:
                print("\nВы проиграли битву...")
                player.hp = max(1, player.max_hp // 2)
                return "failed"
        elif choice == 2:
            print("\nТиран задумывается: 'Интересное предложение... Но чем ты полезен?'")
            player.update_morality(-10)
            # Проверка силы игрока
            if player.damage > 25:
                print("Тиран: 'Достаточно силён. Беру тебя в союзники.'")
                if "Накидка тумана" not in player.artifacts:
                    player.equip_artifact("Накидка тумана")
                return "crystal_obtained"
            else:
                print("Тиран: 'Слабоват. Докажи свою силу в бою!'")
                from game.boss import PirateLord
                from game.battle import BattleSystem
                tyrant = PirateLord("tyrant")
                battle = BattleSystem(player, tyrant)
                if battle.start_battle():
                    print("\nТиран повержен! Вы получаете кристалл.")
                    if "Накидка тумана" not in player.artifacts:
                        player.equip_artifact("Накидка тумана")
                    return "crystal_obtained"
                else:
                    print("\nВы проиграли битву...")
                    player.hp = max(1, player.max_hp // 2)
                    return "failed"
        elif choice == 3:
            print("\nПопытка проникнуть тайно проваливается! Вас окружают стражники.")
            player.take_damage(30)
            player.update_morality(-15)
            return "failed"
        elif choice == 4:
            print("\nВы отступаете, чтобы придумать новый план.")
            return "retreat"

        return True

    def chapter2_conservator(self, player):
        """Ветка Консерватора"""
        print_header("УБЕЖИЩЕ КОНСЕРВАТОРА")

        print("Древний храм скрыт в глубине пещер. Внутри царит тишина и покой.")
        print("Консерватор: 'Ты пришёл за кристаллом? Знаешь ли ты, какую опасность он несёт?'")

        options = [
            "Убедить, что вы достойны",
            "Попытаться украсть кристалл",
            "Спросить о природе кристаллов",
            "Атаковать"
        ]

        print_menu(options)
        choice = get_choice(1, 4)

        if choice == 1:
            print("\nКонсерватор: 'Докажи это. Пройди испытание мудрости.'")
            # Испытание морали
            if player.morality >= 60:
                print("Консерватор: 'Твоё сердце чисто. Возьми кристалл, но используй мудро.'")
                player.update_morality(10)
                if "Щит Тритона" not in player.artifacts:
                    player.equip_artifact("Щит Тритона")
                return "crystal_obtained"
            else:
                print("Консерватор: 'Ты ещё не готов. Вернись, когда поймёшь истинную ценность силы.'")
                return "failed"
        elif choice == 2:
            print("\nКонсерватор: 'Вор! Ты не лучше других!'")
            player.update_morality(-20)
            # Битва с консерватором
            from game.boss import PirateLord
            from game.battle import BattleSystem
            conservator = PirateLord("conservator")
            battle = BattleSystem(player, conservator)
            if battle.start_battle():
                print("\nКонсерватор повержен! Вы получаете кристалл.")
                if "Щит Тритона" not in player.artifacts:
                    player.equip_artifact("Щит Тритона")
                return "crystal_obtained"
            else:
                print("\nВы проиграли битву...")
                player.hp = max(1, player.max_hp // 2)
                return "failed"
        elif choice == 3:
            print("\nКонсерватор рассказывает об истории кристаллов и опасности их использования...")
            player.update_morality(10)
            player.update_morvanna_trust(5)
            print("Консерватор: 'Вижу, ты ищешь знания, а не только силу. Возьми кристалл.'")
            if "Щит Тритона" not in player.artifacts:
                player.equip_artifact("Щит Тритона")
            return "crystal_obtained"
        elif choice == 4:
            print("\nКонсерватор с грустью: 'Насилие... всегда насилие.'")
            player.update_morality(-25)
            # Битва с консерватором
            from game.boss import PirateLord
            from game.battle import BattleSystem
            conservator = PirateLord("conservator")
            battle = BattleSystem(player, conservator)
            if battle.start_battle():
                print("\nКонсерватор повержен! Вы получаете кристалл.")
                if "Щит Тритона" not in player.artifacts:
                    player.equip_artifact("Щит Тритона")
                return "crystal_obtained"
            else:
                print("\nВы проиграли битву...")
                player.hp = max(1, player.max_hp // 2)
                return "failed"

        return True

    def play_chapter3(self, player):
        """Глава 3: Второй кристалл и союзы"""
        print_header("ГЛАВА 3: СОЮЗЫ И ПРЕДАТЕЛЬСТВА")

        print("С первым кристаллом в руках вы понимаете, что остальные лидеры теперь в курсе.")
        print("Морванна: 'Они объединятся против нас. Нужно действовать быстро.'")

        print("\nКакой подход выбрать?")
        options = [
            "Напасть первым на самого слабого",
            "Попытаться расколоть их союз",
            "Искать другие пути получить кристаллы",
            "Устроить засаду"
        ]

        print_menu(options)
        choice = get_choice(1, 4)
        self.decisions.append(("chapter3_approach", choice))

        if choice == 1:
            print("\nВы решаете атаковать первыми...")
            player.update_morality(-10)
            player.update_crew_loyalty(5)
            # Битва с оставшимися лидерами
            print("Вы сражаетесь с двумя оставшимися лидерами...")
            from game.boss import PirateLord
            from game.battle import BattleSystem

            # Создаём двух лордов
            import random
            lord_types = ["scientist", "tyrant", "conservator"]
            # Убираем тип уже побеждённого лорда (определим по артефактам)
            if "Меч Посейдона" in player.artifacts:
                lord_types.remove("scientist")
            elif "Накидка тумана" in player.artifacts:
                lord_types.remove("tyrant")
            elif "Щит Тритона" in player.artifacts:
                lord_types.remove("conservator")

            if len(lord_types) >= 2:
                enemy1 = PirateLord(lord_types[0])
                enemy2 = PirateLord(lord_types[1])

                print(f"\nВы сражаетесь с {enemy1.name} и {enemy2.name}!")
                input("Нажмите Enter чтобы начать битву...")

                # Упрощённая битва - бьём по очереди
                for enemy in [enemy1, enemy2]:
                    battle = BattleSystem(player, enemy)
                    if not battle.start_battle():
                        print("Вы проиграли битву...")
                        player.hp = max(1, player.hp // 2)
                        break

                if player.is_alive():
                    print("\nВы побеждаете! Получаете второй кристалл.")
                    player.equip_artifact("Кристалл глубины")
                    return True
                else:
                    return True
            else:
                print("Все лидеры уже побеждены? Что-то пошло не так...")
                player.equip_artifact("Кристалл глубины")
                return True

        elif choice == 2:
            print("\nВы пытаетесь расколоть их союз переговорами...")
            player.update_morality(5)
            if player.morality > 50:
                print("Переговоры успешны! Вы получаете кристалл без боя.")
                player.equip_artifact("Кристалл глубины")
            else:
                print("Переговоры проваливаются. Приходится сражаться.")
                from game.boss import PirateLord
                from game.battle import BattleSystem

                # Определяем противника
                lord_type = "tyrant" if "scientist" in player.artifacts else "scientist"
                enemy = PirateLord(lord_type)
                battle = BattleSystem(player, enemy)

                if battle.start_battle():
                    print("Вы побеждаете в бою! Получаете второй кристалл.")
                    player.equip_artifact("Кристалл глубины")
                else:
                    print("Вы проигрываете... но спасаетесь.")
                    player.hp = max(1, player.hp // 2)
        elif choice == 3:
            print("\nВы ищете альтернативные пути...")
            player.update_morality(10)
            print("Вы находите тайник с кристаллом в древних руинах.")
            player.equip_artifact("Кристалл глубины")
        elif choice == 4:
            print("\nВы готовите засаду...")
            player.update_morality(-15)
            player.update_crew_loyalty(10)
            print("Засада удалась! Вы захватываете кристалл.")
            player.equip_artifact("Кристалл глубины")

        print("\nГлава 3 завершена!")
        return True

    def play_chapter4(self, player):
        """Глава 4: Третий кристалл и правда"""
        print_header("ГЛАВА 4: ПРАВДА О МОРВАННЕ")

        print("С двумя кристаллами энергия на острове становится нестабильной.")
        print("Странные видения посещают вас по ночам...")

        print("\nМорванна ведёт вас в самое сердце острова.")
        print("Морванна: 'Пришло время узнать правду. Я не совсем та, за кого себя выдаю...'")

        options = [
            "Выслушать её",
            "Потребовать объяснений немедленно",
            "Быть настороже",
            "Отказаться слушать"
        ]

        print_menu(options)
        choice = get_choice(1, 4)
        self.decisions.append(("chapter4_morvanna_truth", choice))

        if choice == 1:
            print("\nМорванна: 'Я - дочь Песни Бездны. Моего отца заточили здесь давно...'")
            print("'Кристаллы - ключи к его тюрьме. Что мы сделаем с ними?'")
            player.update_morvanna_trust(20)
        elif choice == 2:
            print("\nМорванна вздыхает: 'Хорошо. Я - часть той силы, что держит корабли здесь.'")
            print("'Мой отец - сама Песнь Бездны. Кристаллы могут его освободить... или уничтожить.'")
            player.update_morvanna_trust(5)
        elif choice == 3:
            print("\nМорванна: 'Не бойся. Если бы я хотела тебе зла, сделала бы это давно.'")
            print("'Я - дух этого моря в человеческом облике.'")
            player.update_morvanna_trust(10)
        elif choice == 4:
            print("\nМорванна с грустью: 'Как знаешь. Но правда всё равно откроется.'")
            player.update_morvanna_trust(-10)

        print("\nВы находите третий кристалл в сердце острова.")
        if "Компас судьбы" not in player.artifacts:
            player.equip_artifact("Компас судьбы")

        print("\nГлава 4 завершена!")
        return True

    def play_chapter5(self, player):
        """Глава 5: Финальный выбор"""
        print_header("ГЛАВА 5: ПЕСНЬ БЕЗДНЫ")

        print("Все три кристалла в ваших руках. Они пульсируют единым ритмом.")
        print("Песнь Бездны звучит всё громче, призывая к решению.")

        print("\nМорванна стоит перед вами, её глаза светятся древней силой.")
        print("Морванна: 'Время пришло. Выбери судьбу моего отца... и мою.'")

        final_options = [
            "Освободить Песнь (уничтожить кристаллы)",
            "Подчинить Песнь (использовать кристаллы для контроля)",
            "Объединиться с Песнью (стать её частью)",
            "Найти баланс (запечатать, но не уничтожать)"
        ]

        print_menu(final_options)
        choice = get_choice(1, 4)
        self.decisions.append(("chapter5_final_choice", choice))

        player.choose_path(choice)

        # Финальная битва или решение
        if choice == 2 or choice == 3:  # Для контроля или объединения нужна битва
            print("\nПеснь Бездны сопротивляется! Нужно доказать свою силу!")
            from game.boss import Boss
            from game.battle import BattleSystem
            boss = Boss()
            battle = BattleSystem(player, boss)
            if not battle.start_battle():
                print("\nВы не смогли одолеть Песнь Бездны...")
                player.hp = max(1, player.hp // 2)
                choice = 4  # По умолчанию - баланс

        # Показ концовки
        self.show_ending(player, choice)

        return True

    def show_ending(self, player, choice):
        """Показ концовки"""
        print_header("КОНЕЦ ИСТОРИИ")

        if choice == 1:  # Освобождение
            print("Вы разбиваете кристаллы. Громкий крик эхом разносится по острову.")
            print("Песнь Бездны освобождается, но вместо разрушения приносит покой.")
            print("Морванна улыбается сквозь слёзы: 'Спасибо. Он свободен.'")
            print("\nОстров постепенно исчезает. Вы и ваша команда уплываете на свободу.")
            print("Море становится спокойным, но магия уходит из него навсегда.")
            print("Вы возвращаетесь к нормальной жизни, но иногда слышите эхо той Песни...")

        elif choice == 2:  # Контроль
            print("Вы используете кристаллы, чтобы подчинить Песнь своей воле.")
            print("Сила затопляет вас, даруя невероятные способности.")
            print("Морванна смотрит с печалью: 'Ты стал тем, с кем боролся.'")
            print("\nТеперь вы Повелитель Глубин. Корабли повинуются вашему слову.")
            print("Но с каждым днём вы всё больше теряете свою человечность.")
            print("Море темнеет, становясь продолжением вашей воли...")

        elif choice == 3:  # Объединение
            print("Вы предлагаете Песни союз. Кристаллы сливаются с вашим телом.")
            print("Морванна обнимает вас: 'Мы будем вместе. Навсегда.'")
            print("\nВы и Морванна становитесь хранителями моря.")
            print("Ваш корабль теперь может плавать между мирами.")
            print("Вы вечные странники, поддерживающие баланс в океанах...")

        elif choice == 4:  # Баланс
            print("Вы находите способ запечатать Песнь, но не уничтожать её.")
            print("Морванна кивает: 'Мудрое решение. Сила должна быть, но под контролем.'")
            print("\nКристаллы превращаются в амулеты для вас и Морванны.")
            print("Вы становитесь Хранителем Равновесия.")
            print("Ваша задача - следить, чтобы ни одна сторона не стала слишком сильной.")
            print("Море остаётся живым, опасным, но справедливым...")

        print(f"\nВаша итоговая мораль: {player.morality}/100")
        print(f"Лояльность команды: {player.crew_loyalty}/100")
        print(f"Доверие Морванны: {player.morvanna_trust}/100")

        print("\n=== ИГРА ЗАВЕРШЕНА ===")

    def get_story_progress(self):
        """Получение прогресса сюжета"""
        return {
            "chapter": self.current_chapter,
            "decisions": self.decisions,
            "branches_unlocked": list(self.branches.keys())
        }

    # Методы для словаря branches
    def chapter3_choose_target(self, player):
        """Выбор цели для атаки во 2 главе"""
        return self.play_chapter3(player)

    def chapter4_morvanna_truth(self, player):
        """Правда о Морванне"""
        return self.play_chapter4(player)

    def chapter5_final_choice(self, player):
        """Финальный выбор"""
        return self.play_chapter5(player)