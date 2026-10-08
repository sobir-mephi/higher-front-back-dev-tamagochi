"""Интерфейс и реализация класса тамагочи."""

from abc import ABC, abstractmethod

from .exceptions import MedicineIsEmpty, TamagochiIsGone
from .models import Food, Medicine


DEFAULT_HUNGER = 10
DEFAULT_TIREDNESS = 0
DEFAULT_HP = 100
DEFAULT_ENERGY = 100


class AbstractTamagochi(ABC):
    """Интерфейс логики тамагочи."""

    @abstractmethod
    def feed(self, food: Food) -> None:
        """Абстрактный метод для кормления тамагочи.

        :param food: объект еды для кормления
        """
        raise NotImplementedError

    @abstractmethod
    def play(self) -> None:
        """Абстрактный метод для игры с тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def rest(self) -> None:
        """Абстрактный метод для отдыха тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def heal(self, medicine: Medicine) -> None:
        """Абстрактный метод для лечения тамагочи.

        :param medicine: лекарство для лечения
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def status(self) -> dict[str, int]:
        """Абстрактное свойство для доступа ко всем состояниям тамагочи.

        :return: словарь со всеми состояниями тамагочи
        """
        raise NotImplementedError

    @abstractmethod
    def is_alive(self) -> bool:
        """Абстрактный метод для проверки жив ли тамагочи.

        :return: True если жив, иначе False
        """
        raise NotImplementedError

    @abstractmethod
    def is_sick(self) -> bool:
        """Абстрактный метод для проверки, не заболел ли тамагочи.

        :return: True если тамагочи болеет, иначе False
        """
        raise NotImplementedError

    @abstractmethod
    def update(self) -> None:
        """Абстрактный метод для обновления состояний тамагочи.

        Должен использоваться после каждого взаимодействия с тамагочи.
        """
        raise NotImplementedError


class MyTamagochi(AbstractTamagochi):
    """Питомец для консольной игры."""

    def __init__(
        self,
        hunger: int = DEFAULT_HUNGER,
        tiredness: int = DEFAULT_TIREDNESS,
        hp: int = DEFAULT_HP,
        energy: int = DEFAULT_ENERGY,
    ) -> None:
        """Создаёт питомца с начальными параметрами."""
        self._hunger = hunger
        self._tiredness = tiredness
        self._hp = hp
        self._energy = energy
        self.normalize_stats()

    def feed(self, food: Food) -> None:
        """Кормит питомца и уменьшает его голод.

        :param food: еда, которой кормят питомца
        """
        self._hunger -= food.satiety
        if self._hunger < 0:
            self._hunger = 0

        self._energy -= 2
        if self._energy < 0:
            self._energy = 0

    def play(self) -> None:
        """Играет с питомцем и расходует энергию."""
        self._energy -= 15
        self._hunger += 5
        self._tiredness += 10
        self.normalize_stats()

    def rest(self) -> None:
        """Восстанавливает энергию и снимает усталость."""
        energy_recovery = 20
        if self.is_sick():
            energy_recovery = 10

        self._energy += energy_recovery
        self._tiredness -= 20
        self.normalize_stats()

    def heal(self, medicine: Medicine) -> None:
        """Лечит питомца.

        :param medicine: лекарство
        """
        if medicine.is_empty():
            raise MedicineIsEmpty('Лекарство закончилось')

        self._hp += medicine.heal_hp
        medicine.uses += 1
        self.normalize_stats()

    @property
    def status(self) -> dict[str, int]:
        """Возвращает показатели питомца.

        :return: словарь с показателями
        """
        return {
            'hunger': self._hunger,
            'tiredness': self._tiredness,
            'hp': self._hp,
            'energy': self._energy,
        }

    def is_alive(self) -> bool:
        """Проверяет, жив ли питомец.

        :return: True, если здоровье больше нуля
        """
        return self._hp > 0

    def is_sick(self) -> bool:
        """Проверяет, заболел ли питомец.

        :return: True при плохих показателях
        """
        return (
            self._hunger >= 80
            or self._tiredness >= 80
            or self._energy <= 20
        )

    def update(self) -> None:
        """Обновляет питомца после действия."""
        self._hunger += 5
        self._tiredness += 5
        self._energy -= 5

        if self.is_sick():
            self._hp -= 10
            self._tiredness += 5
        else:
            self._hp -= 2

        self.normalize_stats()

        if not self.is_alive():
            raise TamagochiIsGone('Питомец умер')

    def normalize_stats(self) -> None:
        """Оставляет показатели в диапазоне от 0 до 100."""
        if self._hunger < 0:
            self._hunger = 0
        elif self._hunger > 100:
            self._hunger = 100

        if self._tiredness < 0:
            self._tiredness = 0
        elif self._tiredness > 100:
            self._tiredness = 100

        if self._hp < 0:
            self._hp = 0
        elif self._hp > 100:
            self._hp = 100

        if self._energy < 0:
            self._energy = 0
        elif self._energy > 100:
            self._energy = 100
