"""Интерфейс и реализация класса тамагочи."""

from abc import ABC, abstractmethod

from .exceptions import TamagochiIsGone
from .models import Food, Medicine


class AbstractTamagochi(ABC):
    """Интерфейс логики тамагочи"""

    @abstractmethod
    def feed(self, food: Food) -> None:
        """
        Абстрактный метод для кормления тамагочи

        :param food: объект еды для кормления
        """
        raise NotImplementedError

    @abstractmethod
    def play(self) -> None:
        """Абстрактный метод для игры с тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def rest(self) -> None:
        """Абстрактный метод для отдыха тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def heal(self, medicine: Medicine) -> None:
        """
        Абстрактный метод для лечения тамагочи

        :param medicine: лекарство для лечения
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def status(self) -> dict[str, int]:
        """
        Абстрактное свойство для доступа ко всем состояниям тамагочи

        :return: словарь со всеми состояниями тамагочи
        """
        raise NotImplementedError

    @abstractmethod
    def is_alive(self) -> bool:
        """
        Абстрактный метод для проверки жив ли тамагочи

        :return: True если жив, иначе False
        """
        raise NotImplementedError

    @abstractmethod
    def is_sick(self) -> bool:
        """
        Абстрактный метод для проверки, не заболел ли тамагочи

        :return: True если тамагочи болеет, иначе False
        """
        raise NotImplementedError

    @abstractmethod
    def update(self) -> None:
        """
        Абстрактный метод для обновления состояний тамагочи.
        Должен использоваться после каждого взаимодействия с тамагочи
        """
        raise NotImplementedError


class MyTamagochi(AbstractTamagochi):
    """Питомец для консольной игры."""

    def __init__(self) -> None:
        """Создаёт питомца с начальными параметрами."""
        self.hunger = 20
        self.tiredness = 0
        self.hp = 100
        self.energy = 100

    def feed(self, food: Food) -> None:
        """Кормит питомца и уменьшает его голод.

        :param food: еда, которой кормят питомца
        """
        self.hunger -= food.satiety
        if self.hunger < 0:
            self.hunger = 0

        self.energy -= 2
        if self.energy < 0:
            self.energy = 0

    def play(self) -> None:
        """Играет с питомцем и расходует энергию."""
        self.energy -= 15
        self.hunger += 5
        self.tiredness += 10
        self.normalize_stats()

    def rest(self) -> None:
        """Восстанавливает энергию и снимает усталость."""
        energy_recovery = 20
        if self.is_sick():
            energy_recovery = 10

        self.energy += energy_recovery
        self.tiredness -= 20
        self.normalize_stats()

    def heal(self, medicine: Medicine) -> None:
        """Лечит питомца.

        :param medicine: лекарство
        """
        if medicine.is_empty():
            print('Лекарство закончилось')
            return

        self.hp += medicine.heal_hp
        medicine.uses += 1
        self.normalize_stats()

    @property
    def status(self) -> dict[str, int]:
        """Возвращает показатели питомца.

        :return: словарь с показателями
        """
        return {
            'hunger': self.hunger,
            'tiredness': self.tiredness,
            'hp': self.hp,
            'energy': self.energy,
        }

    def is_alive(self) -> bool:
        """Проверяет, жив ли питомец.

        :return: True, если здоровье больше нуля
        """
        return self.hp > 0

    def is_sick(self) -> bool:
        """Проверяет, заболел ли питомец.

        :return: True при плохих показателях
        """
        return (
            self.hunger >= 80
            or self.tiredness >= 80
            or self.energy <= 20
        )

    def update(self) -> None:
        """Обновляет питомца после действия."""
        self.hunger += 5
        self.tiredness += 5
        self.energy -= 5

        if self.is_sick():
            self.hp -= 10
            self.tiredness += 5
        else:
            self.hp -= 2

        self.normalize_stats()

        if not self.is_alive():
            raise TamagochiIsGone('Питомец умер')

    def normalize_stats(self) -> None:
        """Оставляет показатели в диапазоне от 0 до 100."""
        if self.hunger < 0:
            self.hunger = 0
        elif self.hunger > 100:
            self.hunger = 100

        if self.tiredness < 0:
            self.tiredness = 0
        elif self.tiredness > 100:
            self.tiredness = 100

        if self.hp < 0:
            self.hp = 0
        elif self.hp > 100:
            self.hp = 100

        if self.energy < 0:
            self.energy = 0
        elif self.energy > 100:
            self.energy = 100
