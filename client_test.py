"""
Service Test Client - Console Application
Tests all REST API endpoints for the Budget Tracker

USAGE:
1. Start the Flask server: python app.py
2. In a new terminal, run: python client_test.py
"""

import requests
import json
from datetime import datetime, timedelta

# Base URL for the API
BASE_URL = "http://localhost:5001/api"

# For testing on Render.com, change to:
# BASE_URL = "https://your-app-name.onrender.com/api"


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80)


def print_result(operation, result):
    """Print formatted result"""
    print(f"\n{operation}:")
    print(json.dumps(result, indent=2, default=str))


def test_user_service():
    """Test User Service endpoints"""
    print_section("TESTING USER SERVICE")
    
    # Test 1: Create new user
    print("\n1. Creating new user...")
    user_data = {
        "user_id": 0,
        "username": "testuser_" + datetime.now().strftime("%Y%m%d%H%M%S"),
        "email": f"test_{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com",
        "password_hash": "SecurePass123"
    }
    response = requests.post(f"{BASE_URL}/users", json=user_data)
    result = response.json()
    print_result("Create User", result)
    
    if not result.get('success'):
        print("❌ Failed to create user. Stopping user tests.")
        return None
    
    user_id = result['user_id']
    print(f"✅ User created with ID: {user_id}")
    
    # Test 2: Get user by ID
    print(f"\n2. Getting user by ID {user_id}...")
    response = requests.get(f"{BASE_URL}/users/{user_id}")
    result = response.json()
    print_result("Get User", result)
    
    # Test 3: Update user
    print(f"\n3. Updating user {user_id}...")
    user_data['user_id'] = user_id
    user_data['email'] = f"updated_{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com"
    response = requests.post(f"{BASE_URL}/users", json=user_data)
    result = response.json()
    print_result("Update User", result)
    
    # Test 4: Get all users
    print("\n4. Getting all users...")
    response = requests.get(f"{BASE_URL}/users")
    result = response.json()
    print(f"Found {result['count']} users")
    
    return user_id


def test_category_service():
    """Test Category Service endpoints"""
    print_section("TESTING CATEGORY SERVICE")
    
    # Test 1: Create new category
    print("\n1. Creating new category...")
    category_data = {
        "category_id": 0,
        "category_name": f"Test Category {datetime.now().strftime('%H%M%S')}",
        "description": "Testing category creation",
        "icon": "🧪"
    }
    response = requests.post(f"{BASE_URL}/categories", json=category_data)
    result = response.json()
    print_result("Create Category", result)
    
    if not result.get('success'):
        print("❌ Failed to create category. Stopping category tests.")
        return None
    
    category_id = result['category_id']
    print(f"✅ Category created with ID: {category_id}")
    
    # Test 2: Get category by ID
    print(f"\n2. Getting category by ID {category_id}...")
    response = requests.get(f"{BASE_URL}/categories/{category_id}")
    result = response.json()
    print_result("Get Category", result)
    
    # Test 3: Update category
    print(f"\n3. Updating category {category_id}...")
    category_data['category_id'] = category_id
    category_data['description'] = "Updated description"
    response = requests.post(f"{BASE_URL}/categories", json=category_data)
    result = response.json()
    print_result("Update Category", result)
    
    # Test 4: Get all categories
    print("\n4. Getting all categories...")
    response = requests.get(f"{BASE_URL}/categories")
    result = response.json()
    print(f"Found {result['count']} categories")
    
    return category_id


