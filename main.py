import os

from game.clicker import MyClicker
from game.exceptions import NotEnoughMoney, TamagochiIsGone
from game.game import MyGame
from game.models import Food, Medicine
from game.tamagochi import MyTamagochi


def create_game() -> MyGame:
    """Создаёт игру с питомцем, товарами магазина лекарствами.

    :return: игра
    """
    all_food = [
        Food(name='Бургер', satiety=20, price=40),
        Food(name='Салат', satiety=10, price=20),
        Food(name='Яблоко', satiety=10, price=15)
    ]

    all_medicine = [
        Medicine(
            name='Ибупрофен',
            price=30,
            heal_hp=20,
            number_of_uses=2,
        )
    ]

    return MyGame(
        MyTamagochi(0, 0, 100, 100),
        MyClicker(10, 20),
        all_food=all_food,
        all_medicine=all_medicine,
    )


def show_menu(game: MyGame) -> None:
    """Показывает состояние питомца и доступные действия.

    :param game: текущая игра
    """
    status = game.get_status()
    print(f"Сумка с едой: {game.food}")
    print(f"Сумка с лекарствами: {game.medicine}")
    print(
        f"\nСтатус: голод {status['hunger']}, "
        f"усталость {status['tiredness']}, "
        f"здоровье {status['hp']}, энергия {status['energy']}, "
        f"монет {status['coins']}\n"
    )
    if game.tamagochi.is_sick():
        print("=======Тамагочи болеет======")
        print("=======Отдых действует менее эффективно=======")

    print("1. Пойти на работу")
    print("2. Купить еду")
    print("3. Купить лекарство")
    print("4. Покормить")
    print("5. Вылечить")
    print("6. Играть")
    print("7. Отдых")
    print("0. Выход")


def perform_action(game: MyGame, command: str) -> str:
    """Применяет к игре команду пользователя.

    :param game: текущая игра
    :param command: команда
    """
    match command:
        case '1':
            income = game.work()
            game.tamagochi.update()
            return f'Вы заработали {income} монет'
        case '2':
            game.buy_food()
        case '3':
            game.buy_medicine()
        case '4':
            game.feed_tamagochi()
        case '5':
            game.heal_tamagochi()
        case '6':
            game.play_with_tamagochi()
            return 'Вы поиграли с питомцем'
        case '7':
            game.rest_tamagochi()
            return 'Питомец отдохнул'
        case _:
            return 'Неверная команда'

    return ''


def main() -> None:
    """Запускает консольный игровой цикл."""
    game = create_game()
    print("Добро пожаловать в Тамагочи-кликер!")
    output = ""

    while True:
        print(output)
        show_menu(game)
        command = input("Выберите действие: ")
        if command == "0":
            break

        try:
            output = perform_action(game, command)
        except NotEnoughMoney as error:
            output = str(error)
        except TamagochiIsGone:
            print("Питомец умер. Игра окончена.")
            break

        os.system('clear')


if __name__ == "__main__":
    main()
