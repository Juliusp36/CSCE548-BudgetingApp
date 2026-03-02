/**
 * Main App Component
 * Handles routing and navigation between all CRUD components
 */

import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, Navigate } from 'react-router-dom';
import './App.css';

// Import all components
import Users from './Users';
import Categories from './Categories';
import Budgets from './Budgets';
import BudgetRules from './BudgetRules';
import Transactions from './Transactions';

function App() {
  return (
    <Router>
      <div className="App">
        {/* Navigation Bar */}
        <nav className="navbar">
          <div className="nav-brand">
            <h1>💰 Budget Tracker</h1>
            <p>Full Stack Application - CSCE 548</p>
          </div>
          <ul className="nav-links">
            <li><Link to="/users">Users</Link></li>
            <li><Link to="/categories">Categories</Link></li>
            <li><Link to="/budgets">Budgets</Link></li>
            <li><Link to="/budget-rules">Budget Rules</Link></li>
            <li><Link to="/transactions">Transactions</Link></li>
          </ul>
        </nav>

        {/* Main Content */}
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Navigate to="/users" replace />} />
            <Route path="/users" element={<Users />} />
            <Route path="/categories" element={<Categories />} />
            <Route path="/budgets" element={<Budgets />} />
            <Route path="/budget-rules" element={<BudgetRules />} />
            <Route path="/transactions" element={<Transactions />} />
          </Routes>
        </main>

        {/* Footer */}
        <footer className="footer">
          <p>Budget Tracker © 2026 | Built with React + Flask + MySQL</p>
          <p>Projects 1, 2, and 3 - Complete Full Stack Application</p>
        </footer>
      </div>
    </Router>
  );
}

export default App;
