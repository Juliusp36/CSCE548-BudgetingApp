"""
Category Manager - Business Layer
Handles category-related business logic and validation
"""

from typing import Optional, List, Dict
from models.category import Category
from models.transaction import Transaction


class CategoryManager:
    """
    Business layer for Category operations
    Implements business rules and validation before calling data layer
    """
    
    @staticmethod
    def save(category_id: int, category_name: str, description: str = "", 
             icon: str = "") -> Dict:
        """
        Save category (insert if ID is 0, update if ID exists)
        
        Business Rules:
        - Category name must be unique
        - Category name is required
        
        Args:
            category_id: Category ID (0 for new category)
            category_name: Unique category name
            description: Category description (optional)
            icon: Category icon/emoji (optional)
        
        Returns:
            Dict with success status and category_id or error message
        """
        try:
            # Validate category name
            if not category_name or category_name.strip() == "":
                return {"success": False, "error": "Category name is required"}
            
            # Check for duplicate category name
            existing = Category.get_by_name(category_name)
            if existing and existing['category_id'] != category_id:
                return {"success": False, "error": "Category name already exists"}
            
            # If ID is 0, this is a new record (INSERT)
            if category_id == 0:
                new_id = Category.create(category_name, description, icon)
                return {
                    "success": True,
                    "category_id": new_id,
                    "message": "Category created successfully"
                }
            
            # If ID exists, this is an update (UPDATE)
            else:
                # Verify category exists
                existing = Category.get_by_id(category_id)
                if not existing:
                    return {"success": False, "error": "Category not found"}
                
                Category.update(category_id, category_name=category_name, 
                              description=description, icon=icon)
                return {
                    "success": True,
                    "category_id": category_id,
                    "message": "Category updated successfully"
                }
                
        except Exception as e:
            return {"success": False, "error": f"Database error: {str(e)}"}
    
    @staticmethod
    def get_by_id(category_id: int) -> Optional[Dict]:
        """
        Get category by ID
        
        Args:
            category_id: Category ID to retrieve
        
        Returns:
            Category data dictionary or None if not found
        """
        try:
            return Category.get_by_id(category_id)
        except Exception as e:
            print(f"Error retrieving category: {e}")
            return None
    
    @staticmethod
    def get_all() -> List[Dict]:
        """
        Get all categories
        
        Returns:
            List of all categories
        """
        try:
            return Category.get_all()
        except Exception as e:
            print(f"Error retrieving categories: {e}")
            return []
    
    @staticmethod
    def delete(category_id: int) -> Dict:
        """
        Delete category
        
        Business Rules:
        - Category must exist
        - Cannot delete if category has transactions (RESTRICT constraint)
        
        Args:
            category_id: Category ID to delete
        
        Returns:
            Dict with success status and message
        """
        try:
            # Verify category exists
            category = Category.get_by_id(category_id)
            if not category:
                return {"success": False, "error": "Category not found"}
            
            # Check if category has transactions
            transactions = Transaction.get_by_category(category_id, limit=1)
            if transactions:
                return {
                    "success": False,
                    "error": "Cannot delete category with existing transactions"
                }
            
            # Delete category
            Category.delete(category_id)
            return {
                "success": True,
                "message": f"Category '{category['category_name']}' deleted successfully"
            }
            
        except Exception as e:
            return {"success": False, "error": f"Delete error: {str(e)}"}
    
    @staticmethod
    def get_with_transaction_count() -> List[Dict]:
        """
        Get all categories with their transaction counts (additional business method)
        
        Returns:
            List of categories with transaction counts
        """
        try:
            return Category.get_with_transaction_count()
        except Exception as e:
            print(f"Error retrieving categories: {e}")
            return []
    
    @staticmethod
    def count() -> int:
        """
        Get total category count (additional business method)
        
        Returns:
            Total number of categories
        """
        try:
            return Category.count()
        except Exception as e:
            print(f"Error counting categories: {e}")
            return 0