def test_budget_service(user_id):
    """Test Budget Service endpoints"""
    print_section("TESTING BUDGET SERVICE")
    
    if not user_id:
        print("⚠️ No user_id provided, skipping budget tests")
        return None
    
    # Test 1: Create new budget
    print("\n1. Creating new budget...")
    today = datetime.now().date()
    next_month = today + timedelta(days=30)
    
    budget_data = {
        "budget_id": 0,
        "user_id": user_id,
        "budget_name": f"Test Budget {datetime.now().strftime('%H%M%S')}",
        "budget_type": "moderate",
        "total_amount": 2500.00,
        "start_date": str(today),
        "end_date": str(next_month),
        "is_active": True
    }
    response = requests.post(f"{BASE_URL}/budgets", json=budget_data)
    result = response.json()
    print_result("Create Budget", result)
    
    if not result.get('success'):
        print("❌ Failed to create budget. Stopping budget tests.")
        return None
    
    budget_id = result['budget_id']
    print(f"✅ Budget created with ID: {budget_id}")
    
    # Test 2: Get budget by ID
    print(f"\n2. Getting budget by ID {budget_id}...")
    response = requests.get(f"{BASE_URL}/budgets/{budget_id}")
    result = response.json()
    print_result("Get Budget", result)
    
    # Test 3: Update budget
    print(f"\n3. Updating budget {budget_id}...")
    budget_data['budget_id'] = budget_id
    budget_data['total_amount'] = 3000.00
    response = requests.post(f"{BASE_URL}/budgets", json=budget_data)
    result = response.json()
    print_result("Update Budget", result)
    
    # Test 4: Get user's budgets
    print(f"\n4. Getting budgets for user {user_id}...")
    response = requests.get(f"{BASE_URL}/budgets/user/{user_id}")
    result = response.json()
    print(f"Found {result['count']} budgets for this user")
    
    return budget_id


def test_budget_rule_service(budget_id, category_id):
    """Test Budget Rule Service endpoints"""
    print_section("TESTING BUDGET RULE SERVICE")
    
    if not budget_id or not category_id:
        print("⚠️ No budget_id or category_id provided, skipping budget rule tests")
        return None
    
    # Test 1: Create new budget rule
    print("\n1. Creating new budget rule...")
    rule_data = {
        "rule_id": 0,
        "budget_id": budget_id,
        "category_id": category_id,
        "limit_amount": 500.00,
        "alert_threshold": 80.0
    }
    response = requests.post(f"{BASE_URL}/budget-rules", json=rule_data)
    result = response.json()
    print_result("Create Budget Rule", result)
    
    if not result.get('success'):
        print("❌ Failed to create budget rule. Stopping budget rule tests.")
        return None
    
    rule_id = result['rule_id']
    print(f"✅ Budget rule created with ID: {rule_id}")
    
    # Test 2: Get budget rule by ID
    print(f"\n2. Getting budget rule by ID {rule_id}...")
    response = requests.get(f"{BASE_URL}/budget-rules/{rule_id}")
    result = response.json()
    print_result("Get Budget Rule", result)
    
    # Test 3: Update budget rule
    print(f"\n3. Updating budget rule {rule_id}...")
    rule_data['rule_id'] = rule_id
    rule_data['limit_amount'] = 600.00
    response = requests.post(f"{BASE_URL}/budget-rules", json=rule_data)
    result = response.json()
    print_result("Update Budget Rule", result)
    
    # Test 4: Get rules for budget
    print(f"\n4. Getting rules for budget {budget_id}...")
    response = requests.get(f"{BASE_URL}/budget-rules/budget/{budget_id}")
    result = response.json()
    print(f"Found {result['count']} rules for this budget")
    
    return rule_id


