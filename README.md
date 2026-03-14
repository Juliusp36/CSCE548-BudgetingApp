# Budget Tracker Application

A comprehensive budget tracking system with a MySQL database backend and Python data access layer.

## Project Overview

This application allows users to:
- Track spending across multiple categories
- Create and manage multiple budgets (strict, moderate, custom)
- Set spending limits per category
- View spending summaries and analytics
- Manage transactions with detailed records

 # NOTE: do this before testing 
 make sure you install of the requirements using: 
```python
pip/pip3 install -r requirments.txt
```
# Data Access Layer 
## Run Command
```python
python3/python main.py             # gives you access to a frontend where you can execute various CRUD operations
```
## File Locations

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

### Prerequisites

- Python 3.8 or higher
- MySQL Server 8.0 or higher (or compatible like MariaDB)
# Business/Service Layer

**Database:** Hosted on [railway.com](https://railway.com) 

**API/Services:** Hosted on [render.com](https://render.com) 

**More specifically, my API's are hosted here:** [csce548-budgetingapp.onrender.com/](https://csce548-budgetingapp.onrender.com/)

### Run command
```
python/python3 client_test.py                 #This is envokes the client tester for the services which calls from the manager classes
```

**NOTE: Because I am hosting with the free tiers of railway and render, it will take some time (around 30-60 additional seconds) for the test script to run. Render specifically will spin down you’re instance when idle on the free tier. The process of completing all of the tests is fairly long without the additional loading time. When looking on the website during the coldstart/spin up period it may show that the API is not loading initially, but it will show after the cold start period** 

### File Locations

**Business layer:** Defines all of the rules for each table within the database
```
├── business/                  # Business layer (business rules)
│   ├── __init__.py
│   ├── user_manager.py
│   ├── category_manager.py
│   ├── budget_manager.py
│   ├── budget_rule_manager.py
│   └── transaction_manager.py
```

**Service layer (within the root directory):** Adds services/APIs for the data
```
/app.py
```

# Client Layer/Frontend
**Frontend:** Hosted on [netlify.com](https://benevolent-nasturtium-26b5e7.netlify.app) 

**NOTE: It may take a while for things on the external site to load due to Render's cold start time**
### File Locations
```
├──frontend/                       
    │
    ├── public/
    │   └── index.html
    │
    ├── src/
    │   ├── components/
    │   │   ├── Users.jsx
    │   │   ├── Categories.jsx
    │   │   ├── Budgets.jsx
    │   │   ├── BudgetRules.jsx
    │   │   └── Transactions.jsx
    │   │
    │   ├── services/
    │   │   └── api.js
    │   │
    │   ├── App.jsx
    │   ├── App.css
    │   ├── index.js
    │   └── index.css
    │
    ├── package.json
    ├── .gitignore
```
## License

This project was created as part of CSCE 548 coursework.

## Author - Julius Parker

Created for CSCE 548 - Full Stack Development
