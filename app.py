"""
Budget Tracker REST API - Service Layer
Flask application that exposes business layer through REST endpoints

HOSTING INSTRUCTIONS:
1. Local: python app.py (runs on http://localhost:5001)
2. Render.com: Push to GitHub, connect repo, deploy automatically
   - Platform: Web Service
   - Build Command: pip install -r requirements_service.txt
   - Start Command: gunicorn app:app
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import business layer managers
from business.user_manager import UserManager
from business.category_manager import CategoryManager
from business.budget_manager import BudgetManager
from business.budget_rule_manager import BudgetRuleManager
from business.transaction_manager import TransactionManager

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
app.config['JSON_SORT_KEYS'] = False


# ============================================================================
# HEALTH CHECK & INFO
# ============================================================================

@app.route('/', methods=['GET'])
def home():
    """API home/health check endpoint"""
    return jsonify({
        "service": "Budget Tracker API",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "users": "/api/users",
            "categories": "/api/categories",
            "budgets": "/api/budgets",
            "budget_rules": "/api/budget-rules",
            "transactions": "/api/transactions"
        }
    })


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check for monitoring"""
    return jsonify({"status": "healthy"}), 200


# ============================================================================
# USER SERVICE - /api/users
# ============================================================================

@app.route('/api/users', methods=['POST'])
def create_or_update_user():
    """
    Create or update a user
    Body: {user_id, username, email, password_hash}
    If user_id is 0, creates new user. Otherwise updates existing.
    """
    try:
        data = request.get_json()
        
        result = UserManager.save(
            user_id=data.get('user_id', 0),
            username=data.get('username'),
            email=data.get('email'),
            password_hash=data.get('password_hash')
        )
        
        status_code = 201 if result.get('success') and data.get('user_id', 0) == 0 else 200
        return jsonify(result), status_code if result.get('success') else 400
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get user by ID"""
    try:
        user = UserManager.get_by_id(user_id)
        if user:
            return jsonify({"success": True, "data": user}), 200
        return jsonify({"success": False, "error": "User not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/users', methods=['GET'])
def get_all_users():
    """Get all users"""
    try:
        users = UserManager.get_all()
        return jsonify({"success": True, "data": users, "count": len(users)}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete user by ID"""
    try:
        result = UserManager.delete(user_id)
        return jsonify(result), 200 if result.get('success') else 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ============================================================================
# CATEGORY SERVICE - /api/categories
# ============================================================================

