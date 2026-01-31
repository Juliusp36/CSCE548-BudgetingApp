# Budget Tracker Application

A comprehensive budget tracking system with a MySQL database backend and Python data access layer.

## Project Overview

This application allows users to:
- Track spending across multiple categories
- Create and manage multiple budgets (strict, moderate, custom)
- Set spending limits per category
- View spending summaries and analytics
- Manage transactions with detailed records

## Database Schema

The application uses 5 tables with proper relationships:

### Tables

1. **users** - User account information
   - Primary Key: user_id
   - Unique constraints on username and email

2. **categories** - Spending categories
   - Primary Key: category_id
   - Unique constraint on category_name

3. **budgets** - Budget configurations
   - Primary Key: budget_id
   - Foreign Key: user_id → users(user_id)

4. **budget_rules** - Category spending limits within budgets
   - Primary Key: rule_id
   - Foreign Keys:
     - budget_id → budgets(budget_id)
     - category_id → categories(category_id)

5. **transactions** - Individual spending records
   - Primary Key: transaction_id
   - Foreign Keys:
     - user_id → users(user_id)
     - category_id → categories(category_id)

### Relationships

- Users → Budgets (One-to-Many, CASCADE delete)
- Budgets → Budget Rules (One-to-Many, CASCADE delete)
- Categories → Budget Rules (One-to-Many, CASCADE delete)
- Users → Transactions (One-to-Many, CASCADE delete)
- Categories → Transactions (One-to-Many, RESTRICT delete)

## Installation

### Prerequisites

- Python 3.8 or higher
- MySQL Server 8.0 or higher (or compatible like MariaDB)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd budget-tracker
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure database connection**
   
   Edit `db_config.py` and update the database credentials:
   ```python
   DB_CONFIG = {
       'host': 'localhost',
       'user': 'your_mysql_username',
       'password': 'your_mysql_password',
       'database': 'budget_tracker',
       'port': 3306
   }
   ```

4. **Create the database**
   ```bash
   mysql -u root -p < schema.sql
   ```

5. **Load test data**
   ```bash
   mysql -u root -p < test_data.sql
   ```

## Running the Application

Start the console application:
```bash
python main.py
```

## Features

### Menu Options

1. **View All Users** - Display all registered users
2. **View All Categories** - Show spending categories with transaction counts
3. **View All Budgets** - List all budgets with details
4. **View All Transactions** - Display recent transactions (last 50)
5. **View Budget Details** - Detailed information about a specific budget
6. **View User Transactions** - All transactions for a specific user
7. **View Spending Summary** - Spending breakdown by category for a date range
8. **View Budget Rules with Spending** - Budget limits vs actual spending
9. **Create New Transaction** - Add a new spending entry
10. **Database Statistics** - Overview of database contents

## Project Structure

```
budget-tracker/
├── schema.sql              # Database schema creation
├── test_data.sql           # Test data insertion (50+ rows)
├── db_config.py           # Database configuration
├── main.py                # Console application
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── models/
    ├── __init__.py       # Models package initialization
    ├── user.py           # User model with CRUD operations
    ├── category.py       # Category model with CRUD operations
    ├── budget.py         # Budget model with CRUD operations
    ├── budget_rule.py    # Budget Rule model with CRUD operations
    └── transaction.py    # Transaction model with CRUD operations
```

## Data Access Layer

All models include complete CRUD operations:

- **Create**: Insert new records
- **Read**: Retrieve by ID, get all, custom queries
- **Update**: Modify existing records
- **Delete**: Remove records

### Example Usage

```python
from models import User, Transaction

# Create a new user
user_id = User.create("john_doe", "john@email.com", "hashed_password")

# Get user by ID
user = User.get_by_id(user_id)

# Update user
User.update(user_id, email="newemail@email.com")

# Create transaction
Transaction.create(user_id, category_id=1, amount=45.67, 
                  transaction_date="2024-02-15", 
                  description="Grocery shopping")

# Get user's transactions
transactions = Transaction.get_by_user(user_id)
```

## Database Constraints

- Email validation (CHECK constraint)
- Positive amounts for budgets and transactions
- Date validation (end_date >= start_date)
- Alert thresholds between 0-100%
- Unique budget-category combinations in budget rules

## Test Data

The database is populated with:
- 10 users
- 12 categories
- 15 budgets
- 40+ budget rules
- 60+ transactions

**Total: 137+ rows across all tables**
## Future Enhancements

Potential features for future iterations:
- User authentication with password hashing
- Budget analytics and visualizations
- Recurring transaction support
- Budget alerts and notifications
- Export functionality (CSV, PDF)
- Web-based frontend
- Mobile application

## License

This project was created as part of CSCE 548 coursework.

## Author - Julius Parker

Created for CSCE 548 - Full Stack Development
