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
) ENGINE=InnoDB;

-- Table 2: Categories
-- Defines spending categories (food, entertainment, etc.)
CREATE TABLE categories (
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    category_name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    icon VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- Table 3: Budgets
-- Stores different budget configurations for users
CREATE TABLE budgets (
    budget_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    budget_name VARCHAR(100) NOT NULL,
    budget_type ENUM('strict', 'moderate', 'custom') NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    is_active TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_budget_amount CHECK (total_amount > 0),
    CONSTRAINT chk_budget_dates CHECK (end_date >= start_date),
    
    INDEX idx_budget_user (user_id),
    INDEX idx_budget_active (is_active),
    
    CONSTRAINT fk_budget_user 
        FOREIGN KEY (user_id) 
        REFERENCES users(user_id) 
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;

-- Table 4: Budget Rules
-- Defines spending limits for each category within a budget
CREATE TABLE budget_rules (
    rule_id INT PRIMARY KEY AUTO_INCREMENT,
    budget_id INT NOT NULL,
    category_id INT NOT NULL,
    limit_amount DECIMAL(10, 2) NOT NULL,
    alert_threshold DECIMAL(5, 2) DEFAULT 80.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_limit_amount CHECK (limit_amount > 0),
    CONSTRAINT chk_alert_threshold CHECK (alert_threshold BETWEEN 0 AND 100),
    CONSTRAINT unique_budget_category UNIQUE (budget_id, category_id),
    
    INDEX idx_budget_rule_budget (budget_id),
    INDEX idx_budget_rule_category (category_id),
    
    CONSTRAINT fk_rule_budget 
        FOREIGN KEY (budget_id) 
        REFERENCES budgets(budget_id) 
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_rule_category 
        FOREIGN KEY (category_id) 
        REFERENCES categories(category_id) 
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;

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
    
    CONSTRAINT chk_transaction_amount CHECK (amount > 0),
    
    INDEX idx_transaction_user (user_id),
    INDEX idx_transaction_date (transaction_date),
    INDEX idx_transaction_category (category_id),
    
    CONSTRAINT fk_transaction_user 
        FOREIGN KEY (user_id) 
        REFERENCES users(user_id) 
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_transaction_category 
        FOREIGN KEY (category_id) 
        REFERENCES categories(category_id) 
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE=InnoDB;

-- Additional index on user email
CREATE INDEX idx_user_email ON users(email);

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

-- Verify foreign keys were created
SELECT 
    'Foreign Keys Verification' AS info,
    COUNT(*) as total_foreign_keys
FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
WHERE TABLE_SCHEMA = 'budget_tracker'
AND REFERENCED_TABLE_NAME IS NOT NULL;

-- Show all foreign keys
SELECT 
    TABLE_NAME,
    COLUMN_NAME,
    CONSTRAINT_NAME,
    REFERENCED_TABLE_NAME,
    REFERENCED_COLUMN_NAME
FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
WHERE TABLE_SCHEMA = 'budget_tracker'
AND REFERENCED_TABLE_NAME IS NOT NULL
ORDER BY TABLE_NAME;