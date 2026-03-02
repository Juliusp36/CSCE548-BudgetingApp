"""
Budget Rule Manager - Business Layer
Handles budget rule-related business logic and validation
"""

from typing import Optional, List, Dict
from models.budget_rule import BudgetRule
from models.budget import Budget
from models.category import Category


class BudgetRuleManager:
    """
    Business layer for Budget Rule operations
    Implements business rules and validation before calling data layer
    """
    
    @staticmethod
    def save(rule_id: int, budget_id: int, category_id: int, 
             limit_amount: float, alert_threshold: float = 80.0) -> Dict:
        """
        Save budget rule (insert if ID is 0, update if ID exists)
        
        Business Rules:
        - Limit amount must be positive
        - Alert threshold must be between 0-100%
        - Cannot have duplicate rules (same budget + category)
        - Budget and category must exist
        
        Args:
            rule_id: Rule ID (0 for new rule)
            budget_id: Budget ID this rule belongs to
            category_id: Category ID this rule applies to
            limit_amount: Spending limit for this category
            alert_threshold: Alert percentage (0-100)
        
        Returns:
            Dict with success status and rule_id or error message
        """
        try:
            rule_id = int(rule_id)
            budget_id = int(budget_id)
            category_id = int(category_id)
            limit_amount = float(limit_amount)
            alert_threshold = float(alert_threshold)
            
            # Verify budget exists
            budget = Budget.get_by_id(budget_id)
            if not budget:
                return {"success": False, "error": "Budget not found"}
            
            # Verify category exists
            category = Category.get_by_id(category_id)
            if not category:
                return {"success": False, "error": "Category not found"}
            
            # Validate limit amount
            if limit_amount <= 0:
                return {"success": False, "error": "Limit amount must be positive"}
            
            # Validate alert threshold
            if not (0 <= alert_threshold <= 100):
                return {"success": False, "error": "Alert threshold must be between 0 and 100"}
            
            # Business Rule: Limit shouldn't exceed budget total
            budget_total = float(budget['total_amount'])

            if limit_amount > budget_total:
                return {
                    "success": False,
                   "error": f"Limit (${limit_amount:.2f}) exceeds budget total (${budget_total:.2f})"
                }
            
            # Check for duplicate budget-category combination
            existing_rule = BudgetRule.get_by_budget_and_category(budget_id, category_id)
            if existing_rule and existing_rule['rule_id'] != rule_id:
                return {
                    "success": False,
                    "error": f"Rule already exists for category '{category['category_name']}' in this budget"
                }
            
            # If ID is 0, this is a new record (INSERT)
            if rule_id == 0:
                new_id = BudgetRule.create(budget_id, category_id, limit_amount, alert_threshold)
                return {
                    "success": True,
                    "rule_id": new_id,
                    "message": "Budget rule created successfully"
                }
            
            # If ID exists, this is an update (UPDATE)
            else:
                # Verify rule exists
                existing = BudgetRule.get_by_id(rule_id)
                if not existing:
                    return {"success": False, "error": "Budget rule not found"}
                
                BudgetRule.update(rule_id, limit_amount=limit_amount, 
                                alert_threshold=alert_threshold)
                return {
                    "success": True,
                    "rule_id": rule_id,
                    "message": "Budget rule updated successfully"
                }
        except (ValueError, TypeError):
            return {"success": False, "error": "Invalid numeric input"}
                
        except Exception as e:
            return {"success": False, "error": f"Database error: {str(e)}"}
    
    @staticmethod
    def get_by_id(rule_id: int) -> Optional[Dict]:
        """
        Get budget rule by ID
        
        Args:
            rule_id: Rule ID to retrieve
        
        Returns:
            Budget rule data dictionary or None if not found
        """
        try:
            return BudgetRule.get_by_id(rule_id)
        except Exception as e:
            print(f"Error retrieving budget rule: {e}")
            return None
    
    @staticmethod
    def get_all() -> List[Dict]:
        """
        Get all budget rules
        
        Returns:
            List of all budget rules
        """
        try:
            return BudgetRule.get_all()
        except Exception as e:
            print(f"Error retrieving budget rules: {e}")
            return []
    
    @staticmethod
    def delete(rule_id: int) -> Dict:
        """
        Delete budget rule
        
        Business Rules:
        - Rule must exist
        
        Args:
            rule_id: Rule ID to delete
        
        Returns:
            Dict with success status and message
        """
        try:
            # Verify rule exists
            rule = BudgetRule.get_by_id(rule_id)
            if not rule:
                return {"success": False, "error": "Budget rule not found"}
            
            # Delete rule
            BudgetRule.delete(rule_id)
            return {
                "success": True,
                "message": "Budget rule deleted successfully"
            }
            
        except Exception as e:
            return {"success": False, "error": f"Delete error: {str(e)}"}
    
    @staticmethod
    def get_by_budget(budget_id: int) -> List[Dict]:
        """
        Get all rules for a specific budget (additional business method)
        
        Args:
            budget_id: Budget ID
        
        Returns:
            List of budget rules
        """
        try:
            return BudgetRule.get_by_budget(budget_id)
        except Exception as e:
            print(f"Error retrieving budget rules: {e}")
            return []
    
    @staticmethod
    def get_rules_with_spending(budget_id: int) -> List[Dict]:
        """
        Get budget rules with current spending (additional business method)
        
        Args:
            budget_id: Budget ID
        
        Returns:
            List of rules with spending information
        """
        try:
            return BudgetRule.get_rules_with_spending(budget_id)
        except Exception as e:
            print(f"Error retrieving rules with spending: {e}")
            return []
    
    @staticmethod
    def check_budget_alerts(budget_id: int) -> List[Dict]:
        """
        Check which categories are approaching their limits (additional business method)
        
        Args:
            budget_id: Budget ID to check
        
        Returns:
            List of categories that have exceeded their alert threshold
        """
        try:
            rules_with_spending = BudgetRule.get_rules_with_spending(budget_id)
            alerts = []
            
            for rule in rules_with_spending:
                percent_used = float(rule['percent_used'])
                alert_threshold = float(rule['alert_threshold'])
                
                if percent_used >= alert_threshold:
                    alerts.append({
                        'category': rule['category_name'],
                        'limit': rule['limit_amount'],
                        'spent': rule['total_spent'],
                        'percent_used': percent_used,
                        'alert_threshold': alert_threshold,
                        'status': 'over_budget' if percent_used >= 100 else 'approaching_limit'
                    })
            
            return alerts
            
        except Exception as e:
            print(f"Error checking budget alerts: {e}")
            return []
    
    @staticmethod
    def count() -> int:
        """
        Get total budget rule count (additional business method)
        
        Returns:
            Total number of budget rules
        """
        try:
            return BudgetRule.count()
        except Exception as e:
            print(f"Error counting budget rules: {e}")
            return 0
