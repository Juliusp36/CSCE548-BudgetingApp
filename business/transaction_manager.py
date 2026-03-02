"""
Transaction Manager - Business Layer
Handles transaction-related business logic and validation
"""

from typing import Optional, List, Dict
from datetime import datetime, date
from decimal import Decimal
from models.transaction import Transaction
from models.user import User
from models.category import Category
from models.budget import Budget


class TransactionManager:
    """
    Business layer for Transaction operations
    Implements business rules and validation before calling data layer
    """
    
    @staticmethod
    def _validate_date(transaction_date: str) -> bool:
        """Validate that date is not in the future"""
        try:
            txn_date = datetime.strptime(transaction_date, '%Y-%m-%d').date()
            return txn_date <= date.today()
        except ValueError:
            return False
    
    @staticmethod
    def save(transaction_id: int, user_id: int, category_id: int, amount: float,
             transaction_date: str, description: str = "", 
             payment_method: str = "") -> Dict:
        """
        Save transaction (insert if ID is 0, update if ID exists)
        
        Business Rules:
        - Amount must be positive
        - Date cannot be in the future
        - User and category must exist
        - Warn if transaction pushes spending over budget limit
        
        Args:
            transaction_id: Transaction ID (0 for new transaction)
            user_id: User who made the transaction
            category_id: Category of the transaction
            amount: Transaction amount
            transaction_date: Date of transaction (YYYY-MM-DD)
            description: Transaction description
            payment_method: Payment method used
        
        Returns:
            Dict with success status, transaction_id, and any warnings
        """
        try:
            transaction_id = int(transaction_id)
            user_id = int(user_id)
            category_id = int(category_id)
            amount = float(amount)

            
            # Verify user exists
            user = User.get_by_id(user_id)
            if not user:
                return {"success": False, "error": "User not found"}
            
            # Verify category exists
            category = Category.get_by_id(category_id)
            if not category:
                return {"success": False, "error": "Category not found"}
            
            # Validate amount
            if amount <= 0:
                return {"success": False, "error": "Amount must be positive"}
            
            # Validate date
            if not TransactionManager._validate_date(transaction_date):
                return {"success": False, "error": "Transaction date cannot be in the future"}
            
            # If ID is 0, this is a new record (INSERT)
            if transaction_id == 0:
                new_id = Transaction.create(user_id, category_id, amount, 
                                           transaction_date, description, payment_method)
                
                # Check budget warnings
                warnings = TransactionManager._check_budget_warnings(user_id, category_id, 
                                                                    transaction_date)
                
                return {
                    "success": True,
                    "transaction_id": new_id,
                    "message": "Transaction created successfully",
                    "warnings": warnings
                }
            
            # If ID exists, this is an update (UPDATE)
            else:
                # Verify transaction exists
                existing = Transaction.get_by_id(transaction_id)
                if not existing:
                    return {"success": False, "error": "Transaction not found"}
                
                Transaction.update(transaction_id, category_id=category_id, amount=amount,
                                 transaction_date=transaction_date, description=description,
                                 payment_method=payment_method)
                
                # Check budget warnings
                warnings = TransactionManager._check_budget_warnings(user_id, category_id, 
                                                                    transaction_date)
                
                return {
                    "success": True,
                    "transaction_id": transaction_id,
                    "message": "Transaction updated successfully",
                    "warnings": warnings
                }
                
        except Exception as e:
            return {"success": False, "error": f"Database error: {str(e)}"}
    
    @staticmethod
    def _check_budget_warnings(user_id: int, category_id: int, 
                               transaction_date: str) -> List[str]:
        """
        Check if transaction pushes spending over budget limits
        
        Args:
            user_id: User ID
            category_id: Category ID
            transaction_date: Transaction date
        
        Returns:
            List of warning messages
        """
        warnings = []
        
        try:
            # Get user's active budget
            active_budgets = Budget.get_active_budgets(user_id)
            if not active_budgets:
                return warnings
            
            budget = active_budgets[0]
            
            # Check if transaction date is within budget period
            txn_date = datetime.strptime(transaction_date, '%Y-%m-%d').date()
            budget_start = budget['start_date']
            budget_end = budget['end_date']
            if isinstance(budget_start, str):
                budget_start = datetime.strptime(budget_start, '%Y-%m-%d').date()

            if isinstance(budget_end, str):
                budget_end = datetime.strptime(budget_end, '%Y-%m-%d').date()
            if not (budget_start <= txn_date <= budget_end):
                warnings.append(f"Transaction date is outside active budget period ({budget_start} to {budget_end})")
                return warnings
            
            # Get spending for this category
            category = Category.get_by_id(category_id)
            spending = Transaction.get_spending_by_category(
                user_id, 
                str(budget_start), 
                str(budget_end)
            )
            
            # Find spending for this specific category
            category_spending = next(
                (s for s in spending if s['category_name'] == category['category_name']), 
                None
            )
            
            if category_spending:
                # Get budget rule for this category
                from models.budget_rule import BudgetRule
                rule = BudgetRule.get_by_budget_and_category(budget['budget_id'], category_id)
                
                if rule:
                    spent = float(category_spending['total_spent'])
                    limit = float(rule['limit_amount'])
                    percent_used = (spent / limit) * 100
                    
                    if percent_used >= 100:
                        warnings.append(
                            f"⚠️ OVER BUDGET: {category['category_name']} "
                            f"(${spent:.2f} / ${limit:.2f})"
                        )
                    elif percent_used >= float(rule['alert_threshold']):
                        warnings.append(
                            f"⚠️ Approaching limit: {category['category_name']} "
                            f"({percent_used:.1f}% of ${limit:.2f})"
                        )
            
        except Exception as e:
            print(f"Error checking budget warnings: {e}")
        
        return warnings
    
    @staticmethod
    def get_by_id(transaction_id: int) -> Optional[Dict]:
        """
        Get transaction by ID
        
        Args:
            transaction_id: Transaction ID to retrieve
        
        Returns:
            Transaction data dictionary or None if not found
        """
        try:
            return Transaction.get_by_id(transaction_id)
        except Exception as e:
            print(f"Error retrieving transaction: {e}")
            return None
    
    @staticmethod
    def get_all(limit: Optional[int] = None) -> List[Dict]:
        """
        Get all transactions
        
        Args:
            limit: Optional limit on results
        
        Returns:
            List of all transactions
        """
        try:
            return Transaction.get_all(limit)
        except Exception as e:
            print(f"Error retrieving transactions: {e}")
            return []
    
    @staticmethod
    def delete(transaction_id: int) -> Dict:
        """
        Delete transaction
        
        Business Rules:
        - Transaction must exist
        
        Args:
            transaction_id: Transaction ID to delete
        
        Returns:
            Dict with success status and message
        """
        try:
            # Verify transaction exists
            transaction = Transaction.get_by_id(transaction_id)
            if not transaction:
                return {"success": False, "error": "Transaction not found"}
            
            # Delete transaction
            Transaction.delete(transaction_id)
            return {
                "success": True,
                "message": "Transaction deleted successfully"
            }
            
        except Exception as e:
            return {"success": False, "error": f"Delete error: {str(e)}"}
    
    @staticmethod
    def get_by_user(user_id: int, limit: Optional[int] = None) -> List[Dict]:
        """
        Get transactions for a specific user (additional business method)
        
        Args:
            user_id: User ID
            limit: Optional limit
        
        Returns:
            List of user's transactions
        """
        try:
            return Transaction.get_by_user(user_id, limit)
        except Exception as e:
            print(f"Error retrieving transactions: {e}")
            return []
    
    @staticmethod
    def get_spending_summary(user_id: int, start_date: str, end_date: str) -> Dict:
        """
        Get spending summary for a user (additional business method)
        
        Args:
            user_id: User ID
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
        
        Returns:
            Dict with spending breakdown by category and total
        """
        try:
            by_category = Transaction.get_spending_by_category(user_id, start_date, end_date)
            total = Transaction.get_total_spending(user_id, start_date, end_date)
            
            return {
                "success": True,
                "by_category": by_category,
                "total": float(total),
                "period": f"{start_date} to {end_date}"
            }
        except Exception as e:
            return {"success": False, "error": f"Error: {str(e)}"}
    
    @staticmethod
    def count() -> int:
        """
        Get total transaction count (additional business method)
        
        Returns:
            Total number of transactions
        """
        try:
            return Transaction.count()
        except Exception as e:
            print(f"Error counting transactions: {e}")
            return 0
