"""
Budget Rule Model - Data Access Layer
Handles all database operations for budget_rules table
"""

from typing import Optional, List, Dict
from datetime import datetime
from decimal import Decimal
from db_config import execute_query

class BudgetRule:
    """Budget Rule model representing category spending limits within budgets"""
    
    def __init__(self, rule_id: Optional[int] = None, budget_id: int = 0,
                 category_id: int = 0, limit_amount: Decimal = Decimal('0.00'),
                 alert_threshold: Decimal = Decimal('80.00'),
                 created_at: Optional[datetime] = None):
        self.rule_id = rule_id
        self.budget_id = budget_id
        self.category_id = category_id
        self.limit_amount = limit_amount
        self.alert_threshold = alert_threshold
        self.created_at = created_at
    
    @staticmethod
    def create(budget_id: int, category_id: int, limit_amount: float,
               alert_threshold: float = 80.00) -> int:
        """
        Create a new budget rule
        
        Args:
            budget_id: ID of the budget
            category_id: ID of the category
            limit_amount: Spending limit for this category
            alert_threshold: Percentage threshold for alerts (0-100)
        
        Returns:
            ID of the newly created budget rule
        """
        query = """
            INSERT INTO budget_rules (budget_id, category_id, limit_amount, alert_threshold)
            VALUES (%s, %s, %s, %s)
        """
        rule_id = execute_query(query, (budget_id, category_id, limit_amount, alert_threshold))
        return rule_id
    
    @staticmethod
    def get_by_id(rule_id: int) -> Optional[Dict]:
        """
        Retrieve a budget rule by ID
        
        Args:
            rule_id: The rule's ID
        
        Returns:
            Budget rule data as dictionary or None if not found
        """
        query = "SELECT * FROM budget_rules WHERE rule_id = %s"
        results = execute_query(query, (rule_id,), fetch=True)
        return results[0] if results else None
    
    @staticmethod
    def get_by_budget(budget_id: int) -> List[Dict]:
        """
        Retrieve all rules for a specific budget
        
        Args:
            budget_id: The budget's ID
        
        Returns:
            List of budget rules as dictionaries
        """
        query = """
            SELECT br.*, c.category_name, c.icon
            FROM budget_rules br
            JOIN categories c ON br.category_id = c.category_id
            WHERE br.budget_id = %s
            ORDER BY c.category_name
        """
        return execute_query(query, (budget_id,), fetch=True)
    
    @staticmethod
    def get_by_budget_and_category(budget_id: int, category_id: int) -> Optional[Dict]:
        """
        Retrieve a specific rule for a budget-category combination
        
        Args:
            budget_id: The budget's ID
            category_id: The category's ID
        
        Returns:
            Budget rule data as dictionary or None if not found
        """
        query = """
            SELECT * FROM budget_rules 
            WHERE budget_id = %s AND category_id = %s
        """
        results = execute_query(query, (budget_id, category_id), fetch=True)
        return results[0] if results else None
    
    @staticmethod
    def get_all() -> List[Dict]:
        """
        Retrieve all budget rules
        
        Returns:
            List of all budget rules as dictionaries
        """
        query = "SELECT * FROM budget_rules ORDER BY budget_id, category_id"
        return execute_query(query, fetch=True)
    
    @staticmethod
    def update(rule_id: int, limit_amount: Optional[float] = None,
               alert_threshold: Optional[float] = None) -> bool:
        """
        Update budget rule information
        
        Args:
            rule_id: ID of rule to update
            limit_amount: New limit amount (optional)
            alert_threshold: New alert threshold (optional)
        
        Returns:
            True if update successful
        """
        updates = []
        params = []
        
        if limit_amount is not None:
            updates.append("limit_amount = %s")
            params.append(limit_amount)
        if alert_threshold is not None:
            updates.append("alert_threshold = %s")
            params.append(alert_threshold)
        
        if not updates:
            return False
        
        params.append(rule_id)
        query = f"UPDATE budget_rules SET {', '.join(updates)} WHERE rule_id = %s"
        execute_query(query, tuple(params))
        return True
    
    @staticmethod
    def delete(rule_id: int) -> bool:
        """
        Delete a budget rule
        
        Args:
            rule_id: ID of rule to delete
        
        Returns:
            True if deletion successful
        """
        query = "DELETE FROM budget_rules WHERE rule_id = %s"
        execute_query(query, (rule_id,))
        return True
    
    @staticmethod
    def delete_by_budget(budget_id: int) -> bool:
        """
        Delete all rules for a specific budget
        
        Args:
            budget_id: ID of budget whose rules to delete
        
        Returns:
            True if deletion successful
        """
        query = "DELETE FROM budget_rules WHERE budget_id = %s"
        execute_query(query, (budget_id,))
        return True
    
    @staticmethod
    def count() -> int:
        """
        Count total number of budget rules
        
        Returns:
            Total budget rule count
        """
        query = "SELECT COUNT(*) as count FROM budget_rules"
        result = execute_query(query, fetch=True)
        return result[0]['count'] if result else 0
    
    @staticmethod
    def get_rules_with_spending(budget_id: int) -> List[Dict]:
        """
        Get budget rules with current spending amounts
        
        Args:
            budget_id: The budget's ID
        
        Returns:
            List of rules with spending information
        """
        query = """
            SELECT br.*, c.category_name, c.icon,
                   COALESCE(SUM(t.amount), 0) as total_spent,
                   br.limit_amount - COALESCE(SUM(t.amount), 0) as remaining,
                   (COALESCE(SUM(t.amount), 0) / br.limit_amount * 100) as percent_used
            FROM budget_rules br
            JOIN categories c ON br.category_id = c.category_id
            JOIN budgets b ON br.budget_id = b.budget_id
            LEFT JOIN transactions t ON c.category_id = t.category_id 
                AND t.user_id = b.user_id
                AND t.transaction_date BETWEEN b.start_date AND b.end_date
            WHERE br.budget_id = %s
            GROUP BY br.rule_id
            ORDER BY c.category_name
        """
        return execute_query(query, (budget_id,), fetch=True)
    
    def __repr__(self):
        return f"BudgetRule(id={self.rule_id}, budget={self.budget_id}, category={self.category_id})"
