# QUICK SETUP GUIDE

## Budget Tracker - Data Layer Implementation

This guide will help you get the application running quickly.

## Step 1: Install MySQL

Download and install MySQL Community Server:
- Windows/Mac: https://dev.mysql.com/downloads/mysql/
- Linux: `sudo apt-get install mysql-server` (Ubuntu/Debian)

## Step 2: Install Python Dependencies

```bash
pip install mysql-connector-python
```

Or use the requirements file:
```bash
pip install -r requirements.txt
```

## Step 3: Update Database Credentials

Edit `db_config.py` (line 14-19) with your MySQL credentials:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',           # Change to your MySQL username
    'password': 'your_password',  # Change to your MySQL password
    'database': 'budget_tracker',
    'port': 3306
}
```

## Step 4: Create Database and Tables

Open MySQL command line or MySQL Workbench and run:

```bash
# Option 1: Using command line
mysql -u root -p < schema.sql

# Option 2: In MySQL Workbench
# File > Open SQL Script > Select schema.sql > Execute
```

## Step 5: Load Test Data

```bash
# Option 1: Using command line
mysql -u root -p < test_data.sql

# Option 2: In MySQL Workbench
# File > Open SQL Script > Select test_data.sql > Execute
```

## Step 6: Run the Application

```bash
python main.py
```

## Verification

To verify the data was loaded correctly:

1. In MySQL, run:
```sql
USE budget_tracker;
SELECT 'Users' as TableName, COUNT(*) as RowCount FROM users
UNION ALL
SELECT 'Categories', COUNT(*) FROM categories
UNION ALL
SELECT 'Budgets', COUNT(*) FROM budgets
UNION ALL
SELECT 'Budget Rules', COUNT(*) FROM budget_rules
UNION ALL
SELECT 'Transactions', COUNT(*) FROM transactions;
```

You should see:
- Users: 10
- Categories: 12
- Budgets: 15
- Budget Rules: 46
- Transactions: 60
- **Total: 143 rows**

## Taking Screenshots for Assignment

### Screenshot 1: Database Diagram
In MySQL Workbench:
1. Database > Reverse Engineer
2. Select budget_tracker database
3. Generate diagram showing all 5 tables with relationships
4. Screenshot the diagram

### Screenshot 2: Row Count
Run the verification query above and screenshot the results showing 50+ rows

### Screenshot 3: Application Execution
1. Run `python main.py`
2. Select option 10 (Database Statistics)
3. Screenshot showing the statistics
4. Select option 4 (View All Transactions)
5. Screenshot showing transactions being retrieved

### Screenshot 4: Data Retrieval
1. Select option 6 (View User Transactions)
2. Enter user ID: 1
3. Screenshot showing user's transactions with totals

## Troubleshooting

### "Access denied for user" error
- Check your username and password in db_config.py
- Ensure MySQL server is running

### "No module named 'mysql.connector'" error
- Run: `pip install mysql-connector-python`

### "Table doesn't exist" error
- Make sure you ran schema.sql first
- Verify database exists: `SHOW DATABASES;` in MySQL

### Connection timeout
- Check if MySQL server is running
- Verify port 3306 is not blocked by firewall

## Project Structure

```
budget-tracker/
├── schema.sql          # Creates database and tables
├── test_data.sql       # Populates tables with test data
├── db_config.py        # Database connection configuration
├── main.py            # Console application
├── requirements.txt   # Python dependencies
├── README.md         # Detailed documentation
└── models/           # Data Access Layer
    ├── __init__.py
    ├── user.py
    ├── category.py
    ├── budget.py
    ├── budget_rule.py
    └── transaction.py
```
