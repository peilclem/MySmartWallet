from dataclasses import dataclass

from mysmartwallet.utils.enums import EnumCategoryType


@dataclass
class Category:
    """A class representing a category object."""

    name: str
    parent_id: int | None = None
    type: EnumCategoryType = EnumCategoryType.EXPENSE
    user_id: int | None = None

    @property
    def is_root(self) -> bool:
        """Check if the category is a root category (i.e., has no parent)

        Returns
        -------
        bool
            True if the category is a root category, False otherwise
        """
        return self.parent_id is None

    @property
    def is_expense(self) -> bool:
        """Check if the category is an expense category

        Returns
        -------
        bool
            True if the category is an expense category, False otherwise
        """
        return self.type.lower() == "expense"

    @property
    def is_income(self) -> bool:
        """Check if the category is an income category

        Returns
        -------
        bool
            True if the category is an income category, False otherwise
        """
        return self.type.lower() == "income"

    @property
    def is_transfer(self) -> bool:
        """Check if the category is a transfer category

        Returns
        -------
        bool
            True if the category is a transfer category, False otherwise
        """
        return self.type.lower() == "transfer"
