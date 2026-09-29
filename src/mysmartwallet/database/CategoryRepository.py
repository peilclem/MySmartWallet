from mysmartwallet.database.DatabaseManager import DatabaseManager
from mysmartwallet.models.category import Category


class CategoryRepository:
    def __init__(self, db_manager: DatabaseManager) -> None:
        self.db_manager = db_manager

    def get_category_by_id(self, category_id: int) -> Category | None:
        """Retrieve a category by its ID from the database."""
        query = """SELECT * FROM Categories WHERE Category_id = ?"""
        result = self.db_manager.execute(query, (category_id,))
        if result:
            return Category(**result[0])
        return None

    def get_id_by_name(self, category_name: str) -> int | None:
        """Retrieve a category ID by its name from the database."""
        query = """SELECT Category_id FROM Categories WHERE Category_name = ?"""
        result = self.db_manager.execute(query, (category_name,))
        if result:
            return result[0]["Category_id"]
        return None

    def get_all_categories(self) -> list[Category]:
        """Retrieve all categories from the database."""
        query = """SELECT * FROM Categories"""
        result = self.db_manager.execute(query)
        return [Category(**row) for row in result]

    def add_category(self, category: Category):
        """Add a new category to the database."""
        query = """
        INSERT INTO Categories
        (Category_name, Parent_id, Type, User_id)
        VALUES (?, ?, ?, ?)
        """
        self.db_manager.execute(
            query,
            (
                category.name,
                category.parent_id,
                category.type,
                category.user_id,
            ),
        )
        self.db_manager.commit()

    def delete_category(self, category_id: int) -> None:
        """Delete a category from the database by its ID."""
        query = """DELETE FROM Categories WHERE Category_id = ?"""
        self.db_manager.execute(query, (category_id,))
        self.db_manager.commit()
