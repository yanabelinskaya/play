import json
import csv
import random
import sys
import os

game_data = {
    "player_name": "",
    "player_health": 5,
    "player_power": 10,
    "player_defense": 5,
    "treasure_count": 0,
    "victory_goal": 3,
    "attack_locations": ["лес", "поляна", "пещера"],
    "enemies": [
        {
            "name": "Злой орк",
            "health": 8,
            "power": 4,
            "defense": 3
        },
        {
            "name": "Лютый волк",
            "health": 6,
            "power": 5,
            "defense": 2
        },
        {
            "name": "Гигантский паук",
            "health": 10,
            "power": 3,
            "defense": 5
        },
    ],
    "attack_location_chosen": False,
    "player_defense_boost": 0,
    "player_defense_active": False,
}

def start_new_game():
    global game_data
    game_data["player_name"] = input("Введите ваше имя: ")
    game_data["treasure_count"] = 0
    game_data["victory_goal"] = 3
    game_data["attack_location_chosen"] = False
    game_data["player_defense_boost"] = 0
    game_data["player_defense_active"] = False

    print(f"{game_data['player_name']}, вы оказались в мистическом месте, известном своими опасностями и тайнами.")

    hero_choice = input("Выберите вашего героя (1 - Воин, 2 - Маг, 3 - Разбойник): ")
    if hero_choice == "1":
        game_data["player_power"] = 10
        game_data["player_defense"] = 7
        print("Вы - воин! Вы обладаете высокой силой и защитой.")
    elif hero_choice == "2":
        game_data["player_power"] = 6
        game_data["player_defense"] = 3
        print("Вы - маг! Вы обладаете магическими способностями и средней защитой.")
    elif hero_choice == "3":
        game_data["player_power"] = 8
        game_data["player_defense"] = 5
        print("Вы - разбойник! Вы ловки и умел в обороне.")
    else:
        print("Выбор неверен, вы стали воином по умолчанию.")

    if not game_data["attack_location_chosen"]:
        print("Выберите место для битвы:")
        for i, location in enumerate(game_data["attack_locations"], 1):
            print(f"{i}. {location}")

        location_choice = int(input("Введите номер места: ")) - 1
        if location_choice >= 0 and location_choice < len(game_data["attack_locations"]):
            battle_location = game_data["attack_locations"][location_choice]
            game_data["attack_location_chosen"] = True
        else:
            print("Неправильный выбор. Вы упускаете ход.")
            return

    print("Выберите врага для битвы:")
    for i, enemy in enumerate(game_data["enemies"], 1):
        if isinstance(enemy, dict):
            print(f"{i}. {enemy['name']}")
    enemy_choice = int(input("Введите номер врага: ")) - 1
    chosen_enemy = game_data["enemies"][enemy_choice]

    game_data["enemy_name"] = chosen_enemy["name"]
    game_data["enemy_health"] = chosen_enemy["health"]
    game_data["enemy_power"] = chosen_enemy["power"]
    game_data["enemy_defense"] = chosen_enemy["defense"]

    print(f"Вы начали битву с {game_data['enemy_name']} в месте {battle_location}")
    # Вызываем функцию для диалога
    dialog_with_enemy()

def dialog_with_enemy():
    dialog_options = {
        "1": "Атаковать ты мерзавец!",
        "2": "Может, мы мирно разойдемся"
    }

    print(f"{game_data['enemy_name']} говорит: 'Что ты здесь делаешь, незнакомец? Готов сразиться?'")
    print("Выберите ответ (1 - Атаковать, 2 - Мирно разойтись)")

    while True:
        choice = input("Введите номер ответа: ")
        if choice in dialog_options:
            response = dialog_options[choice]
            if choice == "1":
                print("Вы решили атаковать врага!")
                battle()
                break  # Завершаем цикл после битвы
            elif choice == "2":
                print("Вы решили попробовать договориться и мирно разойтись.")
                play_again = input("Вы мирно разошлись. Хотите начать новую игру? (да/нет): ").lower()
                if play_again == "да":
                    start_new_game()
                break  # Завершаем цикл после мирного разрешения
        else:
            print("Неправильный выбор. Попробуйте снова.")


