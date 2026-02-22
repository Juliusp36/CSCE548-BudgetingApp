# Business Layer Documentation

## Overview

The Business Layer sits between the Service Layer (REST APIs) and the Data Access Layer (models). It implements all business rules, validation logic, and authorization before calling the database.

## Architecture

```
Service Layer (Flask REST APIs)
    ↓
Business Layer (Manager Classes) ← YOU ARE HERE
    ↓
Data Access Layer (Models)
    ↓
MySQL Database
```

## Business Layer Components

### 1. UserManager (`business/user_manager.py`)

**Methods:**
- `save(user_id, username, email, password_hash)` - Insert if ID=0, Update if ID exists
- `get_by_id(user_id)` - Retrieve user by ID
- `get_all()` - Retrieve all users
- `delete(user_id)` - Delete user (cascades to budgets/transactions)
- `get_by_username(username)` - Additional: Find user by username
- `count()` - Additional: Get total user count

**Business Rules:**
- ✅ Email must be unique and valid format
- ✅ Username must be unique
- ✅ Password must be at least 8 characters with letters and numbers
- ✅ Cannot delete if user has active budgets (cascade handled by DB)

---

### 2. CategoryManager (`business/category_manager.py`)

**Methods:**
- `save(category_id, category_name, description, icon)` - Insert if ID=0, Update if ID exists
- `get_by_id(category_id)` - Retrieve category by ID
- `get_all()` - Retrieve all categories
- `delete(category_id)` - Delete category
- `get_with_transaction_count()` - Additional: Categories with transaction counts
- `count()` - Additional: Get total category count

**Business Rules:**
- ✅ Category name must be unique
- ✅ Category name is required
- ✅ Cannot delete category if it has transactions (RESTRICT constraint)

---

### 3. BudgetManager (`business/budget_manager.py`)

**Methods:**
- `save(budget_id, user_id, budget_name, budget_type, total_amount, start_date, end_date, is_active)` - Insert if ID=0, Update if ID exists
- `get_by_id(budget_id)` - Retrieve budget by ID
- `get_all()` - Retrieve all budgets
- `delete(budget_id)` - Delete budget (cascades to budget rules)
- `get_by_user(user_id)` - Additional: Get user's budgets
- `get_active_budgets(user_id)` - Additional: Get active budgets
- `deactivate(budget_id)` - Additional: Soft delete budget
- `count()` - Additional: Get total budget count

**Business Rules:**
- ✅ **User can only have ONE active budget at a time** (critical rule!)
- ✅ End date must be on or after start date
- ✅ Total amount must be positive
- ✅ Budget name must be unique per user
- ✅ Budget type must be: 'strict', 'moderate', or 'custom'
- ✅ User must exist

---

### 4. BudgetRuleManager (`business/budget_rule_manager.py`)

**Methods:**
- `save(rule_id, budget_id, category_id, limit_amount, alert_threshold)` - Insert if ID=0, Update if ID exists
- `get_by_id(rule_id)` - Retrieve rule by ID
- `get_all()` - Retrieve all rules
- `delete(rule_id)` - Delete rule
- `get_by_budget(budget_id)` - Additional: Get rules for a budget
- `get_rules_with_spending(budget_id)` - Additional: Rules with spending data
- `check_budget_alerts(budget_id)` - Additional: Check which categories are over threshold
- `count()` - Additional: Get total rule count

**Business Rules:**
- ✅ Limit amount must be positive
- ✅ Alert threshold must be between 0-100%
- ✅ Cannot have duplicate rules (same budget + category)
- ✅ **Limit cannot exceed budget total**
- ✅ Budget and category must exist

---

### 5. TransactionManager (`business/transaction_manager.py`)

**Methods:**
- `save(transaction_id, user_id, category_id, amount, transaction_date, description, payment_method)` - Insert if ID=0, Update if ID exists
- `get_by_id(transaction_id)` - Retrieve transaction by ID
- `get_all(limit)` - Retrieve all transactions
- `delete(transaction_id)` - Delete transaction
- `get_by_user(user_id, limit)` - Additional: Get user's transactions
- `get_spending_summary(user_id, start_date, end_date)` - Additional: Spending breakdown
- `count()` - Additional: Get total transaction count

**Business Rules:**
- ✅ Amount must be positive
- ✅ Date cannot be in the future
- ✅ User and category must exist
- ✅ **Warns if transaction pushes spending over budget limit** (returns warnings array)
- ✅ **Warns if transaction is outside active budget period**

