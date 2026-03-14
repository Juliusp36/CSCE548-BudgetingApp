# Budget Tracker - Full Stack Application
## Deployment & System Test Documentation

**Course:** CSCE 548 - Full Stack Development  
**Project:** Complete N-Tier Application (Projects 1-4)  
**Technologies:** React, Flask, Python, MySQL, Railway, Render, Netlify  

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Prerequisites](#prerequisites)
4. [Database Setup (Railway)](#database-setup-railway)
5. [Backend Deployment (Render)](#backend-deployment-render)
6. [Frontend Deployment (Netlify)](#frontend-deployment-netlify)
7. [Local Development Setup](#local-development-setup)
8. [Testing & Verification](#testing--verification)
9. [AI-Generated Code Analysis](#ai-generated-code-analysis)
10. [Troubleshooting](#troubleshooting)

---

## Project Overview

Budget Tracker is a complete full-stack web application for personal budget management. The application demonstrates a professional n-tier architecture with:

- **Data Layer:** MySQL database with 5 normalized tables
- **Business Layer:** Python business logic with validation rules
- **Service Layer:** Flask REST API with CRUD endpoints
- **Client Layer:** React single-page application with purple theme

### Key Features

✅ **Full CRUD Operations** for all 5 tables (Users, Categories, Budgets, Budget Rules, Transactions)  
✅ **Business Rule Validation** (unique constraints, date validation, spending limits)  
✅ **Subset Queries** (filter budgets by user, rules by budget, transactions by user)  
✅ **Responsive Design** with purple (#A020F0) theme  
✅ **Cloud Deployment** (Railway + Render + Netlify)  

---

## Architecture

### System Diagram

```
┌─────────────────────────────────────┐
│   React Frontend (Netlify)          │
│   - User Interface                   │
│   - CRUD Forms                       │
│   - Data Display                     │
└─────────────┬───────────────────────┘
              │ HTTPS REST API
              ↓
┌─────────────────────────────────────┐
│   Flask REST API (Render)           │
│   - Service Layer Endpoints          │
│   - CORS Configuration               │
└─────────────┬───────────────────────┘
              │
              ↓
┌─────────────────────────────────────┐
│   Business Layer                     │
│   - Validation Logic                 │
│   - Business Rules                   │
└─────────────┬───────────────────────┘
              │
              ↓
┌─────────────────────────────────────┐
│   Data Access Layer                  │
│   - CRUD Operations                  │
│   - Connection Pooling               │
└─────────────┬───────────────────────┘
              │
              ↓
┌─────────────────────────────────────┐
│   MySQL Database (Railway)          │
│   - 5 Tables, 5 Foreign Keys         │
│   - 143 Rows Test Data               │
└─────────────────────────────────────┘
```

### Technology Stack

| Layer | Technology | Hosting |
|-------|-----------|---------|
| Frontend | React 18.2, Axios, React Router | Netlify |
| Service | Flask, Flask-CORS, Gunicorn | Render.com |
| Business | Python 3.x | (part of backend) |
| Data Access | mysql-connector-python | (part of backend) |
| Database | MySQL 8.0 | Railway |

---

## Prerequisites

Before deploying, ensure you have:

### Development Tools
- **Git** (2.0+) - Version control
- **Python** (3.8+) - Backend runtime
- **Node.js** (16+) & npm - Frontend build tools
- **MySQL Workbench** (optional) - Database management

### Cloud Accounts (All Free Tier)
- **GitHub** account - Code repository
- **Railway** account - MySQL database hosting
- **Render** account - Backend API hosting
- **Netlify** account - Frontend hosting

### Local Environment
- Terminal/Command Line access
- Text editor or IDE (VS Code recommended)
- Web browser (Chrome, Firefox, Safari)

---

## Database Setup (Railway)

### Step 1: Create MySQL Database

1. Go to [railway.app](https://railway.app)
2. Sign up/login with GitHub
3. Click **"New Project"**
4. Select **"Provision MySQL"**
5. Wait for database to provision (~30 seconds)

### Step 2: Get Database Credentials

1. Click on your MySQL service
2. Go to **"Variables"** tab
3. Copy these values:

```bash
MYSQLHOST     = viaduct.proxy.rlwy.net
MYSQLPORT     = 12345
MYSQLUSER     = root
MYSQLPASSWORD = your_password_here
MYSQLDATABASE = railway
```

⚠️ **Important:** Note the PORT - it's NOT 3306!

### Step 3: Connect to Database

Using MySQL command line:

```bash
mysql -h viaduct.proxy.rlwy.net -P 12345 -u root -p railway
# Enter password when prompted
```

Or using MySQL Workbench:
- Hostname: `viaduct.proxy.rlwy.net`
- Port: `12345` (your actual port)
- Username: `root`
- Password: (your Railway password)

### Step 4: Load Schema and Data

```bash
# Clone the repository first
git clone https://github.com/yourusername/CSCE548-BudgetingApp.git
cd CSCE548-BudgetingApp/backend

# Load schema
mysql -h viaduct.proxy.rlwy.net -P 12345 -u root -p railway < schema.sql

# Load test data
mysql -h viaduct.proxy.rlwy.net -P 12345 -u root -p railway < test_data.sql
```

### Step 5: Verify Database

```sql
-- Connect to database
mysql -h viaduct.proxy.rlwy.net -P 12345 -u root -p railway

-- Check tables
SHOW TABLES;

-- Should show: users, categories, budgets, budget_rules, transactions

-- Check data
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM transactions;

-- Should show 143 total rows across tables
```

✅ **Database setup complete!**

---

## Backend Deployment (Render)

### Step 1: Prepare Backend Files

Ensure your repository has these files in `backend/`:

```
backend/
├── models/           # Data Access Layer
├── business/         # Business Layer
├── app.py           # Flask service
├── db_config.py     # Database connection
├── requirements_service.txt
├── Procfile
└── .env (local only - not in git)
```

**Verify `requirements_service.txt`:**
```
Flask==3.0.0
Flask-CORS==4.0.0
mysql-connector-python==8.2.0
python-dotenv==1.0.0
gunicorn==21.2.0
```

**Verify `Procfile`:**
```
web: gunicorn app:app
```

### Step 2: Create Render Web Service

1. Go to [render.com](https://render.com)
2. Sign up/login with GitHub
3. Click **"New +"** → **"Web Service"**
4. Connect your GitHub repository
5. Select `CSCE548-BudgetingApp`

### Step 3: Configure Build Settings

```
Name:               budget-tracker-api
Region:             Oregon (or closest)
Branch:             main
Root Directory:     backend
Runtime:            Python 3
Build Command:      pip install -r requirements_service.txt
Start Command:      gunicorn app:app
```

### Step 4: Add Environment Variables

Click **"Advanced"** → **"Add Environment Variable"**

Add all Railway database credentials:

```
DB_HOST          = viaduct.proxy.rlwy.net
DB_PORT          = 12345
DB_USER          = root
DB_PASSWORD      = your_railway_password
DB_NAME          = railway
```

### Step 5: Deploy

1. Click **"Create Web Service"**
2. Wait 5-10 minutes for first deployment
3. Watch build logs for errors
4. Once deployed, note your URL: `https://your-app.onrender.com`

### Step 6: Test Backend API

```bash
# Test health endpoint
curl https://your-app.onrender.com/

# Should return:
{
  "service": "Budget Tracker API",
  "status": "running",
  "version": "1.0.0"
}

# Test users endpoint
curl https://your-app.onrender.com/api/users

# Should return JSON array of users
```

✅ **Backend deployment complete!**

⚠️ **Note:** Render free tier spins down after inactivity. First request may take 30-60 seconds.

---

## Frontend Deployment (Netlify)

### Step 1: Prepare Frontend Files

Ensure your repository has these files in `frontend/`:

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── Users.jsx
│   │   ├── Categories.jsx
│   │   ├── Budgets.jsx
│   │   ├── BudgetRules.jsx
│   │   └── Transactions.jsx
│   ├── services/
│   │   └── api.js
│   ├── App.jsx
│   ├── App.css
│   ├── index.js
│   └── index.css
└── package.json
```

**Verify `package.json` has build script:**
```json
"scripts": {
  "start": "react-scripts start",
  "build": "CI=false react-scripts build",
  "test": "react-scripts test",
  "eject": "react-scripts eject"
}
```

### Step 2: Create Netlify Site

1. Go to [netlify.com](https://netlify.com)
2. Sign up/login with GitHub
3. Click **"Add new site"** → **"Import an existing project"**
4. Choose **GitHub**
5. Select `CSCE548-BudgetingApp` repository

### Step 3: Configure Build Settings

```
Base directory:     frontend
Build command:      npm run build
Publish directory:  frontend/build
```

### Step 4: Add Environment Variable

1. Before deploying, click **"Show advanced"**
2. Click **"New variable"**
3. Add:
   ```
   Key:   REACT_APP_API_URL
   Value: https://your-backend.onrender.com/api
   ```
   
   ⚠️ **Important:** Use YOUR Render backend URL + `/api`

### Step 5: Deploy

1. Click **"Deploy site"**
2. Wait 3-5 minutes for build
3. Once deployed, note your URL: `https://random-name.netlify.app`

### Step 6: Customize Domain (Optional)

1. Go to **Site settings** → **Domain management**
2. Click **"Options"** → **"Edit site name"**
3. Change to: `budget-tracker-yourname`
4. New URL: `https://budget-tracker-yourname.netlify.app`

### Step 7: Test Frontend

1. Visit your Netlify URL
2. Should see purple-themed Budget Tracker app
3. Navigate to each section:
   - Users
   - Categories
   - Budgets
   - Budget Rules
   - Transactions

✅ **Frontend deployment complete!**

---

## Local Development Setup

For local testing and development:

### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/CSCE548-BudgetingApp.git
cd CSCE548-BudgetingApp
```

### Step 2: Setup Backend

```bash
cd backend

# Install dependencies
pip install -r requirements_service.txt --break-system-packages

# Create .env file with Railway credentials
cat > .env << EOF
DB_HOST=viaduct.proxy.rlwy.net
DB_PORT=12345
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=railway
EOF

# Start Flask server
python app.py

# Should show: Running on http://127.0.0.1:5001
```

### Step 3: Setup Frontend (New Terminal)

```bash
cd frontend

# Install dependencies
npm install

# Start React dev server
npm start

# Should open browser at http://localhost:3000
```

### Step 4: Test Locally

- Backend: http://localhost:5001
- Frontend: http://localhost:3000
- Both should be running simultaneously

✅ **Local development setup complete!**

---

## Testing & Verification

### Full System Test Checklist

Test each operation for all 5 tables:

#### **Users Table**
- [ ] Create new user
- [ ] View all users
- [ ] View single user
- [ ] Update user
- [ ] Delete user

#### **Categories Table**
- [ ] Create new category
- [ ] View all categories
- [ ] View single category
- [ ] Update category
- [ ] Delete category

#### **Budgets Table**
- [ ] Create new budget
- [ ] View all budgets
- [ ] View single budget
- [ ] **Filter budgets by user** (subset query)
- [ ] Update budget
- [ ] Delete budget

#### **Budget Rules Table**
- [ ] Create new budget rule
- [ ] View all rules
- [ ] View single rule
- [ ] **Filter rules by budget** (subset query)
- [ ] Update rule
- [ ] Delete rule

#### **Transactions Table**
- [ ] Create new transaction
- [ ] View all transactions
- [ ] View single transaction
- [ ] **Filter transactions by user** (subset query)
- [ ] Update transaction
- [ ] Delete transaction

### Database Verification

After each operation, verify in Railway database:

```sql
-- After creating a user
SELECT * FROM users ORDER BY created_at DESC LIMIT 1;

-- After updating a budget
SELECT * FROM budgets WHERE budget_id = 123;

-- After deleting a category
SELECT * FROM categories WHERE category_id = 456;
-- Should return empty

-- Verify subset queries
SELECT * FROM budgets WHERE user_id = 1;
SELECT * FROM budget_rules WHERE budget_id = 5;
SELECT * FROM transactions WHERE user_id = 2 LIMIT 10;
```

### Expected Results

✅ **All operations should:**
- Display success message in UI
- Update database immediately
- Reflect changes in subsequent queries
- Handle errors gracefully
- Validate business rules

---

## AI-Generated Code Analysis

### AI Tool Used

**Primary Tool:** Claude (Anthropic)  
**Model:** Claude Sonnet 4.5  
**Usage:** All code generation, debugging, and deployment guidance

### Prompts Used Per Layer

#### **Project 1: Data Layer**

**Initial Prompt:**
```
Create a MySQL database schema for a budget tracking application with 5 tables: 
users, categories, budgets, budget_rules, and transactions. Include foreign key 
relationships, proper constraints, and sample test data. Then create a Python 
Data Access Layer with full CRUD operations for each table using 
mysql-connector-python.
```

**Follow-up Prompts:**
- "Add connection pooling to the database configuration"
- "Create 143 rows of realistic test data"
- "Fix foreign key constraints to use InnoDB engine"

#### **Project 2: Business & Service Layers**

**Business Layer Prompt:**
```
Create a Python Business Layer that sits between the Data Access Layer and 
Service Layer. Implement business rules including: unique constraints, date 
validation, one active budget per user, spending limit warnings, and proper 
error handling. Use a save() pattern where ID=0 means INSERT, ID>0 means UPDATE.
```

**Service Layer Prompt:**
```
Create a Flask REST API service layer that exposes all business layer methods 
as HTTP endpoints. Include CORS support, proper error handling, and health 
check endpoints. Deploy to Render.com using Gunicorn.
```

#### **Project 3: Frontend**

**Initial Prompt:**
```
Create a React application with full CRUD operations for a budget tracking 
system with 5 tables: Users, Categories, Budgets, Budget Rules, and 
Transactions. Use purple (#A020F0) as the primary color. Include forms for 
create/update, tables for displaying data, view buttons for single records, 
delete buttons with confirmation, and filter dropdowns for subset queries.
```

**Styling Prompt:**
```
Adapt the styling from a garnet color scheme to purple (#A020F0). Create a 
professional design with gradient navigation, card-based layouts, smooth 
transitions, and responsive design.
```

### Changes Made to Generated Code

#### **Database Layer Modifications**
1. **Foreign Key Fix:** Added `ENGINE=InnoDB` to all CREATE TABLE statements (AI initially used default engine)
2. **Date Handling:** Modified `_validate_dates()` in `budget_manager.py` to handle both string and date objects
3. **Port Configuration:** Changed default port from 5000 to 5001 to avoid conflicts

#### **Business Layer Modifications**
1. **Date Comparison Bug:** Fixed budget manager where date strings were being compared with `<=` operator
   - Original code: `return end_date >= start_date` (failed when dates were strings)
   - Fixed code: Convert strings to date objects before comparison
   
2. **Unused Variables:** Removed unused `loading` state variables in `BudgetRules.jsx` and `Transactions.jsx`

#### **Service Layer Modifications**
1. **Environment Variables:** Updated `db_config.py` to use individual env vars instead of single connection string
2. **CORS Configuration:** Added proper CORS headers for Netlify domain

#### **Frontend Modifications**
1. **Build Configuration:** Added `CI=false` to npm build script to prevent warnings from breaking production builds
2. **API URL:** Configured `REACT_APP_API_URL` environment variable for deployment
3. **File Structure:** Moved `App.jsx` from `components/` to `src/` directory

### AI Effectiveness Analysis

#### **What AI Did Well ✅**

1. **Complete Code Generation**
   - Generated all 5 CRUD components with proper structure
   - Created comprehensive REST API endpoints
   - Built professional business layer with validation
   - Produced clean, maintainable code

2. **Best Practices**
   - Proper separation of concerns (n-tier architecture)
   - Connection pooling for database
   - Error handling and validation
   - RESTful API design

3. **Documentation**
   - Detailed inline comments
   - Clear function docstrings
   - README generation
   - Setup guides

4. **Styling & UX**
   - Professional, cohesive purple theme
   - Responsive design
   - Smooth animations
   - User-friendly forms

#### **What AI Missed ❌**

1. **Deployment-Specific Configuration**
   - Didn't account for Railway's non-standard MySQL port
   - Initial `.env` setup required manual configuration
   - Netlify build settings needed manual adjustment

2. **Edge Cases**
   - Date validation bug when mixing string/date types
   - Unused variable warnings in production builds
   - CORS configuration for specific domains

3. **Platform Nuances**
   - Render vs Netlify environment variable differences
   - Free tier cold start behavior (Render)
   - Build optimization flags (Netlify)

#### **Errors Resolved Manually 🔧**

1. **Budget Date Comparison Error**
   - Error: `'<=' not supported between instances of 'str' and 'int'`
   - Cause: Dates from forms were strings, code expected date objects
   - Fix: Added type checking and conversion in `_validate_dates()`

2. **Netlify Build Failure**
   - Error: `Treating warnings as errors because process.env.CI = true`
   - Cause: ESLint warnings for unused variables
   - Fix: Added `CI=false` to build script and removed unused variables

3. **API Connection Error**
   - Error: `Failed to load users: Endpoint not found`
   - Cause: `REACT_APP_API_URL` missing `/api` suffix
   - Fix: Updated environment variable to include full path

4. **MySQL Workbench Foreign Keys Not Showing**
   - Issue: Foreign keys present in database but not visible in GUI
   - Cause: MySQL Workbench bug with MySQL 9.x
   - Fix: Verified relationships via SQL query instead of GUI

#### **Overall Assessment**

**AI Effectiveness Score: 9/10**

**Strengths:**
- Generated 95% of functional code correctly
- Saved approximately 40-50 hours of manual coding
- Produced professional, industry-standard architecture
- Excellent at explaining concepts and debugging

**Weaknesses:**
- Required manual intervention for deployment edge cases
- Needed debugging for type conversion issues
- Some platform-specific knowledge gaps

**Conclusion:**  
AI was highly effective for rapid prototyping and development. The few issues encountered were minor and quickly resolved with targeted prompts or manual fixes. The tool excelled at generating boilerplate code, implementing patterns, and providing deployment guidance.

---

## Troubleshooting

### Common Issues

#### **Backend Issues**

**Issue:** `Database connection failed`
- Check Railway credentials in Render environment variables
- Verify Railway MySQL is running (green status)
- Confirm port is correct (not 3306)

**Issue:** `Render app spins down`
- Free tier sleeps after 15 minutes inactivity
- First request takes 30-60 seconds to wake
- Upgrade to paid tier for always-on service

**Issue:** `Module not found` during Render build
- Verify `requirements_service.txt` is in backend/ folder
- Check build command includes `-r requirements_service.txt`
- Ensure Python version compatibility

#### **Frontend Issues**

**Issue:** `Cannot connect to API`
- Verify `REACT_APP_API_URL` is set correctly in Netlify
- Check URL ends with `/api`
- Confirm backend is deployed and running
- Check browser console for CORS errors

**Issue:** `Build failed on Netlify`
- Check deploy logs for specific error
- Verify `package.json` has `build` script
- Try `CI=false` to ignore warnings
- Ensure `frontend/build` publish directory is correct

**Issue:** `Shows React logo instead of app`
- Build deployed from wrong directory
- Check base directory is `frontend`
- Verify GitHub has latest code
- Try "Clear cache and redeploy"

#### **Database Issues**

**Issue:** `Foreign keys not showing in MySQL Workbench`
- Known bug with MySQL Workbench 8.x and MySQL 9.x
- Verify via SQL: `SHOW CREATE TABLE table_name;`
- Relationships exist even if GUI doesn't show them

**Issue:** `Cannot connect to Railway database`
- Check you're using the PUBLIC hostname (ends with `.proxy.rlwy.net`)
- Don't use `mysql.railway.internal` (internal only)
- Verify port is correct
- Check Railway service is running

#### **Local Development Issues**

**Issue:** `Port 3000/5001 already in use`
```bash
# Kill process on port 3000
lsof -ti:3000 | xargs kill -9

# Kill process on port 5001
lsof -ti:5001 | xargs kill -9
```

**Issue:** `pip install fails`
- Use `--break-system-packages` flag on newer Python versions
- Or create virtual environment: `python -m venv venv`

---

## Deployment Verification Checklist

Use this checklist to verify successful deployment:

### Database (Railway)
- [ ] MySQL service is running (green status)
- [ ] Can connect via MySQL Workbench
- [ ] All 5 tables exist
- [ ] Tables have data (143 rows total)
- [ ] Foreign key relationships are present

### Backend (Render)
- [ ] Web service is deployed and running
- [ ] Health endpoint returns JSON: `https://your-app.onrender.com/`
- [ ] API endpoints accessible: `https://your-app.onrender.com/api/users`
- [ ] Environment variables are set (5 DB credentials)
- [ ] Build logs show no errors

### Frontend (Netlify)
- [ ] Site is deployed and live
- [ ] Purple theme displays correctly
- [ ] All 5 navigation links work
- [ ] Environment variable `REACT_APP_API_URL` is set
- [ ] No console errors in browser (F12)

### Full System
- [ ] Can create records in all 5 tables
- [ ] Can view all records
- [ ] Can view single records
- [ ] Can update records
- [ ] Can delete records
- [ ] Subset queries work (filter dropdowns)
- [ ] Data persists across sessions
- [ ] Changes reflect immediately in UI

✅ **If all items are checked, deployment is successful!**

---

## Project Statistics

### Development Timeline
- **Project 1 (Data Layer):** 6 hours
- **Project 2 (Business/Service):** 8 hours
- **Project 3 (Frontend):** 10 hours
- **Project 4 (Deployment/Docs):** 4 hours
- **Total:** ~28 hours

### Code Metrics
- **Total Files:** 25
- **Lines of Code:** ~3,500
- **Database Tables:** 5
- **Foreign Keys:** 5
- **API Endpoints:** 25
- **React Components:** 5
- **Test Data Rows:** 143

### Deployment URLs
- **Frontend:** https://benevolent-nasturtium-26b5e7.netlify.app
- **Backend:** https://csce548-budgetingapp.onrender.com
- **Database:** Railway (private)
- **Repository:** https://github.com/Juliusp36/CSCE548-BudgetingApp

---

## Credits

**Course:** CSCE 548 - Full Stack Development  
**Institution:** University of South Carolina  
**Semester:** Spring 2026  

**Technologies:** React, Flask, Python, MySQL, Railway, Render, Netlify  
**AI Assistance:** Claude (Anthropic) for code generation and debugging  

---

## License

Academic project for CSCE 548. All rights reserved.

---

**Last Updated:** March 13, 2026  
**Version:** 1.0.0  
**Status:** ✅ Complete and Deployed
