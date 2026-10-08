"""Интерфейс и реализация кликера."""

from abc import ABC, abstractmethod
from random import randint


class AbstractClicker(ABC):
    """Интерфейс для кликера."""

    @abstractmethod
    def __init__(self) -> None:
        """Абстрактный метод инициализации."""
        raise NotImplementedError

    @abstractmethod
    def click(self) -> None:
        """Абстрактный метод клика для накапливания монет."""
        raise NotImplementedError

    @property
    @abstractmethod
    def income_per_click(self) -> int:
        """Абстрактное свойство для доступа к количеству монет за клик."""
        raise NotImplementedError


class MyClicker(AbstractClicker):
    """Кликер со случайным заработком."""

    def __init__(self, min_income: int, max_income: int) -> None:
        """Сохраняет границы заработка.

        :param min_income: минимальный заработок
        :param max_income: максимальный заработок
        """
        self._min_income = min_income
        self._max_income = max_income
        self._income_per_click = 0

    def click(self) -> None:
        """Определяет заработок за текущий клик."""
        self._income_per_click = randint(
            self._min_income,
            self._max_income,
        )

    @property
    def income_per_click(self) -> int:
        """Возвращает заработок за последний клик.

        :return: заработанное количество монет
        """
        return self._income_per_click
