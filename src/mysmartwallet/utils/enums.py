from enum import StrEnum, auto


class EnumCategoryType(StrEnum):
    EXPENSE = auto()
    INCOME = auto()
    TRANSFER = auto()
