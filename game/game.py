"""Интерфейс и реализация класса игры."""

from abc import ABC, abstractmethod
from typing import Any

from .clicker import AbstractClicker
from .exceptions import NotEnoughMoney
from .models import Food, Medicine
from .tamagochi import AbstractTamagochi


class AbstractGame(ABC):
    """Интерфейс для логики игры"""

    @abstractmethod
    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine]
    ):
        """
        Абстрактный метод инициализации класса игры

        :param tamagochi: экземпляр тамагочи
        :param clicker: экземпляр кликера
        :param all_food: все доступные варианты еды
        :param all_medicine: все доступные варианты лекарств
        """
        raise NotImplementedError

    @abstractmethod
    def work(self) -> int:
        """
        Абстрактный метод для логики действия "работа

        :return: количество заработанных монет
        """
        raise NotImplementedError

    @abstractmethod
    def buy_food(self) -> None:
        """Абстрактный метод для покупки еды"""
        raise NotImplementedError

    @abstractmethod
    def buy_medicine(self) -> None:
        """Абстрактный метод для покупки лекарства"""
        raise NotImplementedError

    @abstractmethod
    def feed_tamagochi(self) -> None:
        """Абстрактный метод для кормления тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def heal_tamagochi(self) -> None:
        """Абстрактный метод для лечения тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def rest_tamagochi(self) -> None:
        """Абстрактный метод для отдыха тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def play_with_tamagochi(self) -> None:
        """Абстрактный метод для игры с тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def get_status(self) -> dict[str, Any]:
        """
        Абстрактный метод для получения статуса (всех характеристик) тамагочи

        :return: словарь со всеми характеристиками тамагочи
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def food(self) -> list[Food]:
        """
        Абстрактное свойство для доступа к сумке с едой

        :return: список с имеющимися (купленными) объектами еды
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def medicine(self) -> list[Medicine]:
        """
        Абстрактное свойство для доступа к сумке с лекарствами

        :return: список с имеющимися (купленными) объектами лекарств
        """
        raise NotImplementedError


class MyGame(AbstractGame):
    """Основная логика игры."""

    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine],
    ) -> None:
        """Создаёт игру.

        :param tamagochi: питомец
        :param clicker: кликер для заработка монет
        :param all_food: еда, доступная в магазине
        :param all_medicine: доступные лекарства
        """
        self.tamagochi = tamagochi
        self.clicker = clicker
        self.all_food = all_food
        self.all_medicine = all_medicine
        self.coins = 0
        self._food: list[Food] = []
        self._medicine: list[Medicine] = []

    def work(self) -> int:
        """Начислить монеты за работу.

        :return: количество заработанных монет
        """
        self.clicker.click()
        income = self.clicker.income_per_click
        self.coins += income
        return income

    def buy_food(self) -> None:
        """Купить еду на выбор."""
        food = choose_item(self.all_food, 'Выберите еду')
        if food is None:
            return

        if self.coins < food.price:
            raise NotEnoughMoney(
                'Недостаточно монет для покупки еды',
            )

        self.coins -= food.price
        self._food.append(food)
        self.tamagochi.update()

    def buy_medicine(self) -> None:
        """Купить лекарства на выбор."""
        medicine = choose_item(
            self.all_medicine,
            'Выберите лекарство',
        )
        if medicine is None:
            return

        if self.coins < medicine.price:
            raise NotEnoughMoney(
                'Недостаточно монет для покупки лекарства',
            )

        self.coins -= medicine.price
        purchased_medicine = Medicine(
            name=medicine.name,
            price=medicine.price,
            heal_hp=medicine.heal_hp,
            number_of_uses=medicine.number_of_uses,
        )
        self._medicine.append(purchased_medicine)
        self.tamagochi.update()

    def feed_tamagochi(self) -> None:
        """Кормит питомца выбранной едой."""
        food = choose_item(
            self._food,
            'Выберите еду из сумки',
        )
        if food is None:
            return

        self.tamagochi.feed(food)
        self._food.remove(food)
        self.tamagochi.update()

    def heal_tamagochi(self) -> None:
        """Лечит питомца выбранным лекарством."""
        medicine = choose_item(
            self._medicine,
            'Выберите лекарство из сумки',
        )
        if medicine is None:
            return

        self.tamagochi.heal(medicine)
        if medicine.is_empty():
            self._medicine.remove(medicine)
        self.tamagochi.update()

    def rest_tamagochi(self) -> None:
        """Даёт питомцу отдохнуть."""
        self.tamagochi.rest()
        self.tamagochi.update()

    def play_with_tamagochi(self) -> None:
        """Играет с питомцем."""
        self.tamagochi.play()
        self.tamagochi.update()

    def get_status(self) -> dict[str, Any]:
        """Возвращает общий статус игры.

        :return: показатели питомца и монеты
        """
        status = self.tamagochi.status.copy()
        status['coins'] = self.coins
        return status

    @property
    def food(self) -> list[Food]:
        """Возвращает купленную еду.

        :return: список еды в сумке
        """
        return self._food

    @property
    def medicine(self) -> list[Medicine]:
        """Возвращает купленные лекарства.

        :return: список лекарств в сумке
        """
        return self._medicine

    def show_menu(self) -> None:
        """Показывает состояние питомца и доступные действия.

        :param game: текущая игра
        """
        status = self.get_status()
        print(f"Сумка с едой: {self.food}")
        print(f"Сумка с лекарствами: {self.medicine}")
        print(
            f"\nСтатус: голод {status['hunger']}, "
            f"усталость {status['tiredness']}, "
            f"здоровье {status['hp']}, энергия {status['energy']}, "
            f"монет {status['coins']}\n"
        )
        if self.tamagochi.is_sick():
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


def choose_item(items: list[Any], title: str) -> Any | None:
    """Возвращает выбранный предмет.

    :param items: предметы для выбора
    :param title: текст перед списком
    :return: предмет или None
    """
    if not items:
        print('Список пуст')
        return

    print(title)
    for number, item in enumerate(items, start=1):
        print(f'{number}. {item}')
    print('0. Отмена')

    try:
        number = int(input('Введите номер: '))
    except ValueError:
        print('Нужно ввести номер из списка')
        return

    if number == 0:
        return
    if number < 1 or number > len(items):
        print('Такого номера нет')
        return

    return items[number - 1]
