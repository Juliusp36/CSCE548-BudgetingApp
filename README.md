# Budget Tracker Application
## Quick Start Guide - Local Development

### Requirements
* Python 3.8 or higher
* Node.js 16+ and npm
* MySQL 8.0 or higher
* Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/CSCE548-BudgetingApp.git
cd CSCE548-BudgetingApp
```

### Step 2: Verify Python Installation

If you don't have Python installed, download it from [python.org/downloads](https://www.python.org/downloads/). During installation, make sure to check "Add Python to PATH".

Verify installation:

```bash
python --version
# or
python3 --version
```

### Step 3: Install and Setup MySQL

#### 3.1 Install MySQL

**macOS (using Homebrew):**
```bash
brew install mysql
brew services start mysql
```

**Windows:**
- Download from [dev.mysql.com/downloads/mysql](https://dev.mysql.com/downloads/mysql/)
- Follow installer instructions
- Start MySQL from Services or MySQL Workbench

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install mysql-server
sudo systemctl start mysql
```

#### 3.2 Secure MySQL Installation

```bash
sudo mysql_secure_installation
```

Follow prompts:
- Set root password (remember this!)
- Remove anonymous users: Yes
- Disallow root login remotely: Yes
- Remove test database: Yes
- Reload privilege tables: Yes

#### 3.3 Create Database and Load Data

```bash
# Connect to MySQL
mysql -u root -p
# Enter your root password

# Create database and user
CREATE DATABASE budget_tracker;
CREATE USER 'budget_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON budget_tracker.* TO 'budget_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

#### 3.4 Load Schema and Test Data

```bash
cd backend

# Load schema
mysql -u budget_user -p budget_tracker < schema.sql

# Load test data
mysql -u budget_user -p budget_tracker < test_data.sql
```

#### 3.5 Verify Database

```bash
mysql -u budget_user -p budget_tracker

# Once connected, verify tables
SHOW TABLES;
# Should show: users, categories, budgets, budget_rules, transactions

# Check data
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM transactions;
# Should show 143 total rows

EXIT;
```

---

### Step 4: Backend Setup

#### 4.1 Set Up Virtual Environment

```bash
# Make sure you're in backend/ directory
cd backend

python -m venv venv
```

Activate it:
* **macOS/Linux:**
  ```bash
  source venv/bin/activate
  ```

* **Windows:**
  ```bash
  venv\Scripts\activate
  ```

#### 4.2 Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4.3 Configure Database Connection

Create a `.env` file in the `backend/` directory:

```bash
# .env
DB_HOST=localhost
DB_PORT=3306
DB_USER=budget_user
DB_PASSWORD=your_password
DB_NAME=budget_tracker
```

Replace `your_password` with the password you set in Step 3.3.

#### 4.4 Start Backend Server

```bash
python app.py
```

You should see:
```
* Running on http://127.0.0.1:5001
```

Backend is now running at: `http://localhost:5001`

---

### Step 5: Frontend Setup (New Terminal)

**Open a NEW terminal window** (keep backend running in the first one)

#### 5.1 Navigate to Frontend Directory

```bash
cd CSCE548-BudgetingApp/frontend
```

#### 5.2 Install Dependencies

```bash
npm install
```

#### 5.3 Start Frontend Server

```bash
npm start
```

Frontend should automatically open at: `http://localhost:3000`

---

### Step 6: Verify Everything Works

- ✅ Backend running at `http://localhost:5001`
- ✅ Frontend running at `http://localhost:3000`
- ✅ Navigate through all 5 sections (Users, Categories, Budgets, Budget Rules, Transactions)
- ✅ Try creating a record to verify database connection

**Test the backend API directly:**
```bash
# In a third terminal
curl http://localhost:5001/
# Should return JSON with service info

curl http://localhost:5001/api/users
# Should return array of users
```

---

### Stopping the Servers

**Backend:**
- Press `Ctrl+C` in backend terminal
- Deactivate virtual environment: `deactivate`

**Frontend:**
- Press `Ctrl+C` in frontend terminal

**MySQL:**
- Stays running in background (good for development)
- To stop: `brew services stop mysql` (macOS) or stop via Services (Windows)

---

### Troubleshooting

#### **Port already in use:**
```bash
# Kill process on port 5001 (backend)
lsof -ti:5001 | xargs kill -9

# Kill process on port 3000 (frontend)
lsof -ti:3000 | xargs kill -9
```

#### **MySQL connection errors:**

**"Access denied for user":**
- Verify password in `.env` matches MySQL user password
- Try connecting manually: `mysql -u budget_user -p budget_tracker`

**"Can't connect to MySQL server":**
- Check MySQL is running: `brew services list` (macOS) or check Services (Windows)
- Start MySQL: `brew services start mysql` (macOS)

**"Database doesn't exist":**
- Recreate database: `mysql -u root -p -e "CREATE DATABASE budget_tracker;"`
- Reload schema: `mysql -u budget_user -p budget_tracker < schema.sql`

#### **Python module not found errors:**
- Ensure virtual environment is activated: `(venv)` should appear in prompt
- Reinstall dependencies: `pip install -r requirements_service.txt`

#### **Frontend shows "Failed to load users":**
- Verify backend is running on port 5001
- Check browser console (F12) for specific errors
- Verify `.env` database credentials are correct

---

### MySQL Management Tools (Optional)

**MySQL Workbench** (GUI for database management):
- Download: [dev.mysql.com/downloads/workbench](https://dev.mysql.com/downloads/workbench/)
- Connection: `localhost:3306`, user: `budget_user`

**Command Line Tools:**
```bash
# View all databases
mysql -u budget_user -p -e "SHOW DATABASES;"

# Backup database
mysqldump -u budget_user -p budget_tracker > backup.sql

# Restore database
mysql -u budget_user -p budget_tracker < backup.sql
```

---

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
