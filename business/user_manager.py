"""
User Manager - Business Layer
Handles user-related business logic and validation
"""

import re
from typing import Optional, List, Dict
from models.user import User


class UserManager:
    """
    Business layer for User operations
    Implements business rules and validation before calling data layer
    """
    
    @staticmethod
    def _validate_email(email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def _validate_password(password: str) -> bool:
        """
        Validate password strength
        Rules: At least 8 characters, contains letter and number
        """
        if len(password) < 8:
            return False
        has_letter = any(c.isalpha() for c in password)
        has_number = any(c.isdigit() for c in password)
        return has_letter and has_number
    
    @staticmethod
    def save(user_id: int, username: str, email: str, password_hash: str) -> Dict:
        """
        Save user (insert if ID is 0, update if ID exists)
        
        Business Rules:
        - Email must be unique and valid format
        - Username must be unique
        - Password must meet minimum requirements
        
        Args:
            user_id: User ID (0 for new user)
            username: Unique username
            email: Valid email address
            password_hash: Hashed password
        
        Returns:
            Dict with success status and user_id or error message
        """
        try:
            # Validate email format
            if not UserManager._validate_email(email):
                return {"success": False, "error": "Invalid email format"}
            
            # Validate password (if creating new user)
            if user_id == 0:
                if not UserManager._validate_password(password_hash):
                    return {"success": False, "error": "Password must be at least 8 characters with letters and numbers"}
            
            # Check for duplicate username (for new users or username changes)
            existing_user = User.get_by_username(username)
            if existing_user and existing_user['user_id'] != user_id:
                return {"success": False, "error": "Username already exists"}
            
            # Check for duplicate email (for new users or email changes)
            existing_email = User.get_by_email(email)
            if existing_email and existing_email['user_id'] != user_id:
                return {"success": False, "error": "Email already exists"}
            
            # If ID is 0, this is a new record (INSERT)
            if user_id == 0:
                new_id = User.create(username, email, password_hash)
                return {
                    "success": True,
                    "user_id": new_id,
                    "message": "User created successfully"
                }
            
            # If ID exists, this is an update (UPDATE)
            else:
                # Verify user exists
                existing = User.get_by_id(user_id)
                if not existing:
                    return {"success": False, "error": "User not found"}
                
                User.update(user_id, username=username, email=email, password_hash=password_hash)
                return {
                    "success": True,
                    "user_id": user_id,
                    "message": "User updated successfully"
                }
                
        except Exception as e:
            return {"success": False, "error": f"Database error: {str(e)}"}
    
    @staticmethod
    def get_by_id(user_id: int) -> Optional[Dict]:
        """
        Get user by ID
        
        Args:
            user_id: User ID to retrieve
        
        Returns:
            User data dictionary or None if not found
        """
        try:
            return User.get_by_id(user_id)
        except Exception as e:
            print(f"Error retrieving user: {e}")
            return None
    
    @staticmethod
    def get_all() -> List[Dict]:
        """
        Get all users
        
        Returns:
            List of all users
        """
        try:
            return User.get_all()
        except Exception as e:
            print(f"Error retrieving users: {e}")
            return []
    
    @staticmethod
    def delete(user_id: int) -> Dict:
        """
        Delete user
        
        Business Rules:
        - User must exist
        - Will cascade delete all user's budgets and transactions
        
        Args:
            user_id: User ID to delete
        
        Returns:
            Dict with success status and message
        """
        try:
            # Verify user exists
            user = User.get_by_id(user_id)
            if not user:
                return {"success": False, "error": "User not found"}
            
            # Delete user (cascades to budgets and transactions)
            User.delete(user_id)
            return {
                "success": True,
                "message": f"User {user['username']} deleted successfully"
            }
            
        except Exception as e:
            return {"success": False, "error": f"Delete error: {str(e)}"}
    
    @staticmethod
    def get_by_username(username: str) -> Optional[Dict]:
        """
        Get user by username (additional business method)
        
        Args:
            username: Username to search for
        
        Returns:
            User data or None
        """
        try:
            return User.get_by_username(username)
        except Exception as e:
            print(f"Error retrieving user: {e}")
            return None
    
    @staticmethod
    def count() -> int:
        """
        Get total user count (additional business method)
        
        Returns:
            Total number of users
        """
        try:
            return User.count()
        except Exception as e:
            print(f"Error counting users: {e}")
            return 0
