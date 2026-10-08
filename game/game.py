"""Интерфейс и реализация класса игры."""

from abc import ABC, abstractmethod
from copy import copy
from typing import Any

from .clicker import AbstractClicker
from .exceptions import (
    EmptyItemList,
    InvalidItemNumber,
    ItemNotFound,
    NotEnoughMoney,
)
from .models import Food, Medicine
from .tamagochi import AbstractTamagochi

STATUS_TEMPLATE = (
    '\nСтатус: голод {hunger}, усталость {tiredness}, '
    'здоровье {hp}, энергия {energy}, монет {coins}\n'
)
MENU_ITEMS = (
    '1. Пойти на работу',
    '2. Купить еду',
    '3. Купить лекарство',
    '4. Покормить',
    '5. Вылечить',
    '6. Играть',
    '7. Отдых',
    '0. Выход',
)
MENU = '\n'.join(MENU_ITEMS)
SICK_MESSAGE = (
    '=======Тамагочи болеет======\n'
    '=======Отдых действует менее эффективно======='
)


class AbstractGame(ABC):
    """Интерфейс для логики игры."""

    @abstractmethod
    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine]
    ):
        """Абстрактный метод инициализации класса игры.

        :param tamagochi: экземпляр тамагочи
        :param clicker: экземпляр кликера
        :param all_food: все доступные варианты еды
        :param all_medicine: все доступные варианты лекарств
        """
        raise NotImplementedError

    @abstractmethod
    def work(self) -> int:
        """Абстрактный метод для логики действия «работа».

        :return: количество заработанных монет
        """
        raise NotImplementedError

    @abstractmethod
    def buy_food(self) -> None:
        """Абстрактный метод для покупки еды."""
        raise NotImplementedError

    @abstractmethod
    def buy_medicine(self) -> None:
        """Абстрактный метод для покупки лекарства."""
        raise NotImplementedError

    @abstractmethod
    def feed_tamagochi(self) -> None:
        """Абстрактный метод для кормления тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def heal_tamagochi(self) -> None:
        """Абстрактный метод для лечения тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def rest_tamagochi(self) -> None:
        """Абстрактный метод для отдыха тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def play_with_tamagochi(self) -> None:
        """Абстрактный метод для игры с тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def get_status(self) -> dict[str, Any]:
        """Абстрактный метод для получения статуса тамагочи.

        :return: словарь со всеми характеристиками тамагочи
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def food(self) -> list[Food]:
        """Абстрактное свойство для доступа к сумке с едой.

        :return: список с имеющимися (купленными) объектами еды
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def medicine(self) -> list[Medicine]:
        """Абстрактное свойство для доступа к сумке с лекарствами.

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
        self._tamagochi = tamagochi
        self._clicker = clicker
        self._all_food = list(all_food)
        self._all_medicine = list(all_medicine)
        self._coins = 0
        self._food: list[Food] = []
        self._medicine: list[Medicine] = []

    def work(self) -> int:
        """Начислить монеты за работу.

        :return: количество заработанных монет
        """
        self._clicker.click()
        income = self._clicker.income_per_click
        self._coins += income
        self._tamagochi.update()
        return income

    def buy_food(self) -> None:
        """Купить еду на выбор."""
        food = choose_item(self._all_food, 'Выберите еду')
        if food is None:
            return

        if self._coins < food.price:
            raise NotEnoughMoney(
                'Недостаточно монет для покупки еды',
            )

        self._coins -= food.price
        self._food.append(food)
        self._tamagochi.update()

    def buy_medicine(self) -> None:
        """Купить лекарства на выбор."""
        medicine = choose_item(
            self._all_medicine,
            'Выберите лекарство',
        )
        if medicine is None:
            return

        if self._coins < medicine.price:
            raise NotEnoughMoney(
                'Недостаточно монет для покупки лекарства',
            )

        self._coins -= medicine.price
        self._medicine.append(copy(medicine))
        self._tamagochi.update()

    def feed_tamagochi(self) -> None:
        """Кормит питомца выбранной едой."""
        food = choose_item(
            self._food,
            'Выберите еду из сумки',
        )
        if food is None:
            return

        self._tamagochi.feed(food)
        self._food.remove(food)
        self._tamagochi.update()

    def heal_tamagochi(self) -> None:
        """Лечит питомца выбранным лекарством."""
        medicine = choose_item(
            self._medicine,
            'Выберите лекарство из сумки',
        )
        if medicine is None:
            return

        self._tamagochi.heal(medicine)
        if medicine.is_empty():
            self._medicine.remove(medicine)
        self._tamagochi.update()

    def rest_tamagochi(self) -> None:
        """Даёт питомцу отдохнуть."""
        self._tamagochi.rest()
        self._tamagochi.update()

    def play_with_tamagochi(self) -> None:
        """Играет с питомцем."""
        self._tamagochi.play()
        self._tamagochi.update()

    def get_status(self) -> dict[str, Any]:
        """Возвращает общий статус игры.

        :return: показатели питомца и монеты
        """
        status = self._tamagochi.status.copy()
        status['coins'] = self._coins
        return status

    @property
    def food(self) -> list[Food]:
        """Возвращает купленную еду.

        :return: список еды в сумке
        """
        return list(self._food)

    @property
    def medicine(self) -> list[Medicine]:
        """Возвращает купленные лекарства.

        :return: список лекарств в сумке
        """
        return list(self._medicine)

    def show_menu(self) -> None:
        """Показывает состояние питомца и доступные действия."""
        lines = [
            f'Сумка с едой: {self.food}',
            f'Сумка с лекарствами: {self.medicine}',
            STATUS_TEMPLATE.format(**self.get_status()),
        ]
        if self._tamagochi.is_sick():
            lines.append(SICK_MESSAGE)
        lines.append(MENU)
        print('\n'.join(lines))


def choose_item(items: list[Any], title: str) -> Any | None:
    """Возвращает выбранный предмет.

    :param items: предметы для выбора
    :param title: текст перед списком
    :return: предмет или None
    """
    if not items:
        raise EmptyItemList('Список пуст')

    lines = [title]
    for number, item in enumerate(items, start=1):
        lines.append(f'{number}. {item}')
    lines.append('0. Отмена')
    print('\n'.join(lines))

    try:
        number = int(input('Введите номер: '))
    except ValueError as error:
        raise InvalidItemNumber('Нужно ввести номер из списка') from error

    if number == 0:
        return
    if number < 1 or number > len(items):
        raise ItemNotFound('Такого номера нет')

    return items[number - 1]
