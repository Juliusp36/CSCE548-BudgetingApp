import React, { useState, useEffect } from 'react';
import { budgetRuleService, budgetService, categoryService } from '../services/api';

const BudgetRules = () => {
  const [rules, setRules] = useState([]);
  const [budgets, setBudgets] = useState([]);
  const [categories, setCategories] = useState([]);
  const [selectedRule, setSelectedRule] = useState(null);
  const [viewRule, setViewRule] = useState(null);
  const [filterBudgetId, setFilterBudgetId] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  
  const [formData, setFormData] = useState({
    budget_id: '',
    category_id: '',
    limit_amount: '',
    alert_threshold: '80'
  });

  useEffect(() => {
    fetchRules();
    fetchBudgets();
    fetchCategories();
  }, []);

  const fetchRules = async () => {
    setLoading(true);
    try {
      const response = await budgetRuleService.getAll();
      setRules(response.data.data || []);
    } catch (err) {
      setError('Failed to load rules');
    } finally {
      setLoading(false);
    }
  };

  const fetchBudgets = async () => {
    try {
      const response = await budgetService.getAll();
      setBudgets(response.data.data || []);
    } catch (err) {
      console.error('Failed to load budgets');
    }
  };

  const fetchCategories = async () => {
    try {
      const response = await categoryService.getAll();
      setCategories(response.data.data || []);
    } catch (err) {
      console.error('Failed to load categories');
    }
  };

  const fetchRuleById = async (id) => {
    try {
      const response = await budgetRuleService.getById(id);
      setViewRule(response.data.data);
    } catch (err) {
      setError('Failed to load rule');
    }
  };

  // SUBSET QUERY
  const fetchRulesByBudget = async (budgetId) => {
    if (!budgetId) {
      fetchRules();
      return;
    }
    
    setLoading(true);
    try {
      const response = await budgetRuleService.getByBudget(budgetId);
      setRules(response.data.data || []);
      setSuccess(`Showing rules for budget ${budgetId}`);
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      setError('Failed to filter rules');
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await budgetRuleService.create(formData);
      setSuccess('Rule created!');
      setFormData({ budget_id: '', category_id: '', limit_amount: '', alert_threshold: '80' });
      fetchRules();
    } catch (err) {
      setError('Failed to create rule: ' + (err.response?.data?.error || err.message));
    } finally {
      setLoading(false);
    }
  };

  const handleUpdate = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await budgetRuleService.update(selectedRule.rule_id, formData);
      setSuccess('Rule updated!');
      setSelectedRule(null);
      setFormData({ budget_id: '', category_id: '', limit_amount: '', alert_threshold: '80' });
      fetchRules();
    } catch (err) {
      setError('Failed to update: ' + (err.response?.data?.error || err.message));
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Delete this rule?')) return;
    try {
      await budgetRuleService.delete(id);
      setSuccess('Rule deleted!');
      fetchRules();
    } catch (err) {
      setError('Failed to delete');
    }
  };

  const handleEdit = (rule) => {
    setSelectedRule(rule);
    setFormData({
      budget_id: rule.budget_id,
      category_id: rule.category_id,
      limit_amount: rule.limit_amount,
      alert_threshold: rule.alert_threshold
    });
  };

  return (
    <div className="container">
      <h2>Budget Rules Management</h2>
      {error && <div className="alert alert-error">{error}</div>}
      {success && <div className="alert alert-success">{success}</div>}
      
      {/* Filter by Budget */}
      <div className="filter-section">
        <h3>Filter Rules</h3>
        <select value={filterBudgetId} onChange={(e) => { setFilterBudgetId(e.target.value); fetchRulesByBudget(e.target.value); }}>
          <option value="">All Budgets</option>
          {budgets.map(b => <option key={b.budget_id} value={b.budget_id}>{b.budget_name} (ID: {b.budget_id})</option>)}
        </select>
      </div>

      {/* Form */}
      <div className="form-section">
        <h3>{selectedRule ? 'Update Rule' : 'Create Rule'}</h3>
        <form onSubmit={selectedRule ? handleUpdate : handleCreate}>
          <div className="form-group">
            <label>Budget:</label>
            <select name="budget_id" value={formData.budget_id} onChange={handleInputChange} required>
              <option value="">Select Budget</option>
              {budgets.map(b => <option key={b.budget_id} value={b.budget_id}>{b.budget_name}</option>)}
            </select>
          </div>
          <div className="form-group">
            <label>Category:</label>
            <select name="category_id" value={formData.category_id} onChange={handleInputChange} required>
              <option value="">Select Category</option>
              {categories.map(c => <option key={c.category_id} value={c.category_id}>{c.category_name}</option>)}
            </select>
          </div>
          <div className="form-group">
            <label>Limit Amount:</label>
            <input type="number" name="limit_amount" value={formData.limit_amount} onChange={handleInputChange} required step="0.01" min="0" />
          </div>
          <div className="form-group">
            <label>Alert Threshold (%):</label>
            <input type="number" name="alert_threshold" value={formData.alert_threshold} onChange={handleInputChange} required min="0" max="100" />
          </div>
          <div className="form-actions">
            <button type="submit" className="btn btn-primary">{selectedRule ? 'Update' : 'Create'}</button>
            {selectedRule && <button type="button" className="btn btn-secondary" onClick={() => setSelectedRule(null)}>Cancel</button>}
          </div>
        </form>
      </div>

      {/* Table */}
      <div className="table-section">
        <h3>All Budget Rules</h3>
        <table className="data-table">
          <thead>
            <tr><th>ID</th><th>Budget ID</th><th>Category ID</th><th>Limit</th><th>Alert %</th><th>Actions</th></tr>
          </thead>
          <tbody>
            {rules.length === 0 ? (
              <tr><td colSpan="6" style={{textAlign: 'center'}}>No rules found</td></tr>
            ) : (
              rules.map(rule => (
                <tr key={rule.rule_id}>
                  <td>{rule.rule_id}</td>
                  <td>{rule.budget_id}</td>
                  <td>{rule.category_id}</td>
                  <td>${parseFloat(rule.limit_amount).toFixed(2)}</td>
                  <td>{rule.alert_threshold}%</td>
                  <td className="actions">
                    <button className="btn btn-small btn-info" onClick={() => fetchRuleById(rule.rule_id)}>View</button>
                    <button className="btn btn-small btn-warning" onClick={() => handleEdit(rule)}>Edit</button>
                    <button className="btn btn-small btn-danger" onClick={() => handleDelete(rule.rule_id)}>Delete</button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* View */}
      {viewRule && (
        <div className="view-section">
          <h3>Rule Details</h3>
          <button className="btn btn-secondary" onClick={() => setViewRule(null)}>Close</button>
          <div className="details">
            <p><strong>ID:</strong> {viewRule.rule_id}</p>
            <p><strong>Budget ID:</strong> {viewRule.budget_id}</p>
            <p><strong>Category ID:</strong> {viewRule.category_id}</p>
            <p><strong>Limit:</strong> ${parseFloat(viewRule.limit_amount).toFixed(2)}</p>
            <p><strong>Alert Threshold:</strong> {viewRule.alert_threshold}%</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default BudgetRules;
