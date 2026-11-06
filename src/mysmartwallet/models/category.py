from dataclasses import dataclass

from mysmartwallet.utils.enums import EnumCategoryType


@dataclass
class Category:
    """A class representing a category object."""

    name: str
    parentId: int | None = None
    type: EnumCategoryType = EnumCategoryType.EXPENSE
    userId: int | None = None

    @property
    def isRoot(self) -> bool:
        """Check if the category is a root category (i.e., has no parent)

        Returns
        -------
        bool
            True if the category is a root category, False otherwise
        """
        return self.parentId is None

    @property
    def isExpense(self) -> bool:
        """Check if the category is an expense category

        Returns
        -------
        bool
            True if the category is an expense category, False otherwise
        """
        return self.type.lower() == "expense"

    @property
    def isIncome(self) -> bool:
        """Check if the category is an income category

        Returns
        -------
        bool
            True if the category is an income category, False otherwise
        """
        return self.type.lower() == "income"

    @property
    def isTransfer(self) -> bool:
        """Check if the category is a transfer category

        Returns
        -------
        bool
            True if the category is a transfer category, False otherwise
        """
        return self.type.lower() == "transfer"
