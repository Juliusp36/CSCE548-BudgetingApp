-- Budget Tracking Application Database Schema
-- Author: Graduate Student Project
-- Database: MySQL

DROP DATABASE IF EXISTS budget_tracker;
CREATE DATABASE budget_tracker;
USE budget_tracker;

-- Table 1: Users
-- Stores user account information
CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT chk_email_format CHECK (email LIKE '%_@__%.__%')
);

-- Table 2: Categories
-- Defines spending categories (food, entertainment, etc.)
CREATE TABLE categories (
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    category_name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    icon VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table 3: Budgets
-- Stores different budget configurations for users
CREATE TABLE budgets (
    budget_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    budget_name VARCHAR(100) NOT NULL,
    budget_type ENUM('strict', 'moderate', 'custom') NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_budget_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    CONSTRAINT chk_budget_amount CHECK (total_amount > 0),
    CONSTRAINT chk_budget_dates CHECK (end_date >= start_date)
);

-- Table 4: Budget Rules
-- Defines spending limits for each category within a budget
CREATE TABLE budget_rules (
    rule_id INT PRIMARY KEY AUTO_INCREMENT,
    budget_id INT NOT NULL,
    category_id INT NOT NULL,
    limit_amount DECIMAL(10, 2) NOT NULL,
    alert_threshold DECIMAL(5, 2) DEFAULT 80.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_rule_budget FOREIGN KEY (budget_id) REFERENCES budgets(budget_id) ON DELETE CASCADE,
    CONSTRAINT fk_rule_category FOREIGN KEY (category_id) REFERENCES categories(category_id) ON DELETE CASCADE,
    CONSTRAINT chk_limit_amount CHECK (limit_amount > 0),
    CONSTRAINT chk_alert_threshold CHECK (alert_threshold BETWEEN 0 AND 100),
    CONSTRAINT unique_budget_category UNIQUE (budget_id, category_id)
);

-- Table 5: Transactions
-- Records individual spending entries
CREATE TABLE transactions (
    transaction_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    category_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    transaction_date DATE NOT NULL,
    description VARCHAR(255),
    payment_method VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_transaction_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    CONSTRAINT fk_transaction_category FOREIGN KEY (category_id) REFERENCES categories(category_id) ON DELETE RESTRICT,
    CONSTRAINT chk_transaction_amount CHECK (amount > 0)
);

-- Create indexes for better query performance
CREATE INDEX idx_user_email ON users(email);
CREATE INDEX idx_budget_user ON budgets(user_id);
CREATE INDEX idx_budget_active ON budgets(is_active);
CREATE INDEX idx_transaction_user ON transactions(user_id);
CREATE INDEX idx_transaction_date ON transactions(transaction_date);
CREATE INDEX idx_transaction_category ON transactions(category_id);
CREATE INDEX idx_budget_rule_budget ON budget_rules(budget_id);

-- Create views for common queries
CREATE VIEW active_budgets AS
SELECT 
    b.budget_id,
    b.user_id,
    u.username,
    b.budget_name,
    b.budget_type,
    b.total_amount,
    b.start_date,
    b.end_date
FROM budgets b
JOIN users u ON b.user_id = u.user_id
WHERE b.is_active = TRUE;

CREATE VIEW transaction_summary AS
SELECT 
    t.transaction_id,
    u.username,
    c.category_name,
    t.amount,
    t.transaction_date,
    t.description,
    t.payment_method
FROM transactions t
JOIN users u ON t.user_id = u.user_id
JOIN categories c ON t.category_id = c.category_id
ORDER BY t.transaction_date DESC;