---

## Usage Examples

### Example 1: Create New User

```python
from business.user_manager import UserManager

# Create new user (ID = 0)
result = UserManager.save(
    user_id=0,
    username="alice123",
    email="alice@example.com",
    password_hash="SecurePass123"
)

if result['success']:
    print(f"User created with ID: {result['user_id']}")
else:
    print(f"Error: {result['error']}")
```

### Example 2: Update Existing Budget

```python
from business.budget_manager import BudgetManager

# Update existing budget (ID = 5)
result = BudgetManager.save(
    budget_id=5,
    user_id=1,
    budget_name="Updated Monthly Budget",
    budget_type="moderate",
    total_amount=3000.00,
    start_date="2024-02-01",
    end_date="2024-02-29",
    is_active=True
)

if result['success']:
    print("Budget updated successfully")
else:
    print(f"Error: {result['error']}")
```

### Example 3: Create Transaction with Budget Warnings

```python
from business.transaction_manager import TransactionManager

# Create new transaction
result = TransactionManager.save(
    transaction_id=0,
    user_id=1,
    category_id=2,  # Dining Out
    amount=150.00,
    transaction_date="2024-02-15",
    description="Expensive dinner",
    payment_method="Credit Card"
)

if result['success']:
    print(f"Transaction created: ID {result['transaction_id']}")
    
    # Check for budget warnings
    if result['warnings']:
        for warning in result['warnings']:
            print(f"⚠️ {warning}")
else:
    print(f"Error: {result['error']}")
```

### Example 4: Check Budget Alerts

```python
from business.budget_rule_manager import BudgetRuleManager

# Check which categories are over their alert thresholds
alerts = BudgetRuleManager.check_budget_alerts(budget_id=2)

for alert in alerts:
    print(f"{alert['category']}: ${alert['spent']:.2f} / ${alert['limit']:.2f}")
    print(f"  Status: {alert['status']}")
```

---

## Return Value Format

All `save()` and `delete()` methods return a dictionary:

### Success Response:
```python
{
    "success": True,
    "user_id": 123,  # or budget_id, transaction_id, etc.
    "message": "User created successfully",
    "warnings": []  # Only for transactions
}
```

### Error Response:
```python
{
    "success": False,
    "error": "Email already exists"
}
```

---

## Key Design Decisions

### 1. **Save Pattern (Insert vs Update)**
Following the lecture's pattern:
- If `ID == 0` → Call DAL's `create()` method (INSERT)
- If `ID > 0` → Call DAL's `update()` method (UPDATE)

### 2. **Validation Before Database**
All validation happens in the business layer BEFORE calling the data layer. This ensures:
- Invalid data never reaches the database
- Consistent error messages
- Business rules enforced centrally

### 3. **Cascade Awareness**
Business layer is aware of database cascade rules:
- Deleting user cascades to budgets and transactions
- Deleting budget cascades to budget rules
- Deleting category is restricted if transactions exist

### 4. **Additional Methods**
Beyond the required Save/Get/GetAll/Delete, each manager includes:
- Count methods
- Specialized query methods
- Business-specific logic (e.g., budget alerts)

---

## Testing the Business Layer

Before creating the service layer, test business layer directly:

```python
# test_business_layer.py
from business.user_manager import UserManager
from business.budget_manager import BudgetManager

# Test 1: Create user
print("Test 1: Creating user...")
result = UserManager.save(0, "testuser", "test@example.com", "TestPass123")
print(result)

# Test 2: Try creating duplicate user (should fail)
print("\nTest 2: Creating duplicate user...")
result = UserManager.save(0, "testuser", "test2@example.com", "TestPass123")
print(result)

# Test 3: Try creating second active budget (should fail)
print("\nTest 3: Creating second active budget...")
result = BudgetManager.save(0, 1, "Second Budget", "moderate", 2000, 
                           "2024-02-01", "2024-02-29", True)
print(result)
```

---

## Next Steps

1. ✅ Business Layer Complete
2. ⏭️ Create Service Layer (Flask REST APIs)
3. ⏭️ Host Services (Render.com - free tier)
4. ⏭️ Create Console Test Client
5. ⏭️ Take Screenshots
6. ⏭️ Document in Overview

---

## Graduate Requirements Met

✅ All DAL CRUD operations accessible through business layer
✅ Business rules implemented and validated
✅ Error handling throughout
✅ Additional business methods beyond basic CRUD
✅ Professional code structure with docstrings
✅ Ready for service layer integration
