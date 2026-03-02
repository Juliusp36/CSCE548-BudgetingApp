"""
Budget Manager - Business Layer
Handles budget-related business logic and validation
"""

from typing import Optional, List, Dict
from datetime import datetime, date
from models.budget import Budget
from models.user import User


class BudgetManager:
    """
    Business layer for Budget operations
    Implements business rules and validation before calling data layer
    """
    
    @staticmethod
    def _validate_dates(start_date: str, end_date: str) -> bool:
        """Validate that end date is after start date"""
        try:
        # Handle both string and date objects
            if isinstance(start_date, str):
                start = datetime.strptime(start_date, '%Y-%m-%d').date()
            else:
                start = start_date
            
            if isinstance(end_date, str):
                end = datetime.strptime(end_date, '%Y-%m-%d').date()
            else:
                end = end_date
            
            return end >= start
        except(ValueError, TypeError) as e:
            print(f"Date validation error: {e}")
            return False
        
        
    @staticmethod
    def save(budget_id: int, user_id: int, budget_name: str, budget_type: str,
             total_amount: float, start_date: str, end_date: str, 
             is_active: bool = True) -> Dict:
        """
        Save budget (insert if ID is 0, update if ID exists)
        
        Business Rules:
        - User can only have ONE active budget at a time
        - End date must be after start date
        - Total amount must be positive
        - Budget name must be unique per user
        - Budget type must be: strict, moderate, or custom
        
        Args:
            budget_id: Budget ID (0 for new budget)
            user_id: User who owns the budget
            budget_name: Name of the budget
            budget_type: Type: 'strict', 'moderate', or 'custom'
            total_amount: Total budget amount
            start_date: Budget start date (YYYY-MM-DD)
            end_date: Budget end date (YYYY-MM-DD)
            is_active: Whether budget is active
        
        Returns:
            Dict with success status and budget_id or error message
        """
        try:
            # Verify user exists
            user = User.get_by_id(user_id)
            if not user:
                return {"success": False, "error": "User not found"}
            
            # Validate budget type
            valid_types = ['strict', 'moderate', 'custom']
            if budget_type not in valid_types:
                return {
                    "success": False,
                    "error": f"Budget type must be one of: {', '.join(valid_types)}"
                }
            
            try: 
                total_amount = float(total_amount)
            except (ValueError, TypeError):
                 return {"success": False, "error": "Total amount must be a valid number"}
            # Validate total amount
            if total_amount <= 0:
                return {"success": False, "error": "Total amount must be positive"}
            
            # Validate dates
            if not BudgetManager._validate_dates(start_date, end_date):
                return {"success": False, "error": "End date must be on or after start date"}
            
            # Business Rule: Only one active budget per user
            if is_active:
                active_budgets = Budget.get_active_budgets(user_id)
                # Filter out the current budget if updating
                active_budgets = [b for b in active_budgets if b['budget_id'] != budget_id]
                if active_budgets:
                    return {
                        "success": False,
                        "error": f"User already has an active budget: '{active_budgets[0]['budget_name']}'"
                    }
            
            # Check for duplicate budget name for this user
            user_budgets = Budget.get_by_user(user_id)
            duplicate = [b for b in user_budgets 
                        if b['budget_name'] == budget_name and b['budget_id'] != budget_id]
            if duplicate:
                return {"success": False, "error": "Budget name already exists for this user"}
            
            # If ID is 0, this is a new record (INSERT)
            if budget_id == 0:
    # Ensure dates are strings in correct format
                start = start_date if isinstance(start_date, str) else start_date.strftime('%Y-%m-%d')
                end = end_date if isinstance(end_date, str) else end_date.strftime('%Y-%m-%d')

                new_id = Budget.create(user_id, budget_name, budget_type, 
                          total_amount, start, end, is_active)
                
                return {
                    "success": True,
                    "budget_id": new_id,
                    "message": "Budget created successfully"
                }
            
            # If ID exists, this is an update (UPDATE)
            else:
                # Verify budget exists
                existing = Budget.get_by_id(budget_id)
                if not existing:
                    return {"success": False, "error": "Budget not found"}
                
                start = start_date if isinstance(start_date, str) else start_date.strftime('%Y-%m-%d')
                end = end_date if isinstance(end_date, str) else end_date.strftime('%Y-%m-%d')
                
                Budget.update(budget_id, budget_name=budget_name, budget_type=budget_type,
                            total_amount=total_amount, start_date=start,  
                            end_date=end, is_active=is_active)
                return {
                    "success": True,
                    "budget_id": budget_id,
                    "message": "Budget updated successfully"
                }
                
        except Exception as e:
            return {"success": False, "error": f"Database error: {str(e)}"}
    
    @staticmethod
    def get_by_id(budget_id: int) -> Optional[Dict]:
        """
        Get budget by ID
        
        Args:
            budget_id: Budget ID to retrieve
        
        Returns:
            Budget data dictionary or None if not found
        """
        try:
            return Budget.get_by_id(budget_id)
        except Exception as e:
            print(f"Error retrieving budget: {e}")
            return None
    
    @staticmethod
    def get_all() -> List[Dict]:
        """
        Get all budgets
        
        Returns:
            List of all budgets
        """
        try:
            return Budget.get_all()
        except Exception as e:
            print(f"Error retrieving budgets: {e}")
            return []
    
    @staticmethod
    def delete(budget_id: int) -> Dict:
        """
        Delete budget
        
        Business Rules:
        - Budget must exist
        - Will cascade delete all budget rules
        
        Args:
            budget_id: Budget ID to delete
        
        Returns:
            Dict with success status and message
        """
        try:
            # Verify budget exists
            budget = Budget.get_by_id(budget_id)
            if not budget:
                return {"success": False, "error": "Budget not found"}
            
            # Delete budget (cascades to budget rules)
            Budget.delete(budget_id)
            return {
                "success": True,
                "message": f"Budget '{budget['budget_name']}' deleted successfully"
            }
            
        except Exception as e:
            return {"success": False, "error": f"Delete error: {str(e)}"}
    
    @staticmethod
    def get_by_user(user_id: int) -> List[Dict]:
        """
        Get all budgets for a specific user (additional business method)
        
        Args:
            user_id: User ID
        
        Returns:
            List of user's budgets
        """
        try:
            return Budget.get_by_user(user_id)
        except Exception as e:
            print(f"Error retrieving budgets: {e}")
            return []
    
    @staticmethod
    def get_active_budgets(user_id: Optional[int] = None) -> List[Dict]:
        """
        Get active budgets (additional business method)
        
        Args:
            user_id: Optional user ID to filter by
        
        Returns:
            List of active budgets
        """
        try:
            return Budget.get_active_budgets(user_id)
        except Exception as e:
            print(f"Error retrieving active budgets: {e}")
            return []
    
    @staticmethod
    def deactivate(budget_id: int) -> Dict:
        """
        Deactivate a budget (soft delete - additional business method)
        
        Args:
            budget_id: Budget ID to deactivate
        
        Returns:
            Dict with success status
        """
        try:
            budget = Budget.get_by_id(budget_id)
            if not budget:
                return {"success": False, "error": "Budget not found"}
            
            Budget.deactivate(budget_id)
            return {
                "success": True,
                "message": f"Budget '{budget['budget_name']}' deactivated successfully"
            }
        except Exception as e:
            return {"success": False, "error": f"Error: {str(e)}"}
    
    @staticmethod
    def count() -> int:
        """
        Get total budget count (additional business method)
        
        Returns:
            Total number of budgets
        """
        try:
            return Budget.count()
        except Exception as e:
            print(f"Error counting budgets: {e}")
            return 0
