import React, { useState, useEffect } from 'react';
import { transactionService, userService, categoryService } from '../services/api';

const Transactions = () => {
  const [transactions, setTransactions] = useState([]);
  const [users, setUsers] = useState([]);
  const [categories, setCategories] = useState([]);
  const [selectedTransaction, setSelectedTransaction] = useState(null);
  const [viewTransaction, setViewTransaction] = useState(null);
  const [filterUserId, setFilterUserId] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  
  const [formData, setFormData] = useState({
    user_id: '',
    category_id: '',
    amount: '',
    transaction_date: new Date().toISOString().split('T')[0],
    description: '',
    payment_method: ''
  });

  useEffect(() => {
    fetchTransactions();
    fetchUsers();
    fetchCategories();
  }, []);

  const fetchTransactions = async () => {
    setLoading(true);
    try {
      const response = await transactionService.getAll(100);
      setTransactions(response.data.data || []);
    } catch (err) {
      setError('Failed to load transactions');
    } finally {
      setLoading(false);
    }
  };

  const fetchUsers = async () => {
    try {
      const response = await userService.getAll();
      setUsers(response.data.data || []);
    } catch (err) {
      console.error('Failed to load users');
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

  const fetchTransactionById = async (id) => {
    try {
      const response = await transactionService.getById(id);
      setViewTransaction(response.data.data);
    } catch (err) {
      setError('Failed to load transaction');
    }
  };

  // SUBSET QUERY
  const fetchTransactionsByUser = async (userId) => {
    if (!userId) {
      fetchTransactions();
      return;
    }
    
    setLoading(true);
    try {
      const response = await transactionService.getByUser(userId, 50);
      setTransactions(response.data.data || []);
      setSuccess(`Showing transactions for user ${userId}`);
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      setError('Failed to filter transactions');
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
      const response = await transactionService.create(formData);
      setSuccess('Transaction created!');
      if (response.data.warnings && response.data.warnings.length > 0) {
        setError('Warnings: ' + response.data.warnings.join(', '));
      }
      setFormData({
        user_id: '',
        category_id: '',
        amount: '',
        transaction_date: new Date().toISOString().split('T')[0],
        description: '',
        payment_method: ''
      });
      fetchTransactions();
    } catch (err) {
      setError('Failed: ' + (err.response?.data?.error || err.message));
    } finally {
      setLoading(false);
    }
  };

  const handleUpdate = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await transactionService.update(selectedTransaction.transaction_id, formData);
      setSuccess('Transaction updated!');
      setSelectedTransaction(null);
      setFormData({
        user_id: '',
        category_id: '',
        amount: '',
        transaction_date: new Date().toISOString().split('T')[0],
        description: '',
        payment_method: ''
      });
      fetchTransactions();
    } catch (err) {
      setError('Failed: ' + (err.response?.data?.error || err.message));
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Delete this transaction?')) return;
    try {
      await transactionService.delete(id);
      setSuccess('Transaction deleted!');
      fetchTransactions();
    } catch (err) {
      setError('Failed to delete');
    }
  };

  const handleEdit = (txn) => {
    setSelectedTransaction(txn);
    setFormData({
      user_id: txn.user_id,
      category_id: txn.category_id,
      amount: txn.amount,
      transaction_date: txn.transaction_date.split('T')[0],
      description: txn.description || '',
      payment_method: txn.payment_method || ''
    });
  };

  return (
    <div className="container">
      <h2>Transactions Management</h2>
      {error && <div className="alert alert-error">{error}</div>}
      {success && <div className="alert alert-success">{success}</div>}
      
      {/* Filter */}
      <div className="filter-section">
        <h3>Filter Transactions</h3>
        <select value={filterUserId} onChange={(e) => { setFilterUserId(e.target.value); fetchTransactionsByUser(e.target.value); }}>
          <option value="">All Users</option>
          {users.map(u => <option key={u.user_id} value={u.user_id}>{u.username} (ID: {u.user_id})</option>)}
        </select>
      </div>

      {/* Form */}
      <div className="form-section">
        <h3>{selectedTransaction ? 'Update Transaction' : 'Create Transaction'}</h3>
        <form onSubmit={selectedTransaction ? handleUpdate : handleCreate}>
          <div className="form-group">
            <label>User:</label>
            <select name="user_id" value={formData.user_id} onChange={handleInputChange} required>
              <option value="">Select User</option>
              {users.map(u => <option key={u.user_id} value={u.user_id}>{u.username}</option>)}
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
            <label>Amount:</label>
            <input type="number" name="amount" value={formData.amount} onChange={handleInputChange} required step="0.01" min="0" />
          </div>
          <div className="form-group">
            <label>Date:</label>
            <input type="date" name="transaction_date" value={formData.transaction_date} onChange={handleInputChange} required />
          </div>
          <div className="form-group">
            <label>Description:</label>
            <input type="text" name="description" value={formData.description} onChange={handleInputChange} placeholder="Optional" />
          </div>
          <div className="form-group">
            <label>Payment Method:</label>
            <input type="text" name="payment_method" value={formData.payment_method} onChange={handleInputChange} placeholder="e.g., Credit Card" />
          </div>
          <div className="form-actions">
            <button type="submit" className="btn btn-primary">{selectedTransaction ? 'Update' : 'Create'}</button>
            {selectedTransaction && <button type="button" className="btn btn-secondary" onClick={() => setSelectedTransaction(null)}>Cancel</button>}
          </div>
        </form>
      </div>

      {/* Table */}
      <div className="table-section">
        <h3>All Transactions</h3>
        <table className="data-table">
          <thead>
            <tr><th>ID</th><th>User</th><th>Category</th><th>Amount</th><th>Date</th><th>Actions</th></tr>
          </thead>
          <tbody>
            {transactions.length === 0 ? (
              <tr><td colSpan="6" style={{textAlign: 'center'}}>No transactions found</td></tr>
            ) : (
              transactions.map(txn => (
                <tr key={txn.transaction_id}>
                  <td>{txn.transaction_id}</td>
                  <td>{txn.username || txn.user_id}</td>
                  <td>{txn.category_name || txn.category_id}</td>
                  <td>${parseFloat(txn.amount).toFixed(2)}</td>
                  <td>{new Date(txn.transaction_date).toLocaleDateString()}</td>
                  <td className="actions">
                    <button className="btn btn-small btn-info" onClick={() => fetchTransactionById(txn.transaction_id)}>View</button>
                    <button className="btn btn-small btn-warning" onClick={() => handleEdit(txn)}>Edit</button>
                    <button className="btn btn-small btn-danger" onClick={() => handleDelete(txn.transaction_id)}>Delete</button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* View */}
      {viewTransaction && (
        <div className="view-section">
          <h3>Transaction Details</h3>
          <button className="btn btn-secondary" onClick={() => setViewTransaction(null)}>Close</button>
          <div className="details">
            <p><strong>ID:</strong> {viewTransaction.transaction_id}</p>
            <p><strong>User:</strong> {viewTransaction.username} (ID: {viewTransaction.user_id})</p>
            <p><strong>Category:</strong> {viewTransaction.category_name}</p>
            <p><strong>Amount:</strong> ${parseFloat(viewTransaction.amount).toFixed(2)}</p>
            <p><strong>Date:</strong> {new Date(viewTransaction.transaction_date).toLocaleDateString()}</p>
            <p><strong>Description:</strong> {viewTransaction.description || 'N/A'}</p>
            <p><strong>Payment Method:</strong> {viewTransaction.payment_method || 'N/A'}</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default Transactions;
