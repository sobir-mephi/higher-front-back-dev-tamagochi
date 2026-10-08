"""Модуль с исключениями."""


class TamagochiIsGone(Exception):
    """Ошибка при смерти тамагочи."""


class NotEnoughMoney(Exception):
    """Ошибка когда не хватает монет для покупки."""


class EmptyItemList(Exception):
    """Ошибка при выборе из пустого списка."""


class InvalidItemNumber(Exception):
    """Ошибка при вводе номера предмета."""


class ItemNotFound(Exception):
    """Ошибка при выборе несуществующего номера."""


class MedicineIsEmpty(Exception):
    """Ошибка при использовании закончившегося лекарства."""
