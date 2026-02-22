"""
Category Model - Data Access Layer
Handles all database operations for categories table
"""

from typing import Optional, List, Dict
from datetime import datetime
from db_config import execute_query

class Category:
    """Category model representing spending categories"""
    
    def __init__(self, category_id: Optional[int] = None, category_name: str = "",
                 description: str = "", icon: str = "",
                 created_at: Optional[datetime] = None):
        self.category_id = category_id
        self.category_name = category_name
        self.description = description
        self.icon = icon
        self.created_at = created_at
    
    @staticmethod
    def create(category_name: str, description: str = "", icon: str = "") -> int:
        """
        Create a new category
        
        Args:
            category_name: Name of the category
            description: Category description
            icon: Icon/emoji for the category
        
        Returns:
            ID of the newly created category
        """
        query = """
            INSERT INTO categories (category_name, description, icon)
            VALUES (%s, %s, %s)
        """
        category_id = execute_query(query, (category_name, description, icon))
        return category_id
    
    @staticmethod
    def get_by_id(category_id: int) -> Optional[Dict]:
        """
        Retrieve a category by ID
        
        Args:
            category_id: The category's ID
        
        Returns:
            Category data as dictionary or None if not found
        """
        query = "SELECT * FROM categories WHERE category_id = %s"
        results = execute_query(query, (category_id,), fetch=True)
        return results[0] if results else None
    
    @staticmethod
    def get_by_name(category_name: str) -> Optional[Dict]:
        """
        Retrieve a category by name
        
        Args:
            category_name: The category name to search for
        
        Returns:
            Category data as dictionary or None if not found
        """
        query = "SELECT * FROM categories WHERE category_name = %s"
        results = execute_query(query, (category_name,), fetch=True)
        return results[0] if results else None
    
    @staticmethod
    def get_all() -> List[Dict]:
        """
        Retrieve all categories
        
        Returns:
            List of all categories as dictionaries
        """
        query = "SELECT * FROM categories ORDER BY category_name"
        return execute_query(query, fetch=True)
    
    @staticmethod
    def update(category_id: int, category_name: Optional[str] = None,
               description: Optional[str] = None, icon: Optional[str] = None) -> bool:
        """
        Update category information
        
        Args:
            category_id: ID of category to update
            category_name: New category name (optional)
            description: New description (optional)
            icon: New icon (optional)
        
        Returns:
            True if update successful
        """
        updates = []
        params = []
        
        if category_name is not None:
            updates.append("category_name = %s")
            params.append(category_name)
        if description is not None:
            updates.append("description = %s")
            params.append(description)
        if icon is not None:
            updates.append("icon = %s")
            params.append(icon)
        
        if not updates:
            return False
        
        params.append(category_id)
        query = f"UPDATE categories SET {', '.join(updates)} WHERE category_id = %s"
        execute_query(query, tuple(params))
        return True
    
    @staticmethod
    def delete(category_id: int) -> bool:
        """
        Delete a category
        Note: This will fail if there are transactions using this category (RESTRICT constraint)
        
        Args:
            category_id: ID of category to delete
        
        Returns:
            True if deletion successful
        """
        query = "DELETE FROM categories WHERE category_id = %s"
        execute_query(query, (category_id,))
        return True
    
    @staticmethod
    def count() -> int:
        """
        Count total number of categories
        
        Returns:
            Total category count
        """
        query = "SELECT COUNT(*) as count FROM categories"
        result = execute_query(query, fetch=True)
        return result[0]['count'] if result else 0
    
    @staticmethod
    def get_with_transaction_count() -> List[Dict]:
        """
        Get all categories with their transaction counts
        
        Returns:
            List of categories with transaction counts
        """
        query = """
            SELECT c.*, COUNT(t.transaction_id) as transaction_count
            FROM categories c
            LEFT JOIN transactions t ON c.category_id = t.category_id
            GROUP BY c.category_id
            ORDER BY c.category_name
        """
        return execute_query(query, fetch=True)
    
    def __repr__(self):
        return f"Category(id={self.category_id}, name='{self.category_name}')"
