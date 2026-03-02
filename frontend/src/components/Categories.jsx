/**
 * Categories Component
 * Manages all category-related operations (CRUD)
 */

import React, { useState, useEffect } from 'react';
import { categoryService } from '../services/api';

const Categories = () => {
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [viewCategory, setViewCategory] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  
  // Form state
  const [formData, setFormData] = useState({
    category_name: '',
    description: '',
    icon: ''
  });

  useEffect(() => {
    fetchCategories();
  }, []);

  const fetchCategories = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await categoryService.getAll();
      setCategories(response.data.data || []);
    } catch (err) {
      setError('Failed to load categories: ' + (err.response?.data?.error || err.message));
    } finally {
      setLoading(false);
    }
  };

  const fetchCategoryById = async (id) => {
    setLoading(true);
    setError('');
    try {
      const response = await categoryService.getById(id);
      setViewCategory(response.data.data);
    } catch (err) {
      setError('Failed to load category: ' + (err.response?.data?.error || err.message));
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');
    
    try {
      await categoryService.create(formData);
      setSuccess('Category created successfully!');
      setFormData({ category_name: '', description: '', icon: '' });
      fetchCategories();
    } catch (err) {
      setError('Failed to create category: ' + (err.response?.data?.error || err.message));
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
      await categoryService.update(selectedCategory.category_id, formData);
      setSuccess('Category updated successfully!');
      setSelectedCategory(null);
      setFormData({ category_name: '', description: '', icon: '' });
      fetchCategories();
    } catch (err) {
      setError('Failed to update category: ' + (err.response?.data?.error || err.message));
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this category?')) return;
    
    setLoading(true);
    setError('');
    setSuccess('');
    
    try {
      await categoryService.delete(id);
      setSuccess('Category deleted successfully!');
      fetchCategories();
    } catch (err) {
      setError('Failed to delete category: ' + (err.response?.data?.error || err.message));
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = (category) => {
    setSelectedCategory(category);
    setFormData({
      category_name: category.category_name,
      description: category.description || '',
      icon: category.icon || ''
    });
    setViewCategory(null);
  };

  const handleCancel = () => {
    setSelectedCategory(null);
    setFormData({ category_name: '', description: '', icon: '' });
  };

  return (
    <div className="container">
      <h2>Categories Management</h2>
      
      {error && <div className="alert alert-error">{error}</div>}
      {success && <div className="alert alert-success">{success}</div>}
      {loading && <div className="loading">Loading...</div>}

      {/* Create/Update Form */}
      <div className="form-section">
        <h3>{selectedCategory ? 'Update Category' : 'Create New Category'}</h3>
        <form onSubmit={selectedCategory ? handleUpdate : handleCreate}>
          <div className="form-group">
            <label>Category Name:</label>
            <input
              type="text"
              name="category_name"
              value={formData.category_name}
              onChange={handleInputChange}
              required
              placeholder="Enter category name"
            />
          </div>
          
          <div className="form-group">
            <label>Description:</label>
            <textarea
              name="description"
              value={formData.description}
              onChange={handleInputChange}
              placeholder="Enter description (optional)"
              rows="3"
            />
          </div>
          
          <div className="form-group">
            <label>Icon (emoji):</label>
            <input
              type="text"
              name="icon"
              value={formData.icon}
              onChange={handleInputChange}
              placeholder="Enter emoji (e.g., 🛒)"
              maxLength="10"
            />
          </div>
          
          <div className="form-actions">
            <button type="submit" className="btn btn-primary" disabled={loading}>
              {selectedCategory ? 'Update Category' : 'Create Category'}
            </button>
            {selectedCategory && (
              <button type="button" className="btn btn-secondary" onClick={handleCancel}>
                Cancel
              </button>
            )}
          </div>
        </form>
      </div>

      {/* Categories List */}
      <div className="table-section">
        <h3>All Categories</h3>
        <table className="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Icon</th>
              <th>Name</th>
              <th>Description</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {categories.length === 0 ? (
              <tr>
                <td colSpan="5" style={{ textAlign: 'center' }}>No categories found</td>
              </tr>
            ) : (
              categories.map(category => (
                <tr key={category.category_id}>
                  <td>{category.category_id}</td>
                  <td style={{ fontSize: '24px' }}>{category.icon || '📁'}</td>
                  <td>{category.category_name}</td>
                  <td>{category.description || 'N/A'}</td>
                  <td className="actions">
                    <button
                      className="btn btn-small btn-info"
                      onClick={() => fetchCategoryById(category.category_id)}
                    >
                      View
                    </button>
                    <button
                      className="btn btn-small btn-warning"
                      onClick={() => handleEdit(category)}
                    >
                      Edit
                    </button>
                    <button
                      className="btn btn-small btn-danger"
                      onClick={() => handleDelete(category.category_id)}
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

      {/* View Single Category */}
      {viewCategory && (
        <div className="view-section">
          <h3>Category Details</h3>
          <button className="btn btn-secondary" onClick={() => setViewCategory(null)}>
            Close
          </button>
          <div className="details">
            <p><strong>ID:</strong> {viewCategory.category_id}</p>
            <p><strong>Name:</strong> {viewCategory.category_name}</p>
            <p><strong>Icon:</strong> {viewCategory.icon || 'N/A'}</p>
            <p><strong>Description:</strong> {viewCategory.description || 'N/A'}</p>
            <p><strong>Created:</strong> {new Date(viewCategory.created_at).toLocaleString()}</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default Categories;
