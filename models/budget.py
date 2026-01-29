"""
Budget Model - Data Access Layer
Handles all database operations for budgets table
"""

from typing import Optional, List, Dict
from datetime import datetime, date
from decimal import Decimal
from db_config import execute_query

class Budget:
    """Budget model representing user budget configurations"""
    
    def __init__(self, budget_id: Optional[int] = None, user_id: int = 0,
                 budget_name: str = "", budget_type: str = "",
                 total_amount: Decimal = Decimal('0.00'),
                 start_date: Optional[date] = None, end_date: Optional[date] = None,
                 is_active: bool = True, created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None):
        self.budget_id = budget_id
        self.user_id = user_id
        self.budget_name = budget_name
        self.budget_type = budget_type
        self.total_amount = total_amount
        self.start_date = start_date
        self.end_date = end_date
        self.is_active = is_active
        self.created_at = created_at
        self.updated_at = updated_at
    
    @staticmethod
    def create(user_id: int, budget_name: str, budget_type: str,
               total_amount: float, start_date: str, end_date: str,
               is_active: bool = True) -> int:
        """
        Create a new budget
        
        Args:
            user_id: ID of the user creating the budget
            budget_name: Name of the budget
            budget_type: Type: 'strict', 'moderate', or 'custom'
            total_amount: Total budget amount
            start_date: Budget start date (YYYY-MM-DD)
            end_date: Budget end date (YYYY-MM-DD)
            is_active: Whether budget is active
        
        Returns:
            ID of the newly created budget
        """
        query = """
            INSERT INTO budgets (user_id, budget_name, budget_type, total_amount,
                                start_date, end_date, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        budget_id = execute_query(query, (user_id, budget_name, budget_type,
                                          total_amount, start_date, end_date, is_active))
        return budget_id
    
    @staticmethod
    def get_by_id(budget_id: int) -> Optional[Dict]:
        """
        Retrieve a budget by ID
        
        Args:
            budget_id: The budget's ID
        
        Returns:
            Budget data as dictionary or None if not found
        """
        query = "SELECT * FROM budgets WHERE budget_id = %s"
        results = execute_query(query, (budget_id,), fetch=True)
        return results[0] if results else None
    
    @staticmethod
    def get_by_user(user_id: int) -> List[Dict]:
        """
        Retrieve all budgets for a specific user
        
        Args:
            user_id: The user's ID
        
        Returns:
            List of budgets as dictionaries
        """
        query = "SELECT * FROM budgets WHERE user_id = %s ORDER BY created_at DESC"
        return execute_query(query, (user_id,), fetch=True)
    
    @staticmethod
    def get_active_budgets(user_id: Optional[int] = None) -> List[Dict]:
        """
        Retrieve all active budgets, optionally filtered by user
        
        Args:
            user_id: Optional user ID to filter by
        
        Returns:
            List of active budgets as dictionaries
        """
        if user_id:
            query = """
                SELECT * FROM budgets 
                WHERE is_active = TRUE AND user_id = %s 
                ORDER BY created_at DESC
            """
            return execute_query(query, (user_id,), fetch=True)
        else:
            query = "SELECT * FROM budgets WHERE is_active = TRUE ORDER BY created_at DESC"
            return execute_query(query, fetch=True)
    
    @staticmethod
    def get_all() -> List[Dict]:
        """
        Retrieve all budgets
        
        Returns:
            List of all budgets as dictionaries
        """
        query = "SELECT * FROM budgets ORDER BY created_at DESC"
        return execute_query(query, fetch=True)
    
    @staticmethod
    def update(budget_id: int, budget_name: Optional[str] = None,
               budget_type: Optional[str] = None, total_amount: Optional[float] = None,
               start_date: Optional[str] = None, end_date: Optional[str] = None,
               is_active: Optional[bool] = None) -> bool:
        """
        Update budget information
        
        Args:
            budget_id: ID of budget to update
            budget_name: New budget name (optional)
            budget_type: New budget type (optional)
            total_amount: New total amount (optional)
            start_date: New start date (optional)
            end_date: New end date (optional)
            is_active: New active status (optional)
        
        Returns:
            True if update successful
        """
        updates = []
        params = []
        
        if budget_name is not None:
            updates.append("budget_name = %s")
            params.append(budget_name)
        if budget_type is not None:
            updates.append("budget_type = %s")
            params.append(budget_type)
        if total_amount is not None:
            updates.append("total_amount = %s")
            params.append(total_amount)
        if start_date is not None:
            updates.append("start_date = %s")
            params.append(start_date)
        if end_date is not None:
            updates.append("end_date = %s")
            params.append(end_date)
        if is_active is not None:
            updates.append("is_active = %s")
            params.append(is_active)
        
        if not updates:
            return False
        
        params.append(budget_id)
        query = f"UPDATE budgets SET {', '.join(updates)} WHERE budget_id = %s"
        execute_query(query, tuple(params))
        return True
    
    @staticmethod
    def delete(budget_id: int) -> bool:
        """
        Delete a budget (will cascade to budget rules)
        
        Args:
            budget_id: ID of budget to delete
        
        Returns:
            True if deletion successful
        """
        query = "DELETE FROM budgets WHERE budget_id = %s"
        execute_query(query, (budget_id,))
        return True
    
    @staticmethod
    def deactivate(budget_id: int) -> bool:
        """
        Deactivate a budget (soft delete)
        
        Args:
            budget_id: ID of budget to deactivate
        
        Returns:
            True if deactivation successful
        """
        return Budget.update(budget_id, is_active=False)
    
    @staticmethod
    def count() -> int:
        """
        Count total number of budgets
        
        Returns:
            Total budget count
        """
        query = "SELECT COUNT(*) as count FROM budgets"
        result = execute_query(query, fetch=True)
        return result[0]['count'] if result else 0
    
    @staticmethod
    def get_budget_summary(budget_id: int) -> Optional[Dict]:
        """
        Get detailed summary of a budget including user info and rule count
        
        Args:
            budget_id: The budget's ID
        
        Returns:
            Budget summary with additional information
        """
        query = """
            SELECT b.*, u.username, u.email,
                   COUNT(DISTINCT br.rule_id) as rule_count
            FROM budgets b
            JOIN users u ON b.user_id = u.user_id
            LEFT JOIN budget_rules br ON b.budget_id = br.budget_id
            WHERE b.budget_id = %s
            GROUP BY b.budget_id
        """
        results = execute_query(query, (budget_id,), fetch=True)
        return results[0] if results else None
    
    def __repr__(self):
        return f"Budget(id={self.budget_id}, name='{self.budget_name}', type='{self.budget_type}')"
