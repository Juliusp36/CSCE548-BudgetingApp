# Service Layer Deployment Guide

## Complete File Structure

```
CSCE548-BudgetingApp/
├── schema.sql
├── test_data.sql
├── .env                           # Local MySQL password
├── .gitignore
├── requirements_service.txt       # NEW - Flask dependencies
├── Procfile                       # NEW - For Render.com
│
├── db_config.py
├── main.py                        # Original console app (Project 1)
├── app.py                         # NEW - Flask REST API server
├── client_test.py                 # NEW - Service test client
│
├── models/                        # Data Access Layer
│   ├── __init__.py
│   ├── user.py
│   ├── category.py
│   ├── budget.py
│   ├── budget_rule.py
│   └── transaction.py
│
└── business/                      # Business Layer
    ├── __init__.py
    ├── user_manager.py
    ├── category_manager.py
    ├── budget_manager.py
    ├── budget_rule_manager.py
    └── transaction_manager.py
```

---

## Part 1: Local Testing (Run on Your Computer)

### Step 1: Install Service Layer Dependencies

```bash
cd CSCE548-BudgetingApp
pip install -r requirements_service.txt
```

This installs:
- Flask (web framework)
- Flask-CORS (cross-origin requests)
- Gunicorn (production server)
- All existing dependencies

### Step 2: Start the Flask Server

```bash
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Running on http://localhost:5000
```

**Leave this terminal running!**

### Step 3: Test the API

Open a NEW terminal and run:

```bash
# Test health endpoint
curl http://localhost:5000/

# Or use the test client
python client_test.py
```

The client will:
- ✅ Create a user
- ✅ Create a category
- ✅ Create a budget
- ✅ Create a budget rule
- ✅ Create a transaction
- ✅ Update each item
- ✅ Get each item by ID
- ✅ Delete everything (optional)

### Step 4: Take Screenshots (Required for Assignment)

Screenshot these:
1. **Flask server running** - Terminal showing "Running on http://127.0.0.1:5000"
2. **Test client output** - Showing successful API calls
3. **API health check** - `curl http://localhost:5000/` response
4. **Service execution** - Any successful POST/GET/DELETE response

---

## Part 2: Deploy to Render.com (Cloud Hosting - FREE)

### Why Render.com?
- ✅ Free tier (750 hours/month - enough for testing)
- ✅ Auto-deploys from GitHub
- ✅ Built-in MySQL support (or connect to external DB)
- ✅ HTTPS by default
- ✅ Easy setup

### Step 1: Push Code to GitHub

```bash
cd CSCE548-BudgetingApp

# Add new files
git add app.py client_test.py requirements_service.txt Procfile business/

# Commit
git commit -m "Add service layer and Flask API"

# Push
git push origin main
```

### Step 2: Create Render.com Account

1. Go to https://render.com/
2. Sign up with GitHub account (easiest)
3. Authorize Render to access your repositories

### Step 3: Create New Web Service

1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository: `CSCE548-BudgetingApp`
3. Configure the service:

**Settings:**
```
Name: budget-tracker-api
Region: Oregon (US West) - or closest to you
Branch: main
Root Directory: (leave blank)
Runtime: Python 3
Build Command: pip install -r requirements_service.txt
Start Command: gunicorn app:app
Instance Type: Free
```

### Step 4: Add Environment Variables

In Render dashboard, go to **Environment** tab and add:

```
SQLPASS=your_mysql_password
```

**IMPORTANT:** You'll need to either:
- **Option A:** Use your local MySQL (keep computer running) - NOT recommended
- **Option B:** Use a cloud MySQL database (see below)

### Step 5: Cloud MySQL Options (Choose One)

#### Option A: Railway.app MySQL (Recommended - Free $5/month credit)

1. Go to https://railway.app/
2. Sign up → Create new project
3. Add **MySQL** database
4. Copy connection details:
   - Host
   - Port
   - Database name
   - Username
   - Password

5. Update `db_config.py` in your code:
```python
DB_CONFIG = {
    'host': 'containers-us-west-xxx.railway.app',  # From Railway
    'user': 'root',
    'password': 'xxx',  # From Railway
    'database': 'railway',
    'port': 6603  # From Railway
}
```

6. Re-run your schema and test data:
```bash
mysql -h containers-us-west-xxx.railway.app -P 6603 -u root -p < schema.sql
mysql -h containers-us-west-xxx.railway.app -P 6603 -u root -p < test_data.sql
```

#### Option B: PlanetScale (Free tier)

1. Go to https://planetscale.com/
2. Create free account
3. Create database
4. Get connection string
5. Update `db_config.py`

#### Option C: Render.com MySQL (Paid - $7/month)

1. In Render dashboard, create **PostgreSQL** database (free)
2. Update your models to use PostgreSQL instead of MySQL

### Step 6: Deploy!