def choose_attack_location():
    print("Выберите место для атаки:")
    for i, location in enumerate(game_data["attack_locations"], 1):
        print(f"{i}. {location}")
    
    choice = input("Введите номер места: ")
    if choice.isnumeric():
        choice = int(choice)
        if 1 <= choice <= len(game_data["attack_locations"]):
            return choice - 1  
    return random.randint(0, len(game_data["attack_locations"]) - 1)  

def random_event():
    events = ["Вы нашли сокровище!", "Враг внезапно атаковал вас!", "Вы нашли укрытие и восстановили здоровье."]
    event = random.choice(events)
    if event == "Вы нашли сокровище!":
        game_data["treasure_count"] += 1
    elif event == "Враг внезапно таковал вас!":
        game_data["enemy_health"] -= random.randint(10, 30)
    elif event == "Вы нашли укрытие и восстановили здоровье.":
        game_data["player_health"] += random.randint(10, 30)
        if game_data["player_health"] > 100:
            game_data["player_health"] = 100
    return event
def battle():
    player_health = game_data["player_health"]
    enemy_health = game_data["enemy_health"]

    # Выбор места атаки перед началом битвы
    attack_location_index = choose_attack_location()
    attack_location = game_data["attack_locations"][attack_location_index]

    print(f"Вы начали битву с {game_data['enemy_name']} в {attack_location}!")

    while player_health > 0 and enemy_health > 0:
        print(f"Здоровье {game_data['player_name']}: {player_health}, Здоровье врага ({game_data['enemy_name']}): {enemy_health}")
        choice = input("Что вы хотите сделать? (атаковать/защищаться/случайное событие): ").lower()

        if choice == "атаковать":
            player_attack = random.randint(1, game_data["player_power"] + 2)
            player_defense = game_data["player_defense"]
            enemy_attack = random.randint(1, game_data["enemy_power"])
            enemy_defense = random.randint(1, game_data["enemy_defense"])
            enemy_health -= max(0, player_attack - enemy_defense)
            print(f"Вы атаковали {game_data['enemy_name']} и нанесли {player_attack - enemy_defense} урона.")

            player_health -= max(0, enemy_attack - player_defense)

        elif choice == "защищаться":
            game_data["player_defense_active"] = True
            game_data["player_defense_boost"] = random.randint(1, 5)
            print("Вы усилили свою защиту.")
        elif choice == "случайное событие":
            event = random_event()
            print(event)
        else:
            print("Неправильный выбор. Вы упускаете ход.")
            continue

        if enemy_health <= 0:
            print(f"Вы победили {game_data['enemy_name']}!")
            game_data["treasure_count"] += 1  
            print(f"Вы получаете сокровище! Теперь у вас {game_data['treasure_count']} сокровищ.")
            break

        if player_health <= 0:
            print("Вас убили.")
            break

        if random.random() < 0.3:
            event = random_event()
            print(event)

    print(f"Битва с {game_data['enemy_name']} закончилась.")
    game_data["player_defense_active"] = False
    game_data["player_defense_boost"] = 0
    game_data["enemy_health"] = chosen_enemy["health"]  


while True:
    print("1. Начать новую игру")
    print("2. Продолжить игру")
    print("3. Удалить сохранение")
    print("4. Выйти из игры")
    choice = input("Выберите действие: ")

    if choice == "1":
        start_new_game()
        while game_data["treasure_count"] < game_data["victory_goal"]:
            dialog_with_enemy()
            if game_data["player_health"] <= 0:
                print("Вы проиграли. Возвращаемся в меню выбора...")
                break  
        if game_data["treasure_count"] >= game_data["victory_goal"]:
            print("Вы победили в этой кампании!")
        save_game_data()
        write_to_csv()
    elif choice == "2":
        try:
            with open("game_data.json", "r") as file:
                game_data = json.load(file)
            print(f"Продолжаем игру как {game_data['player_name']}")
            while game_data["treasure_count"] < game_data["victory_goal"]:
                dialog_with_enemy()
                if game_data["player_health"] <= 0:
                    print("Вы проиграли. Возвращаемся в меню выбора...")
                    break 
            if game_data["treasure_count"] >= game_data["victory_goal"]:
                print("Вы победили в этой кампании!")
            save_game_data()
            write_to_csv()
        except FileNotFoundError:
            print("Сохранение не найдено.")
    elif choice == "3":
        delete_saved_game()
    elif choice == "4":
        sys.exit()
