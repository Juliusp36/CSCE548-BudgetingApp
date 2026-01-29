"""
Transaction Model - Data Access Layer
Handles all database operations for transactions table
"""

from typing import Optional, List, Dict
from datetime import datetime, date
from decimal import Decimal
from db_config import execute_query

class Transaction:
    """Transaction model representing individual spending entries"""
    
    def __init__(self, transaction_id: Optional[int] = None, user_id: int = 0,
                 category_id: int = 0, amount: Decimal = Decimal('0.00'),
                 transaction_date: Optional[date] = None, description: str = "",
                 payment_method: str = "", created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None):
        self.transaction_id = transaction_id
        self.user_id = user_id
        self.category_id = category_id
        self.amount = amount
        self.transaction_date = transaction_date
        self.description = description
        self.payment_method = payment_method
        self.created_at = created_at
        self.updated_at = updated_at
    
    @staticmethod
    def create(user_id: int, category_id: int, amount: float,
               transaction_date: str, description: str = "",
               payment_method: str = "") -> int:
        """
        Create a new transaction
        
        Args:
            user_id: ID of the user
            category_id: ID of the category
            amount: Transaction amount
            transaction_date: Date of transaction (YYYY-MM-DD)
            description: Transaction description
            payment_method: Payment method used
        
        Returns:
            ID of the newly created transaction
        """
        query = """
            INSERT INTO transactions (user_id, category_id, amount, transaction_date,
                                     description, payment_method)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        transaction_id = execute_query(query, (user_id, category_id, amount,
                                               transaction_date, description, payment_method))
        return transaction_id
    
    @staticmethod
    def get_by_id(transaction_id: int) -> Optional[Dict]:
        """
        Retrieve a transaction by ID
        
        Args:
            transaction_id: The transaction's ID
        
        Returns:
            Transaction data as dictionary or None if not found
        """
        query = """
            SELECT t.*, u.username, c.category_name
            FROM transactions t
            JOIN users u ON t.user_id = u.user_id
            JOIN categories c ON t.category_id = c.category_id
            WHERE t.transaction_id = %s
        """
        results = execute_query(query, (transaction_id,), fetch=True)
        return results[0] if results else None
    
    @staticmethod
    def get_by_user(user_id: int, limit: Optional[int] = None) -> List[Dict]:
        """
        Retrieve all transactions for a specific user
        
        Args:
            user_id: The user's ID
            limit: Optional limit on number of results
        
        Returns:
            List of transactions as dictionaries
        """
        query = """
            SELECT t.*, c.category_name, c.icon
            FROM transactions t
            JOIN categories c ON t.category_id = c.category_id
            WHERE t.user_id = %s
            ORDER BY t.transaction_date DESC, t.created_at DESC
        """
        if limit:
            query += f" LIMIT {limit}"
        
        return execute_query(query, (user_id,), fetch=True)
    
    @staticmethod
    def get_by_category(category_id: int, limit: Optional[int] = None) -> List[Dict]:
        """
        Retrieve all transactions for a specific category
        
        Args:
            category_id: The category's ID
            limit: Optional limit on number of results
        
        Returns:
            List of transactions as dictionaries
        """
        query = """
            SELECT t.*, u.username, c.category_name
            FROM transactions t
            JOIN users u ON t.user_id = u.user_id
            JOIN categories c ON t.category_id = c.category_id
            WHERE t.category_id = %s
            ORDER BY t.transaction_date DESC
        """
        if limit:
            query += f" LIMIT {limit}"
        
        return execute_query(query, (category_id,), fetch=True)
    
    @staticmethod
    def get_by_date_range(user_id: int, start_date: str, end_date: str) -> List[Dict]:
        """
        Retrieve transactions within a date range for a user
        
        Args:
            user_id: The user's ID
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
        
        Returns:
            List of transactions as dictionaries
        """
        query = """
            SELECT t.*, c.category_name, c.icon
            FROM transactions t
            JOIN categories c ON t.category_id = c.category_id
            WHERE t.user_id = %s AND t.transaction_date BETWEEN %s AND %s
            ORDER BY t.transaction_date DESC
        """
        return execute_query(query, (user_id, start_date, end_date), fetch=True)
    
    @staticmethod
    def get_all(limit: Optional[int] = None) -> List[Dict]:
        """
        Retrieve all transactions
        
        Args:
            limit: Optional limit on number of results
        
        Returns:
            List of all transactions as dictionaries
        """
        query = """
            SELECT t.*, u.username, c.category_name
            FROM transactions t
            JOIN users u ON t.user_id = u.user_id
            JOIN categories c ON t.category_id = c.category_id
            ORDER BY t.transaction_date DESC, t.created_at DESC
        """
        if limit:
            query += f" LIMIT {limit}"
        
        return execute_query(query, fetch=True)
    
    @staticmethod
    def update(transaction_id: int, category_id: Optional[int] = None,
               amount: Optional[float] = None, transaction_date: Optional[str] = None,
               description: Optional[str] = None, payment_method: Optional[str] = None) -> bool:
        """
        Update transaction information
        
        Args:
            transaction_id: ID of transaction to update
            category_id: New category ID (optional)
            amount: New amount (optional)
            transaction_date: New date (optional)
            description: New description (optional)
            payment_method: New payment method (optional)
        
        Returns:
            True if update successful
        """
        updates = []
        params = []
        
        if category_id is not None:
            updates.append("category_id = %s")
            params.append(category_id)
        if amount is not None:
            updates.append("amount = %s")
            params.append(amount)
        if transaction_date is not None:
            updates.append("transaction_date = %s")
            params.append(transaction_date)
        if description is not None:
            updates.append("description = %s")
            params.append(description)
        if payment_method is not None:
            updates.append("payment_method = %s")
            params.append(payment_method)
        
        if not updates:
            return False
        
        params.append(transaction_id)
        query = f"UPDATE transactions SET {', '.join(updates)} WHERE transaction_id = %s"
        execute_query(query, tuple(params))
        return True
    
    @staticmethod
    def delete(transaction_id: int) -> bool:
        """
        Delete a transaction
        
        Args:
            transaction_id: ID of transaction to delete
        
        Returns:
            True if deletion successful
        """
        query = "DELETE FROM transactions WHERE transaction_id = %s"
        execute_query(query, (transaction_id,))
        return True
    
    @staticmethod
    def count() -> int:
        """
        Count total number of transactions
        
        Returns:
            Total transaction count
        """
        query = "SELECT COUNT(*) as count FROM transactions"
        result = execute_query(query, fetch=True)
        return result[0]['count'] if result else 0
    
    @staticmethod
    def get_spending_by_category(user_id: int, start_date: str, end_date: str) -> List[Dict]:
        """
        Get total spending by category for a user within a date range
        
        Args:
            user_id: The user's ID
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
        
        Returns:
            List of categories with total spending
        """
        query = """
            SELECT c.category_name, c.icon, SUM(t.amount) as total_spent,
                   COUNT(t.transaction_id) as transaction_count
            FROM transactions t
            JOIN categories c ON t.category_id = c.category_id
            WHERE t.user_id = %s AND t.transaction_date BETWEEN %s AND %s
            GROUP BY c.category_id
            ORDER BY total_spent DESC
        """
        return execute_query(query, (user_id, start_date, end_date), fetch=True)
    
    @staticmethod
    def get_total_spending(user_id: int, start_date: str, end_date: str) -> Decimal:
        """
        Get total spending for a user within a date range
        
        Args:
            user_id: The user's ID
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
        
        Returns:
            Total spending amount
        """
        query = """
            SELECT COALESCE(SUM(amount), 0) as total
            FROM transactions
            WHERE user_id = %s AND transaction_date BETWEEN %s AND %s
        """
        result = execute_query(query, (user_id, start_date, end_date), fetch=True)
        return result[0]['total'] if result else Decimal('0.00')
    
    def __repr__(self):
        return f"Transaction(id={self.transaction_id}, amount=${self.amount}, date={self.transaction_date})"
