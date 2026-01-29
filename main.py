"""
Budget Tracker Console Application
Main console interface for interacting with the budget tracking system
"""

import sys
from datetime import datetime
from decimal import Decimal
from typing import Optional

from db_config import DatabaseConfig
from models import User, Category, Budget, BudgetRule, Transaction


class BudgetTrackerApp:
    """Console-based application for budget tracking"""
    
    def __init__(self):
        self.current_user_id: Optional[int] = None
        self.running = True
    
    def display_header(self):
        """Display application header"""
        print("\n" + "="*60)
        print(" "*15 + "BUDGET TRACKER APPLICATION")
        print("="*60 + "\n")
    
    def display_menu(self):
        """Display main menu"""
        print("\n--- MAIN MENU ---")
        print("1. View All Users")
        print("2. View All Categories")
        print("3. View All Budgets")
        print("4. View All Transactions")
        print("5. View Budget Details")
        print("6. View User Transactions")
        print("7. View Spending Summary")
        print("8. View Budget Rules with Spending")
        print("9. Create New Transaction")
        print("10. Database Statistics")
        print("0. Exit")
        print("-" * 40)
    
    def get_user_input(self, prompt: str) -> str:
        """Get input from user with prompt"""
        return input(f"{prompt}: ").strip()
    
    def pause(self):
        """Pause for user to read output"""
        input("\nPress Enter to continue...")
    
    def view_all_users(self):
        """Display all users"""
        print("\n" + "="*60)
        print("ALL USERS")
        print("="*60)
        
        try:
            users = User.get_all()
            if not users:
                print("No users found.")
                return
            
            print(f"\n{'ID':<5} {'Username':<20} {'Email':<30} {'Created':<20}")
            print("-" * 80)
            
            for user in users:
                created = user['created_at'].strftime('%Y-%m-%d %H:%M') if user['created_at'] else 'N/A'
                print(f"{user['user_id']:<5} {user['username']:<20} {user['email']:<30} {created:<20}")
            
            print(f"\nTotal Users: {len(users)}")
            
        except Exception as e:
            print(f"Error retrieving users: {e}")
    
    def view_all_categories(self):
        """Display all categories"""
        print("\n" + "="*60)
        print("ALL CATEGORIES")
        print("="*60)
        
        try:
            categories = Category.get_with_transaction_count()
            if not categories:
                print("No categories found.")
                return
            
            print(f"\n{'ID':<5} {'Icon':<6} {'Name':<20} {'Description':<30} {'Transactions':<12}")
            print("-" * 80)
            
            for cat in categories:
                icon = cat.get('icon', '')[:5] if cat.get('icon') else ''
                desc = (cat.get('description', '')[:28] + '..') if len(cat.get('description', '')) > 30 else cat.get('description', '')
                print(f"{cat['category_id']:<5} {icon:<6} {cat['category_name']:<20} {desc:<30} {cat['transaction_count']:<12}")
            
            print(f"\nTotal Categories: {len(categories)}")
            
        except Exception as e:
            print(f"Error retrieving categories: {e}")
    
    def view_all_budgets(self):
        """Display all budgets"""
        print("\n" + "="*60)
        print("ALL BUDGETS")
        print("="*60)
        
        try:
            budgets = Budget.get_all()
            if not budgets:
                print("No budgets found.")
                return
            
            print(f"\n{'ID':<5} {'User ID':<8} {'Name':<25} {'Type':<10} {'Amount':<12} {'Active':<8}")
            print("-" * 80)
            
            for budget in budgets:
                active = "Yes" if budget['is_active'] else "No"
                amount = f"${budget['total_amount']:,.2f}"
                name = (budget['budget_name'][:23] + '..') if len(budget['budget_name']) > 25 else budget['budget_name']
                print(f"{budget['budget_id']:<5} {budget['user_id']:<8} {name:<25} {budget['budget_type']:<10} {amount:<12} {active:<8}")
            
            print(f"\nTotal Budgets: {len(budgets)}")
            
        except Exception as e:
            print(f"Error retrieving budgets: {e}")
    
    def view_all_transactions(self):
        """Display all transactions (limited to most recent 50)"""
        print("\n" + "="*60)
        print("RECENT TRANSACTIONS (Last 50)")
        print("="*60)
        
        try:
            transactions = Transaction.get_all(limit=50)
            if not transactions:
                print("No transactions found.")
                return
            
            print(f"\n{'ID':<6} {'User':<15} {'Category':<15} {'Amount':<10} {'Date':<12} {'Description':<25}")
            print("-" * 90)
            
            for txn in transactions:
                amount = f"${txn['amount']:,.2f}"
                date_str = txn['transaction_date'].strftime('%Y-%m-%d') if txn['transaction_date'] else 'N/A'
                desc = (txn.get('description', '')[:23] + '..') if len(txn.get('description', '')) > 25 else txn.get('description', '')
                print(f"{txn['transaction_id']:<6} {txn['username']:<15} {txn['category_name']:<15} {amount:<10} {date_str:<12} {desc:<25}")
            
            print(f"\nShowing {len(transactions)} transactions")
            
        except Exception as e:
            print(f"Error retrieving transactions: {e}")
    
    def view_budget_details(self):
        """Display detailed information about a specific budget"""
        budget_id = self.get_user_input("Enter Budget ID")
        
        if not budget_id.isdigit():
            print("Invalid budget ID.")
            return
        
        try:
            budget = Budget.get_budget_summary(int(budget_id))
            if not budget:
                print(f"Budget with ID {budget_id} not found.")
                return
            
            print("\n" + "="*60)
            print("BUDGET DETAILS")
            print("="*60)
            
            print(f"\nBudget ID: {budget['budget_id']}")
            print(f"Budget Name: {budget['budget_name']}")
            print(f"Budget Type: {budget['budget_type']}")
            print(f"Total Amount: ${budget['total_amount']:,.2f}")
            print(f"Period: {budget['start_date']} to {budget['end_date']}")
            print(f"Active: {'Yes' if budget['is_active'] else 'No'}")
            print(f"\nOwner: {budget['username']} ({budget['email']})")
            print(f"Number of Rules: {budget['rule_count']}")
            
        except Exception as e:
            print(f"Error retrieving budget details: {e}")
    
    def view_user_transactions(self):
        """Display transactions for a specific user"""
        user_id = self.get_user_input("Enter User ID")
        
        if not user_id.isdigit():
            print("Invalid user ID.")
            return
        
        try:
            user = User.get_by_id(int(user_id))
            if not user:
                print(f"User with ID {user_id} not found.")
                return
            
            transactions = Transaction.get_by_user(int(user_id), limit=50)
            
            print("\n" + "="*60)
            print(f"TRANSACTIONS FOR {user['username']}")
            print("="*60)
            
            if not transactions:
                print("No transactions found for this user.")
                return
            
            print(f"\n{'ID':<6} {'Category':<15} {'Amount':<10} {'Date':<12} {'Description':<30}")
            print("-" * 80)
            
            total = Decimal('0.00')
            for txn in transactions:
                amount = f"${txn['amount']:,.2f}"
                total += Decimal(str(txn['amount']))
                date_str = txn['transaction_date'].strftime('%Y-%m-%d') if txn['transaction_date'] else 'N/A'
                desc = (txn.get('description', '')[:28] + '..') if len(txn.get('description', '')) > 30 else txn.get('description', '')
                print(f"{txn['transaction_id']:<6} {txn['category_name']:<15} {amount:<10} {date_str:<12} {desc:<30}")
            
            print("-" * 80)
            print(f"Total Spending: ${total:,.2f}")
            print(f"Number of Transactions: {len(transactions)}")
            
        except Exception as e:
            print(f"Error retrieving user transactions: {e}")
    
    def view_spending_summary(self):
        """Display spending summary by category for a user"""
        user_id = self.get_user_input("Enter User ID")
        start_date = self.get_user_input("Enter Start Date (YYYY-MM-DD)")
        end_date = self.get_user_input("Enter End Date (YYYY-MM-DD)")
        
        if not user_id.isdigit():
            print("Invalid user ID.")
            return
        
        try:
            user = User.get_by_id(int(user_id))
            if not user:
                print(f"User with ID {user_id} not found.")
                return
            
            summary = Transaction.get_spending_by_category(int(user_id), start_date, end_date)
            total = Transaction.get_total_spending(int(user_id), start_date, end_date)
            
            print("\n" + "="*60)
            print(f"SPENDING SUMMARY FOR {user['username']}")
            print(f"Period: {start_date} to {end_date}")
            print("="*60)
            
            if not summary:
                print("No transactions found for this period.")
                return
            
            print(f"\n{'Category':<20} {'Icon':<6} {'Transactions':<15} {'Total Spent':<15}")
            print("-" * 60)
            
            for item in summary:
                icon = item.get('icon', '')[:5] if item.get('icon') else ''
                total_spent = f"${item['total_spent']:,.2f}"
                print(f"{item['category_name']:<20} {icon:<6} {item['transaction_count']:<15} {total_spent:<15}")
            
            print("-" * 60)
            print(f"TOTAL SPENDING: ${total:,.2f}")
            
        except Exception as e:
            print(f"Error retrieving spending summary: {e}")
    
    def view_budget_rules_with_spending(self):
        """Display budget rules with current spending"""
        budget_id = self.get_user_input("Enter Budget ID")
        
        if not budget_id.isdigit():
            print("Invalid budget ID.")
            return
        
        try:
            budget = Budget.get_by_id(int(budget_id))
            if not budget:
                print(f"Budget with ID {budget_id} not found.")
                return
            
            rules = BudgetRule.get_rules_with_spending(int(budget_id))
            
            print("\n" + "="*60)
            print(f"BUDGET RULES AND SPENDING")
            print(f"Budget: {budget['budget_name']}")
            print("="*60)
            
            if not rules:
                print("No rules found for this budget.")
                return
            
            print(f"\n{'Category':<15} {'Limit':<12} {'Spent':<12} {'Remaining':<12} {'% Used':<10}")
            print("-" * 70)
            
            for rule in rules:
                limit = f"${rule['limit_amount']:,.2f}"
                spent = f"${rule['total_spent']:,.2f}"
                remaining = f"${rule['remaining']:,.2f}"
                percent = f"{rule['percent_used']:.1f}%"
                print(f"{rule['category_name']:<15} {limit:<12} {spent:<12} {remaining:<12} {percent:<10}")
            
        except Exception as e:
            print(f"Error retrieving budget rules: {e}")
    
    def create_transaction(self):
        """Create a new transaction"""
        print("\n" + "="*60)
        print("CREATE NEW TRANSACTION")
        print("="*60)
        
        try:
            user_id = self.get_user_input("Enter User ID")
            if not user_id.isdigit():
                print("Invalid user ID.")
                return
            
            # Verify user exists
            user = User.get_by_id(int(user_id))
            if not user:
                print(f"User with ID {user_id} not found.")
                return
            
            # Show categories
            print("\nAvailable Categories:")
            categories = Category.get_all()
            for cat in categories[:10]:  # Show first 10
                print(f"  {cat['category_id']}: {cat['category_name']}")
            
            category_id = self.get_user_input("Enter Category ID")
            if not category_id.isdigit():
                print("Invalid category ID.")
                return
            
            amount = self.get_user_input("Enter Amount (e.g., 45.67)")
            try:
                amount_float = float(amount)
                if amount_float <= 0:
                    print("Amount must be positive.")
                    return
            except ValueError:
                print("Invalid amount format.")
                return
            
            date = self.get_user_input("Enter Date (YYYY-MM-DD)")
            description = self.get_user_input("Enter Description")
            payment_method = self.get_user_input("Enter Payment Method")
            
            # Create transaction
            txn_id = Transaction.create(
                int(user_id), int(category_id), amount_float,
                date, description, payment_method
            )
            
            print(f"\n✓ Transaction created successfully! ID: {txn_id}")
            
        except Exception as e:
            print(f"Error creating transaction: {e}")
    
    def show_statistics(self):
        """Display database statistics"""
        print("\n" + "="*60)
        print("DATABASE STATISTICS")
        print("="*60)
        
        try:
            print(f"\nTotal Users: {User.count()}")
            print(f"Total Categories: {Category.count()}")
            print(f"Total Budgets: {Budget.count()}")
            print(f"Total Budget Rules: {BudgetRule.count()}")
            print(f"Total Transactions: {Transaction.count()}")
            
            # Active budgets
            active_budgets = Budget.get_active_budgets()
            print(f"\nActive Budgets: {len(active_budgets)}")
            
        except Exception as e:
            print(f"Error retrieving statistics: {e}")
    
    def run(self):
        """Main application loop"""
        try:
            # Initialize database connection pool
            DatabaseConfig.initialize_pool()
            
            self.display_header()
            print("Welcome to Budget Tracker!")
            print("Database connected successfully.")
            
            while self.running:
                self.display_menu()
                choice = self.get_user_input("Enter your choice")
                
                if choice == '1':
                    self.view_all_users()
                    self.pause()
                elif choice == '2':
                    self.view_all_categories()
                    self.pause()
                elif choice == '3':
                    self.view_all_budgets()
                    self.pause()
                elif choice == '4':
                    self.view_all_transactions()
                    self.pause()
                elif choice == '5':
                    self.view_budget_details()
                    self.pause()
                elif choice == '6':
                    self.view_user_transactions()
                    self.pause()
                elif choice == '7':
                    self.view_spending_summary()
                    self.pause()
                elif choice == '8':
                    self.view_budget_rules_with_spending()
                    self.pause()
                elif choice == '9':
                    self.create_transaction()
                    self.pause()
                elif choice == '10':
                    self.show_statistics()
                    self.pause()
                elif choice == '0':
                    print("\nThank you for using Budget Tracker!")
                    self.running = False
                else:
                    print("\nInvalid choice. Please try again.")
                    self.pause()
            
        except KeyboardInterrupt:
            print("\n\nApplication interrupted by user.")
        except Exception as e:
            print(f"\nFatal error: {e}")
        finally:
            DatabaseConfig.close_pool()
            print("Goodbye!")


if __name__ == "__main__":
    app = BudgetTrackerApp()
    app.run()