1. Push changes to GitHub
2. Render will auto-deploy (takes 2-5 minutes)
3. Watch the deployment logs in Render dashboard
4. Once deployed, you'll get a URL like:
   ```
   https://budget-tracker-api.onrender.com
   ```

### Step 7: Test Your Deployed API

Update `client_test.py`:
```python
# Change this line
BASE_URL = "https://budget-tracker-api.onrender.com/api"
```

Run the test:
```bash
python client_test.py
```

---

## Part 3: API Endpoints Documentation

### Base URL
- **Local:** `http://localhost:5000/api`
- **Deployed:** `https://your-app.onrender.com/api`

### User Service (`/users`)
```
POST   /api/users                 - Create or update user
GET    /api/users/{id}            - Get user by ID
GET    /api/users                 - Get all users
DELETE /api/users/{id}            - Delete user
```

### Category Service (`/categories`)
```
POST   /api/categories            - Create or update category
GET    /api/categories/{id}       - Get category by ID
GET    /api/categories            - Get all categories
DELETE /api/categories/{id}       - Delete category
```

### Budget Service (`/budgets`)
```
POST   /api/budgets               - Create or update budget
GET    /api/budgets/{id}          - Get budget by ID
GET    /api/budgets               - Get all budgets
GET    /api/budgets/user/{id}     - Get user's budgets
DELETE /api/budgets/{id}          - Delete budget
```

### Budget Rule Service (`/budget-rules`)
```
POST   /api/budget-rules          - Create or update rule
GET    /api/budget-rules/{id}     - Get rule by ID
GET    /api/budget-rules          - Get all rules
GET    /api/budget-rules/budget/{id} - Get budget's rules
DELETE /api/budget-rules/{id}     - Delete rule
```

### Transaction Service (`/transactions`)
```
POST   /api/transactions          - Create or update transaction
GET    /api/transactions/{id}     - Get transaction by ID
GET    /api/transactions          - Get all transactions
GET    /api/transactions/user/{id} - Get user's transactions
DELETE /api/transactions/{id}     - Delete transaction
```

---

## Part 4: Testing Examples

### Using curl:

```bash
# Health check
curl https://your-app.onrender.com/

# Create user
curl -X POST https://your-app.onrender.com/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 0,
    "username": "johndoe",
    "email": "john@example.com",
    "password_hash": "SecurePass123"
  }'

# Get all users
curl https://your-app.onrender.com/api/users

# Get user by ID
curl https://your-app.onrender.com/api/users/1
```

### Using Python (requests):

```python
import requests

BASE_URL = "https://your-app.onrender.com/api"

# Create user
response = requests.post(f"{BASE_URL}/users", json={
    "user_id": 0,
    "username": "johndoe",
    "email": "john@example.com",
    "password_hash": "SecurePass123"
})
print(response.json())
```

---

## Part 5: Troubleshooting

### Issue: "Cannot connect to API"
**Solution:** Make sure Flask server is running (`python app.py`)

### Issue: "Database connection error"
**Solution:** 
1. Check MySQL is running: `mysql -u root -p`
2. Verify `.env` file has correct password
3. Test connection in `db_config.py`

### Issue: Render deployment fails
**Solution:**
1. Check Render logs for errors
2. Verify `requirements_service.txt` has all dependencies
3. Make sure `Procfile` exists
4. Check environment variables are set

### Issue: "Module not found" errors
**Solution:**
```bash
pip install -r requirements_service.txt
```

### Issue: Render app sleeps after inactivity
**Solution:** This is normal on free tier. First request will wake it up (takes 30 seconds).

---

## Part 6: For Your Overview Document

Document these items:

### AI Prompts Used:
```
"Create a Flask REST API service layer that exposes my business layer 
managers through HTTP endpoints. Include routes for all CRUD operations 
for users, categories, budgets, budget rules, and transactions."
```

### Changes You Made:
- List any modifications to generated code
- Business rules you added yourself
- Error handling improvements
- Any debugging you did

### Hosting Steps:
1. Installed Flask and dependencies
2. Created Render.com account
3. Connected GitHub repository
4. Configured environment variables
5. Deployed and tested endpoints
6. Verified all CRUD operations work

### Screenshots to Include:
1. ✅ Flask server running locally
2. ✅ Test client showing successful API calls
3. ✅ Render dashboard showing deployed app
4. ✅ Deployed API health check response
5. ✅ Example of Create → Get → Update → Delete sequence

---

## Summary

Your services are now:
- ✅ **5 REST API services** (Users, Categories, Budgets, Rules, Transactions)
- ✅ **Hosted locally** for testing
- ✅ **Deployed to cloud** (Render.com - free tier)
- ✅ **Fully tested** with client
- ✅ **Documented** with deployment instructions

**Assignment Requirements Met:**
- ✅ Business layer created
- ✅ Service layer created
- ✅ Services hosted (local + cloud)
- ✅ Console test client created
- ✅ All methods accessible through services
- ✅ Screenshots taken
- ✅ Code in GitHub

You're done! 🎉
