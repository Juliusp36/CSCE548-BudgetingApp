/**
 * Budgets Component
 * Manages all budget-related operations (CRUD)
 * Includes subset query: Get budgets by user
 */

import React, { useState, useEffect } from 'react';
import { budgetService, userService } from '../services/api';

const Budgets = () => {
  const [budgets, setBudgets] = useState([]);
  const [users, setUsers] = useState([]);
  const [selectedBudget, setSelectedBudget] = useState(null);
  const [viewBudget, setViewBudget] = useState(null);
  const [filterUserId, setFilterUserId] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  
  const [formData, setFormData] = useState({
    user_id: '',
    budget_name: '',
    budget_type: 'moderate',
    total_amount: '',
    start_date: '',
    end_date: '',
    is_active: true
  });

  useEffect(() => {
    fetchBudgets();
    fetchUsers();
  }, []);

  const fetchBudgets = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await budgetService.getAll();
      setBudgets(response.data.data || []);
    } catch (err) {
      setError('Failed to load budgets: ' + (err.response?.data?.error || err.message));
    } finally {
      setLoading(false);
    }
  };

  const fetchUsers = async () => {
    try {
      const response = await userService.getAll();
      setUsers(response.data.data || []);
    } catch (err) {
      console.error('Failed to load users:', err);
    }
  };

  const fetchBudgetById = async (id) => {
    setLoading(true);
    setError('');
    try {
      const response = await budgetService.getById(id);
      setViewBudget(response.data.data);
    } catch (err) {
      setError('Failed to load budget: ' + (err.response?.data?.error || err.message));
    } finally {
      setLoading(false);
    }
  };

  // SUBSET QUERY: Get budgets for specific user
  const fetchBudgetsByUser = async (userId) => {
    if (!userId) {
      fetchBudgets();
      return;
    }
    
    setLoading(true);
    setError('');
    try {
      const response = await budgetService.getByUser(userId);
      setBudgets(response.data.data || []);
      setSuccess(`Showing budgets for user ${userId}`);
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      setError('Failed to filter budgets: ' + (err.response?.data?.error || err.message));
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const value = e.target.type === 'checkbox' ? e.target.checked : e.target.value;
    setFormData({
      ...formData,
      [e.target.name]: value
    });
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');
    
    try {
      await budgetService.create(formData);
      setSuccess('Budget created successfully!');
      setFormData({
        user_id: '',
        budget_name: '',
        budget_type: 'moderate',
        total_amount: '',
        start_date: '',
        end_date: '',
        is_active: true
      });
      fetchBudgets();
    } catch (err) {
      setError('Failed to create budget: ' + (err.response?.data?.error || err.message));
    } finally {
      setLoading(false);
    }
  };

  const handleUpdate = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');
    
    try {
      await budgetService.update(selectedBudget.budget_id, formData);
      setSuccess('Budget updated successfully!');
      setSelectedBudget(null);
      setFormData({
        user_id: '',
        budget_name: '',
        budget_type: 'moderate',
        total_amount: '',
        start_date: '',
        end_date: '',
        is_active: true
      });
      fetchBudgets();
    } catch (err) {
      setError('Failed to update budget: ' + (err.response?.data?.error || err.message));
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure? This will also delete all budget rules.')) return;
    
    setLoading(true);
    setError('');
    setSuccess('');
    
    try {
      await budgetService.delete(id);
      setSuccess('Budget deleted successfully!');
      fetchBudgets();
    } catch (err) {
      setError('Failed to delete budget: ' + (err.response?.data?.error || err.message));
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = (budget) => {
    setSelectedBudget(budget);
    setFormData({
      user_id: budget.user_id,
      budget_name: budget.budget_name,
      budget_type: budget.budget_type,
      total_amount: budget.total_amount,
      start_date: budget.start_date.split('T')[0],
      end_date: budget.end_date.split('T')[0],
      is_active: budget.is_active
    });
    setViewBudget(null);
  };

  const handleCancel = () => {
    setSelectedBudget(null);
    setFormData({
      user_id: '',
      budget_name: '',
      budget_type: 'moderate',
      total_amount: '',
      start_date: '',
      end_date: '',
      is_active: true
    });
  };

  return (
    <div className="container">
      <h2>Budgets Management</h2>
      
      {error && <div className="alert alert-error">{error}</div>}
      {success && <div className="alert alert-success">{success}</div>}
      {loading && <div className="loading">Loading...</div>}

      {/* Filter by User (Subset Query) */}
      <div className="filter-section">
        <h3>Filter Budgets</h3>
        <div className="form-group">
          <label>Filter by User:</label>
          <select
            value={filterUserId}
            onChange={(e) => {
              setFilterUserId(e.target.value);
              fetchBudgetsByUser(e.target.value);
            }}
          >
            <option value="">All Users</option>
            {users.map(user => (
              <option key={user.user_id} value={user.user_id}>
                {user.username} (ID: {user.user_id})
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Create/Update Form */}
      <div className="form-section">
        <h3>{selectedBudget ? 'Update Budget' : 'Create New Budget'}</h3>
        <form onSubmit={selectedBudget ? handleUpdate : handleCreate}>
          <div className="form-group">
            <label>User:</label>
            <select
              name="user_id"
              value={formData.user_id}
              onChange={handleInputChange}
              required
            >
              <option value="">Select User</option>
              {users.map(user => (
                <option key={user.user_id} value={user.user_id}>
                  {user.username}
                </option>
              ))}
            </select>
          </div>
          
          <div className="form-group">
            <label>Budget Name:</label>
            <input
              type="text"
              name="budget_name"
              value={formData.budget_name}
              onChange={handleInputChange}
              required
            />
          </div>
          
          <div className="form-group">
            <label>Budget Type:</label>
            <select
              name="budget_type"
              value={formData.budget_type}
              onChange={handleInputChange}
              required
            >
              <option value="strict">Strict</option>
              <option value="moderate">Moderate</option>
              <option value="custom">Custom</option>
            </select>
          </div>
          
          <div className="form-group">
            <label>Total Amount:</label>
            <input
              type="number"
              name="total_amount"
              value={formData.total_amount}
              onChange={handleInputChange}
              required
              step="0.01"
              min="0"
            />
          </div>
          
          <div className="form-group">
            <label>Start Date:</label>
            <input
              type="date"
              name="start_date"
              value={formData.start_date}
              onChange={handleInputChange}
              required
            />
          </div>
          
          <div className="form-group">
            <label>End Date:</label>
            <input
              type="date"
              name="end_date"
              value={formData.end_date}
              onChange={handleInputChange}
              required
            />
          </div>
          
          <div className="form-group">
            <label>
              <input
                type="checkbox"
                name="is_active"
                checked={formData.is_active}
                onChange={handleInputChange}
              />
              Active
            </label>
          </div>
          
          <div className="form-actions">
            <button type="submit" className="btn btn-primary" disabled={loading}>
              {selectedBudget ? 'Update Budget' : 'Create Budget'}
            </button>
            {selectedBudget && (
              <button type="button" className="btn btn-secondary" onClick={handleCancel}>
                Cancel
              </button>
            )}
          </div>
        </form>
      </div>

      {/* Budgets List */}
      <div className="table-section">
        <h3>All Budgets</h3>
        <table className="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>User ID</th>
              <th>Name</th>
              <th>Type</th>
              <th>Amount</th>
              <th>Period</th>
              <th>Active</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {budgets.length === 0 ? (
              <tr>
                <td colSpan="8" style={{ textAlign: 'center' }}>No budgets found</td>
              </tr>
            ) : (
              budgets.map(budget => (
                <tr key={budget.budget_id}>
                  <td>{budget.budget_id}</td>
                  <td>{budget.user_id}</td>
                  <td>{budget.budget_name}</td>
                  <td>{budget.budget_type}</td>
                  <td>${parseFloat(budget.total_amount).toFixed(2)}</td>
                  <td>
                    {new Date(budget.start_date).toLocaleDateString()} - {new Date(budget.end_date).toLocaleDateString()}
                  </td>
                  <td>{budget.is_active ? '✓' : '✗'}</td>
                  <td className="actions">
                    <button
                      className="btn btn-small btn-info"
                      onClick={() => fetchBudgetById(budget.budget_id)}
                    >
                      View
                    </button>
                    <button
                      className="btn btn-small btn-warning"
                      onClick={() => handleEdit(budget)}
                    >
                      Edit
                    </button>
                    <button
                      className="btn btn-small btn-danger"
                      onClick={() => handleDelete(budget.budget_id)}
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* View Single Budget */}
      {viewBudget && (
        <div className="view-section">
          <h3>Budget Details</h3>
          <button className="btn btn-secondary" onClick={() => setViewBudget(null)}>
            Close
          </button>
          <div className="details">
            <p><strong>ID:</strong> {viewBudget.budget_id}</p>
            <p><strong>User ID:</strong> {viewBudget.user_id}</p>
            <p><strong>Name:</strong> {viewBudget.budget_name}</p>
            <p><strong>Type:</strong> {viewBudget.budget_type}</p>
            <p><strong>Total Amount:</strong> ${parseFloat(viewBudget.total_amount).toFixed(2)}</p>
            <p><strong>Start Date:</strong> {new Date(viewBudget.start_date).toLocaleDateString()}</p>
            <p><strong>End Date:</strong> {new Date(viewBudget.end_date).toLocaleDateString()}</p>
            <p><strong>Active:</strong> {viewBudget.is_active ? 'Yes' : 'No'}</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default Budgets;
