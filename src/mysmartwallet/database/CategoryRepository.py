from mysmartwallet.database.DatabaseManager import DatabaseManager
from mysmartwallet.models.category import Category


class CategoryRepository:
    def __init__(self, dbManager: DatabaseManager) -> None:
        self.dbManager = dbManager

    def getCategoryById(self, categoryId: int) -> Category | None:
        """Retrieve a category by its ID from the database."""
        query = """SELECT * FROM Categories WHERE Category_id = ?"""
        result = self.dbManager.execute(query, (categoryId,))
        if result:
            return Category(**result[0])
        return None

    def getIdByName(self, categoryName: str) -> int | None:
        """Retrieve a category ID by its name from the database."""
        query = """SELECT Category_id FROM Categories WHERE Category_name = ?"""
        result = self.dbManager.execute(query, (categoryName,))
        if result:
            return result[0]["Category_id"]
        return None

    def getAllCategories(self) -> list[Category]:
        """Retrieve all categories from the database."""
        query = """SELECT * FROM Categories"""
        result = self.dbManager.execute(query)
        return [Category(**row) for row in result]

    def addCategory(self, category: Category):
        """Add a new category to the database."""
        query = """
        INSERT INTO Categories
        (Category_name, Parent_id, Type, User_id)
        VALUES (?, ?, ?, ?)
        """
        self.dbManager.execute(
            query,
            (
                category.name,
                category.parentId,
                category.type,
                category.userId,
            ),
        )
        self.dbManager.commit()

    def removeCategory(self, categoryId: int) -> None:
        """Delete a category from the database by its ID."""
        query = """DELETE FROM Categories WHERE Category_id = ?"""
        self.dbManager.execute(query, (categoryId,))
        self.dbManager.commit()
