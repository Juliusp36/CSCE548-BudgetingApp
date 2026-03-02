/**
 * Users Component
 * Manages all user-related operations (CRUD)
 */

import React, { useState, useEffect } from 'react';
import { userService } from '../services/api';

const Users = () => {
  const [users, setUsers] = useState([]);
  const [selectedUser, setSelectedUser] = useState(null);
  const [viewUser, setViewUser] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  
  // Form state
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password_hash: ''
  });

  // Load all users on component mount
  useEffect(() => {
    fetchUsers();
  }, []);

  // Fetch all users
  const fetchUsers = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await userService.getAll();
      setUsers(response.data.data || []);
    } catch (err) {
      setError('Failed to load users: ' + (err.response?.data?.error || err.message));
    } finally {
      setLoading(false);
    }
  };

  // Fetch single user by ID
  const fetchUserById = async (id) => {
    setLoading(true);
    setError('');
    try {
      const response = await userService.getById(id);
      setViewUser(response.data.data);
    } catch (err) {
      setError('Failed to load user: ' + (err.response?.data?.error || err.message));
    } finally {
      setLoading(false);
    }
  };

  // Handle form input changes
  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  // Handle create
  const handleCreate = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');
    
    try {
      await userService.create(formData);
      setSuccess('User created successfully!');
      setFormData({ username: '', email: '', password_hash: '' });
      fetchUsers(); // Refresh list
    } catch (err) {
      setError('Failed to create user: ' + (err.response?.data?.error || err.message));
    } finally {
      setLoading(false);
    }
  };

  // Handle update
  const handleUpdate = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');
    
    try {
      await userService.update(selectedUser.user_id, formData);
      setSuccess('User updated successfully!');
      setSelectedUser(null);
      setFormData({ username: '', email: '', password_hash: '' });
      fetchUsers(); // Refresh list
    } catch (err) {
      setError('Failed to update user: ' + (err.response?.data?.error || err.message));
    } finally {
      setLoading(false);
    }
  };

  // Handle delete
  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this user?')) return;
    
    setLoading(true);
    setError('');
    setSuccess('');
    
    try {
      await userService.delete(id);
      setSuccess('User deleted successfully!');
      fetchUsers(); // Refresh list
    } catch (err) {
      setError('Failed to delete user: ' + (err.response?.data?.error || err.message));
    } finally {
      setLoading(false);
    }
  };

  // Populate form for editing
  const handleEdit = (user) => {
    setSelectedUser(user);
    setFormData({
      username: user.username,
      email: user.email,
      password_hash: ''
    });
    setViewUser(null);
  };

  // Cancel edit
  const handleCancel = () => {
    setSelectedUser(null);
    setFormData({ username: '', email: '', password_hash: '' });
  };

  return (
    <div className="container">
      <h2>Users Management</h2>
      
      {/* Status Messages */}
      {error && <div className="alert alert-error">{error}</div>}
      {success && <div className="alert alert-success">{success}</div>}
      {loading && <div className="loading">Loading...</div>}

      {/* Create/Update Form */}
      <div className="form-section">
        <h3>{selectedUser ? 'Update User' : 'Create New User'}</h3>
        <form onSubmit={selectedUser ? handleUpdate : handleCreate}>
          <div className="form-group">
            <label>Username:</label>
            <input
              type="text"
              name="username"
              value={formData.username}
              onChange={handleInputChange}
              required
              placeholder="Enter username"
            />
          </div>
          
          <div className="form-group">
            <label>Email:</label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleInputChange}
              required
              placeholder="Enter email"
            />
          </div>
          
          <div className="form-group">
            <label>Password:</label>
            <input
              type="password"
              name="password_hash"
              value={formData.password_hash}
              onChange={handleInputChange}
              required={!selectedUser}
              placeholder={selectedUser ? "Leave blank to keep current" : "Enter password"}
            />
          </div>
          
          <div className="form-actions">
            <button type="submit" className="btn btn-primary" disabled={loading}>
              {selectedUser ? 'Update User' : 'Create User'}
            </button>
            {selectedUser && (
              <button type="button" className="btn btn-secondary" onClick={handleCancel}>
                Cancel
              </button>
            )}
          </div>
        </form>
      </div>

      {/* Users List */}
      <div className="table-section">
        <h3>All Users</h3>
        <table className="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Username</th>
              <th>Email</th>
              <th>Created At</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {users.length === 0 ? (
              <tr>
                <td colSpan="5" style={{ textAlign: 'center' }}>No users found</td>
              </tr>
            ) : (
              users.map(user => (
                <tr key={user.user_id}>
                  <td>{user.user_id}</td>
                  <td>{user.username}</td>
                  <td>{user.email}</td>
                  <td>{new Date(user.created_at).toLocaleDateString()}</td>
                  <td className="actions">
                    <button
                      className="btn btn-small btn-info"
                      onClick={() => fetchUserById(user.user_id)}
                    >
                      View
                    </button>
                    <button
                      className="btn btn-small btn-warning"
                      onClick={() => handleEdit(user)}
                    >
                      Edit
                    </button>
                    <button
                      className="btn btn-small btn-danger"
                      onClick={() => handleDelete(user.user_id)}
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

      {/* View Single User */}
      {viewUser && (
        <div className="view-section">
          <h3>User Details</h3>
          <button className="btn btn-secondary" onClick={() => setViewUser(null)}>
            Close
          </button>
          <div className="details">
            <p><strong>ID:</strong> {viewUser.user_id}</p>
            <p><strong>Username:</strong> {viewUser.username}</p>
            <p><strong>Email:</strong> {viewUser.email}</p>
            <p><strong>Created:</strong> {new Date(viewUser.created_at).toLocaleString()}</p>
            <p><strong>Updated:</strong> {new Date(viewUser.updated_at).toLocaleString()}</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default Users;
