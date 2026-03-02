/**
 * API Service
 * Handles all HTTP requests to the Flask backend
 * 
 * For local development: http://localhost:5001/api
 * For production (Render): Update BASE_URL to your Render URL
 */

import axios from 'axios';

// Base URL for API - change this when deploying
const BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001/api';

// Create axios instance with default config
const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// ============================================================================
// USER SERVICES
// ============================================================================

export const userService = {
  // Get all users
  getAll: () => api.get('/users'),
  
  // Get single user by ID
  getById: (id) => api.get(`/users/${id}`),
  
  // Create new user
  create: (userData) => api.post('/users', { ...userData, user_id: 0 }),
  
  // Update existing user
  update: (id, userData) => api.post('/users', { ...userData, user_id: id }),
  
  // Delete user
  delete: (id) => api.delete(`/users/${id}`),
};

// ============================================================================
// CATEGORY SERVICES
// ============================================================================

export const categoryService = {
  // Get all categories
  getAll: () => api.get('/categories'),
  
  // Get single category by ID
  getById: (id) => api.get(`/categories/${id}`),
  
  // Create new category
  create: (categoryData) => api.post('/categories', { ...categoryData, category_id: 0 }),
  
  // Update existing category
  update: (id, categoryData) => api.post('/categories', { ...categoryData, category_id: id }),
  
  // Delete category
  delete: (id) => api.delete(`/categories/${id}`),
};

// ============================================================================
// BUDGET SERVICES
// ============================================================================

export const budgetService = {
  // Get all budgets
  getAll: () => api.get('/budgets'),
  
  // Get single budget by ID
  getById: (id) => api.get(`/budgets/${id}`),
  
  // Get budgets for specific user (subset)
  getByUser: (userId) => api.get(`/budgets/user/${userId}`),
  
  // Create new budget
  create: (budgetData) => api.post('/budgets', { ...budgetData, budget_id: 0 }),
  
  // Update existing budget
  update: (id, budgetData) => api.post('/budgets', { ...budgetData, budget_id: id }),
  
  // Delete budget
  delete: (id) => api.delete(`/budgets/${id}`),
};

// ============================================================================
// BUDGET RULE SERVICES
// ============================================================================

export const budgetRuleService = {
  // Get all budget rules
  getAll: () => api.get('/budget-rules'),
  
  // Get single budget rule by ID
  getById: (id) => api.get(`/budget-rules/${id}`),
  
  // Get rules for specific budget (subset)
  getByBudget: (budgetId) => api.get(`/budget-rules/budget/${budgetId}`),
  
  // Create new budget rule
  create: (ruleData) => api.post('/budget-rules', { ...ruleData, rule_id: 0 }),
  
  // Update existing budget rule
  update: (id, ruleData) => api.post('/budget-rules', { ...ruleData, rule_id: id }),
  
  // Delete budget rule
  delete: (id) => api.delete(`/budget-rules/${id}`),
};

// ============================================================================
// TRANSACTION SERVICES
// ============================================================================

export const transactionService = {
  // Get all transactions (limited to 100)
  getAll: (limit = 100) => api.get('/transactions', { params: { limit } }),
  
  // Get single transaction by ID
  getById: (id) => api.get(`/transactions/${id}`),
  
  // Get transactions for specific user (subset)
  getByUser: (userId, limit = 50) => api.get(`/transactions/user/${userId}`, { params: { limit } }),
  
  // Create new transaction
  create: (transactionData) => api.post('/transactions', { ...transactionData, transaction_id: 0 }),
  
  // Update existing transaction
  update: (id, transactionData) => api.post('/transactions', { ...transactionData, transaction_id: id }),
  
  // Delete transaction
  delete: (id) => api.delete(`/transactions/${id}`),
};

// ============================================================================
// ERROR HANDLER
// ============================================================================

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export default api;
