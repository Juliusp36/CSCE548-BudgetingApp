"""
User Model - Data Access Layer
Handles all database operations for users table
"""

from typing import Optional, List, Dict
from datetime import datetime
from db_config import execute_query

class User:
    """User model representing a user in the budget tracker"""
    
    def __init__(self, user_id: Optional[int] = None, username: str = "", 
                 email: str = "", password_hash: str = "",
                 created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.created_at = created_at
        self.updated_at = updated_at
    
    @staticmethod
    def create(username: str, email: str, password_hash: str) -> int:
        """
        Create a new user
        
        Args:
            username: Unique username
            email: User's email address
            password_hash: Hashed password
        
        Returns:
            ID of the newly created user
        """
        query = """
            INSERT INTO users (username, email, password_hash)
            VALUES (%s, %s, %s)
        """
        user_id = execute_query(query, (username, email, password_hash))
        return user_id
    
    @staticmethod
    def get_by_id(user_id: int) -> Optional[Dict]:
        """
        Retrieve a user by ID
        
        Args:
            user_id: The user's ID
        
        Returns:
            User data as dictionary or None if not found
        """
        query = "SELECT * FROM users WHERE user_id = %s"
        results = execute_query(query, (user_id,), fetch=True)
        return results[0] if results else None
    
    @staticmethod
    def get_by_username(username: str) -> Optional[Dict]:
        """
        Retrieve a user by username
        
        Args:
            username: The username to search for
        
        Returns:
            User data as dictionary or None if not found
        """
        query = "SELECT * FROM users WHERE username = %s"
        results = execute_query(query, (username,), fetch=True)
        return results[0] if results else None
    
    @staticmethod
    def get_by_email(email: str) -> Optional[Dict]:
        """
        Retrieve a user by email
        
        Args:
            email: The email to search for
        
        Returns:
            User data as dictionary or None if not found
        """
        query = "SELECT * FROM users WHERE email = %s"
        results = execute_query(query, (email,), fetch=True)
        return results[0] if results else None
    
    @staticmethod
    def get_all() -> List[Dict]:
        """
        Retrieve all users
        
        Returns:
            List of all users as dictionaries
        """
        query = "SELECT * FROM users ORDER BY created_at DESC"
        return execute_query(query, fetch=True)
    
    @staticmethod
    def update(user_id: int, username: Optional[str] = None, 
               email: Optional[str] = None, password_hash: Optional[str] = None) -> bool:
        """
        Update user information
        
        Args:
            user_id: ID of user to update
            username: New username (optional)
            email: New email (optional)
            password_hash: New password hash (optional)
        
        Returns:
            True if update successful
        """
        updates = []
        params = []
        
        if username is not None:
            updates.append("username = %s")
            params.append(username)
        if email is not None:
            updates.append("email = %s")
            params.append(email)
        if password_hash is not None:
            updates.append("password_hash = %s")
            params.append(password_hash)
        
        if not updates:
            return False
        
        params.append(user_id)
        query = f"UPDATE users SET {', '.join(updates)} WHERE user_id = %s"
        execute_query(query, tuple(params))
        return True
    
    @staticmethod
    def delete(user_id: int) -> bool:
        """
        Delete a user (will cascade to related records)
        
        Args:
            user_id: ID of user to delete
        
        Returns:
            True if deletion successful
        """
        query = "DELETE FROM users WHERE user_id = %s"
        execute_query(query, (user_id,))
        return True
    
    @staticmethod
    def count() -> int:
        """
        Count total number of users
        
        Returns:
            Total user count
        """
        query = "SELECT COUNT(*) as count FROM users"
        result = execute_query(query, fetch=True)
        return result[0]['count'] if result else 0
    
    def __repr__(self):
        return f"User(id={self.user_id}, username='{self.username}', email='{self.email}')"