@app.route('/api/categories', methods=['POST'])
def create_or_update_category():
    """
    Create or update a category
    Body: {category_id, category_name, description, icon}
    """
    try:
        data = request.get_json()
        
        result = CategoryManager.save(
            category_id=data.get('category_id', 0),
            category_name=data.get('category_name'),
            description=data.get('description', ''),
            icon=data.get('icon', '')
        )
        
        status_code = 201 if result.get('success') and data.get('category_id', 0) == 0 else 200
        return jsonify(result), status_code if result.get('success') else 400
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    """Get category by ID"""
    try:
        category = CategoryManager.get_by_id(category_id)
        if category:
            return jsonify({"success": True, "data": category}), 200
        return jsonify({"success": False, "error": "Category not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/categories', methods=['GET'])
def get_all_categories():
    """Get all categories"""
    try:
        categories = CategoryManager.get_all()
        return jsonify({"success": True, "data": categories, "count": len(categories)}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    """Delete category by ID"""
    try:
        result = CategoryManager.delete(category_id)
        return jsonify(result), 200 if result.get('success') else 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ============================================================================
# BUDGET SERVICE - /api/budgets
# ============================================================================

@app.route('/api/budgets', methods=['POST'])
def create_or_update_budget():
    """
    Create or update a budget
    Body: {budget_id, user_id, budget_name, budget_type, total_amount, start_date, end_date, is_active}
    """
    try:
        data = request.get_json()
        
        result = BudgetManager.save(
            budget_id=data.get('budget_id', 0),
            user_id=data.get('user_id'),
            budget_name=data.get('budget_name'),
            budget_type=data.get('budget_type'),
            total_amount=data.get('total_amount'),
            start_date=data.get('start_date'),
            end_date=data.get('end_date'),
            is_active=data.get('is_active', True)
        )
        
        status_code = 201 if result.get('success') and data.get('budget_id', 0) == 0 else 200
        return jsonify(result), status_code if result.get('success') else 400
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/budgets/<int:budget_id>', methods=['GET'])
def get_budget(budget_id):
    """Get budget by ID"""
    try:
        budget = BudgetManager.get_by_id(budget_id)
        if budget:
            return jsonify({"success": True, "data": budget}), 200
        return jsonify({"success": False, "error": "Budget not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/budgets', methods=['GET'])
def get_all_budgets():
    """Get all budgets"""
    try:
        budgets = BudgetManager.get_all()
        return jsonify({"success": True, "data": budgets, "count": len(budgets)}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/budgets/user/<int:user_id>', methods=['GET'])
def get_user_budgets(user_id):
    """Get all budgets for a specific user"""
    try:
        budgets = BudgetManager.get_by_user(user_id)
        return jsonify({"success": True, "data": budgets, "count": len(budgets)}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/budgets/<int:budget_id>', methods=['DELETE'])
def delete_budget(budget_id):
    """Delete budget by ID"""
    try:
        result = BudgetManager.delete(budget_id)
        return jsonify(result), 200 if result.get('success') else 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ============================================================================
# BUDGET RULE SERVICE - /api/budget-rules
# ============================================================================

@app.route('/api/budget-rules', methods=['POST'])
def create_or_update_budget_rule():
    """
    Create or update a budget rule
    Body: {rule_id, budget_id, category_id, limit_amount, alert_threshold}
    """
    try:
        data = request.get_json()
        
        result = BudgetRuleManager.save(
            rule_id=data.get('rule_id', 0),
            budget_id=data.get('budget_id'),
            category_id=data.get('category_id'),
            limit_amount=data.get('limit_amount'),
            alert_threshold=data.get('alert_threshold', 80.0)
        )
        
        status_code = 201 if result.get('success') and data.get('rule_id', 0) == 0 else 200
        return jsonify(result), status_code if result.get('success') else 400
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/budget-rules/<int:rule_id>', methods=['GET'])
def get_budget_rule(rule_id):
    """Get budget rule by ID"""
    try:
        rule = BudgetRuleManager.get_by_id(rule_id)
        if rule:
            return jsonify({"success": True, "data": rule}), 200
        return jsonify({"success": False, "error": "Budget rule not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/budget-rules', methods=['GET'])
def get_all_budget_rules():
    """Get all budget rules"""
    try:
        rules = BudgetRuleManager.get_all()
        return jsonify({"success": True, "data": rules, "count": len(rules)}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/budget-rules/budget/<int:budget_id>', methods=['GET'])
def get_budget_rules_for_budget(budget_id):
    """Get all rules for a specific budget"""
    try:
        rules = BudgetRuleManager.get_by_budget(budget_id)
        return jsonify({"success": True, "data": rules, "count": len(rules)}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/budget-rules/<int:rule_id>', methods=['DELETE'])
def delete_budget_rule(rule_id):
    """Delete budget rule by ID"""
    try:
        result = BudgetRuleManager.delete(rule_id)
        return jsonify(result), 200 if result.get('success') else 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ============================================================================
# TRANSACTION SERVICE - /api/transactions
# ============================================================================

@app.route('/api/transactions', methods=['POST'])
def create_or_update_transaction():
    """
    Create or update a transaction
    Body: {transaction_id, user_id, category_id, amount, transaction_date, description, payment_method}
    """
    try:
        data = request.get_json()
        
        result = TransactionManager.save(
            transaction_id=data.get('transaction_id', 0),
            user_id=data.get('user_id'),
            category_id=data.get('category_id'),
            amount=data.get('amount'),
            transaction_date=data.get('transaction_date'),
            description=data.get('description', ''),
            payment_method=data.get('payment_method', '')
        )
        
        status_code = 201 if result.get('success') and data.get('transaction_id', 0) == 0 else 200
        return jsonify(result), status_code if result.get('success') else 400
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/transactions/<int:transaction_id>', methods=['GET'])
def get_transaction(transaction_id):
    """Get transaction by ID"""
    try:
        transaction = TransactionManager.get_by_id(transaction_id)
        if transaction:
            return jsonify({"success": True, "data": transaction}), 200
        return jsonify({"success": False, "error": "Transaction not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/transactions', methods=['GET'])
def get_all_transactions():
    """Get all transactions (limited to 100)"""
    try:
        limit = request.args.get('limit', 100, type=int)
        transactions = TransactionManager.get_all(limit=limit)
        return jsonify({"success": True, "data": transactions, "count": len(transactions)}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/transactions/user/<int:user_id>', methods=['GET'])
def get_user_transactions(user_id):
    """Get all transactions for a specific user"""
    try:
        limit = request.args.get('limit', 50, type=int)
        transactions = TransactionManager.get_by_user(user_id, limit=limit)
        return jsonify({"success": True, "data": transactions, "count": len(transactions)}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/transactions/<int:transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    """Delete transaction by ID"""
    try:
        result = TransactionManager.delete(transaction_id)
        return jsonify(result), 200 if result.get('success') else 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({"success": False, "error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"success": False, "error": "Internal server error"}), 500


# ============================================================================
# RUN APPLICATION
# ============================================================================

if __name__ == '__main__':
    # For local development
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True)