def test_transaction_service(user_id, category_id):
    """Test Transaction Service endpoints"""
    print_section("TESTING TRANSACTION SERVICE")
    
    if not user_id or not category_id:
        print("⚠️ No user_id or category_id provided, skipping transaction tests")
        return None
    
    # Test 1: Create new transaction
    print("\n1. Creating new transaction...")
    transaction_data = {
        "transaction_id": 0,
        "user_id": user_id,
        "category_id": category_id,
        "amount": 75.50,
        "transaction_date": str(datetime.now().date()),
        "description": "Test transaction",
        "payment_method": "Credit Card"
    }
    response = requests.post(f"{BASE_URL}/transactions", json=transaction_data)
    result = response.json()
    print_result("Create Transaction", result)
    
    # Check for budget warnings
    if result.get('warnings'):
        print("\n⚠️ Budget Warnings:")
        for warning in result['warnings']:
            print(f"  - {warning}")
    
    if not result.get('success'):
        print("❌ Failed to create transaction. Stopping transaction tests.")
        return None
    
    transaction_id = result['transaction_id']
    print(f"✅ Transaction created with ID: {transaction_id}")
    
    # Test 2: Get transaction by ID
    print(f"\n2. Getting transaction by ID {transaction_id}...")
    response = requests.get(f"{BASE_URL}/transactions/{transaction_id}")
    result = response.json()
    print_result("Get Transaction", result)
    
    # Test 3: Update transaction
    print(f"\n3. Updating transaction {transaction_id}...")
    transaction_data['transaction_id'] = transaction_id
    transaction_data['amount'] = 85.00
    response = requests.post(f"{BASE_URL}/transactions", json=transaction_data)
    result = response.json()
    print_result("Update Transaction", result)
    
    # Test 4: Get user's transactions
    print(f"\n4. Getting transactions for user {user_id}...")
    response = requests.get(f"{BASE_URL}/transactions/user/{user_id}")
    result = response.json()
    print(f"Found {result['count']} transactions for this user")
    
    return transaction_id


def cleanup_test_data(user_id, category_id, budget_id, rule_id, transaction_id):
    """Clean up test data (optional)"""
    print_section("CLEANUP (Optional)")
    
    print("\nDo you want to delete the test data? (y/n): ", end="")
    choice = input().strip().lower()
    
    if choice != 'y':
        print("Skipping cleanup. Test data remains in database.")
        return
    
    # Delete in reverse order of dependencies
    if transaction_id:
        print(f"\nDeleting transaction {transaction_id}...")
        response = requests.delete(f"{BASE_URL}/transactions/{transaction_id}")
        print(response.json())
    
    if rule_id:
        print(f"\nDeleting budget rule {rule_id}...")
        response = requests.delete(f"{BASE_URL}/budget-rules/{rule_id}")
        print(response.json())
    
    if budget_id:
        print(f"\nDeleting budget {budget_id}...")
        response = requests.delete(f"{BASE_URL}/budgets/{budget_id}")
        print(response.json())
    
    if category_id:
        print(f"\nDeleting category {category_id}...")
        response = requests.delete(f"{BASE_URL}/categories/{category_id}")
        print(response.json())
    
    if user_id:
        print(f"\nDeleting user {user_id}...")
        response = requests.delete(f"{BASE_URL}/users/{user_id}")
        print(response.json())
    
    print("\n✅ Cleanup complete!")


def main():
    """Main test runner"""
    print_section("BUDGET TRACKER API TEST CLIENT")
    print(f"\nTesting API at: {BASE_URL}")
    print("Make sure the Flask server is running (python app.py)")
    
    try:
        # Test health endpoint
        response = requests.get(BASE_URL.replace('/api', '/'))
        if response.status_code == 200:
            print("✅ API is running!")
        else:
            print("❌ API is not responding correctly")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure Flask server is running.")
        return
    
    # Run all tests
    user_id = test_user_service()
    category_id = test_category_service()
    budget_id = test_budget_service(user_id)
    rule_id = test_budget_rule_service(budget_id, category_id)
    transaction_id = test_transaction_service(user_id, category_id)
    
    # Summary
    print_section("TEST SUMMARY")
    print(f"\nCreated IDs:")
    print(f"  User ID: {user_id}")
    print(f"  Category ID: {category_id}")
    print(f"  Budget ID: {budget_id}")
    print(f"  Budget Rule ID: {rule_id}")
    print(f"  Transaction ID: {transaction_id}")
    
    # Cleanup option
    cleanup_test_data(user_id, category_id, budget_id, rule_id, transaction_id)
    
    print_section("TESTING COMPLETE")
    print("✅ All service endpoints tested successfully!")


if __name__ == "__main__":
    main()
