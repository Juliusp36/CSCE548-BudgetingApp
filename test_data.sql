-- Test Data for Budget Tracking Application
-- This script populates all tables with realistic test data
-- Total rows: 100+ across all tables

USE budget_tracker;

-- Insert Users (10 users)
INSERT INTO users (username, email, password_hash) VALUES
('john_doe', 'john.doe@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzS7oBPqSS'),
('jane_smith', 'jane.smith@email.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW'),
('mike_johnson', 'mike.j@email.com', '$2b$12$KIXZaYVK2fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga32lW'),
('sarah_williams', 'sarah.w@email.com', '$2b$12$MIXZaYVK3fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga33lW'),
('david_brown', 'david.b@email.com', '$2b$12$NIXZaYVK4fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga34lW'),
('emily_davis', 'emily.d@email.com', '$2b$12$OIXZaYVK5fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga35lW'),
('robert_miller', 'robert.m@email.com', '$2b$12$PIXZaYVK6fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga36lW'),
('lisa_wilson', 'lisa.w@email.com', '$2b$12$QIXZaYVK7fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga37lW'),
('james_moore', 'james.m@email.com', '$2b$12$RIXZaYVK8fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga38lW'),
('amanda_taylor', 'amanda.t@email.com', '$2b$12$SIXZaYVK9fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga39lW');

-- Insert Categories (12 categories)
INSERT INTO categories (category_name, description, icon) VALUES
('Groceries', 'Food and household items', '🛒'),
('Dining Out', 'Restaurants and takeout', '🍽️'),
('Transportation', 'Gas, public transit, rideshare', '🚗'),
('Utilities', 'Electric, water, internet, phone', '💡'),
('Entertainment', 'Movies, games, streaming services', '🎬'),
('Healthcare', 'Medical expenses, prescriptions', '🏥'),
('Shopping', 'Clothing, electronics, misc purchases', '🛍️'),
('Housing', 'Rent or mortgage payments', '🏠'),
('Education', 'Tuition, books, courses', '📚'),
('Fitness', 'Gym membership, sports equipment', '💪'),
('Travel', 'Vacation, flights, hotels', '✈️'),
('Savings', 'Emergency fund, investments', '💰');

-- Insert Budgets (15 budgets for various users)
INSERT INTO budgets (user_id, budget_name, budget_type, total_amount, start_date, end_date, is_active) VALUES
(1, 'January 2024 Strict', 'strict', 2000.00, '2024-01-01', '2024-01-31', FALSE),
(1, 'February 2024 Moderate', 'moderate', 2500.00, '2024-02-01', '2024-02-29', TRUE),
(2, 'Monthly Budget', 'moderate', 3000.00, '2024-02-01', '2024-02-29', TRUE),
(3, 'Saving for Vacation', 'strict', 1800.00, '2024-02-01', '2024-02-29', TRUE),
(4, 'Student Budget', 'strict', 1500.00, '2024-02-01', '2024-02-29', TRUE),
(5, 'Family Budget', 'moderate', 4000.00, '2024-02-01', '2024-02-29', TRUE),
(6, 'Custom Spending Plan', 'custom', 2800.00, '2024-02-01', '2024-02-29', TRUE),
(7, 'Minimal Lifestyle', 'strict', 1200.00, '2024-02-01', '2024-02-29', TRUE),
(8, 'Professional Budget', 'moderate', 3500.00, '2024-02-01', '2024-02-29', TRUE),
(9, 'Freelancer Budget', 'custom', 2200.00, '2024-02-01', '2024-02-29', TRUE),
(10, 'Retirement Prep', 'moderate', 2600.00, '2024-02-01', '2024-02-29', TRUE),
(1, 'Q1 2024 Planning', 'custom', 7500.00, '2024-01-01', '2024-03-31', FALSE),
(2, 'Emergency Fund Builder', 'strict', 1000.00, '2024-02-01', '2024-02-29', FALSE),
(3, 'Summer Prep', 'moderate', 3200.00, '2024-02-01', '2024-02-29', FALSE),
(4, 'Debt Reduction Plan', 'strict', 1600.00, '2024-02-01', '2024-02-29', FALSE);

-- Insert Budget Rules (40+ rules)
-- Rules for Budget 1 (User 1 - Strict)
INSERT INTO budget_rules (budget_id, category_id, limit_amount, alert_threshold) VALUES
(1, 1, 300.00, 80.00),
(1, 2, 150.00, 90.00),
(1, 3, 200.00, 75.00),
(1, 4, 250.00, 85.00),
(1, 5, 100.00, 80.00);

-- Rules for Budget 2 (User 1 - Moderate)
INSERT INTO budget_rules (budget_id, category_id, limit_amount, alert_threshold) VALUES
(2, 1, 400.00, 75.00),
(2, 2, 250.00, 80.00),
(2, 3, 300.00, 70.00),
(2, 4, 300.00, 85.00),
(2, 5, 200.00, 75.00),
(2, 7, 350.00, 80.00);

-- Rules for Budget 3 (User 2)
INSERT INTO budget_rules (budget_id, category_id, limit_amount, alert_threshold) VALUES
(3, 1, 500.00, 80.00),
(3, 2, 300.00, 75.00),
(3, 3, 250.00, 80.00),
(3, 4, 350.00, 85.00),
(3, 5, 250.00, 70.00),
(3, 7, 400.00, 75.00),
(3, 8, 1200.00, 90.00);

-- Rules for Budget 4 (User 3 - Saving for Vacation)
INSERT INTO budget_rules (budget_id, category_id, limit_amount, alert_threshold) VALUES
(4, 1, 250.00, 85.00),
(4, 2, 100.00, 90.00),
(4, 3, 150.00, 80.00),
(4, 4, 200.00, 85.00),
(4, 11, 500.00, 70.00);

-- Rules for Budget 5 (User 4 - Student)
INSERT INTO budget_rules (budget_id, category_id, limit_amount, alert_threshold) VALUES
(5, 1, 200.00, 80.00),
(5, 2, 100.00, 85.00),
(5, 3, 100.00, 90.00),
(5, 9, 600.00, 75.00),
(5, 5, 150.00, 70.00);

-- Rules for Budget 6 (User 5 - Family)
INSERT INTO budget_rules (budget_id, category_id, limit_amount, alert_threshold) VALUES
(6, 1, 800.00, 80.00),
(6, 2, 400.00, 75.00),
(6, 3, 350.00, 80.00),
(6, 4, 450.00, 85.00),
(6, 6, 300.00, 90.00),
(6, 7, 500.00, 75.00),
(6, 8, 1500.00, 95.00);

-- Rules for remaining budgets (condensed)
INSERT INTO budget_rules (budget_id, category_id, limit_amount, alert_threshold) VALUES
(7, 1, 300.00, 85.00),
(7, 3, 150.00, 90.00),
(7, 4, 200.00, 85.00),
(8, 1, 450.00, 80.00),
(8, 2, 350.00, 75.00),
(8, 5, 300.00, 70.00),
(9, 1, 350.00, 80.00),
(9, 3, 250.00, 75.00),
(10, 1, 400.00, 80.00),
(10, 12, 800.00, 70.00);

-- Insert Transactions (50+ transactions)
-- Transactions for User 1
INSERT INTO transactions (user_id, category_id, amount, transaction_date, description, payment_method) VALUES
(1, 1, 45.67, '2024-02-01', 'Whole Foods grocery run', 'Credit Card'),
(1, 1, 32.50, '2024-02-03', 'Trader Joes', 'Debit Card'),
(1, 2, 28.99, '2024-02-02', 'Chipotle lunch', 'Credit Card'),
(1, 3, 45.00, '2024-02-05', 'Gas station fill-up', 'Credit Card'),
(1, 5, 15.99, '2024-02-04', 'Netflix subscription', 'Credit Card'),
(1, 1, 78.34, '2024-02-07', 'Costco bulk shopping', 'Debit Card'),
(1, 2, 42.50, '2024-02-08', 'Dinner at Italian restaurant', 'Credit Card'),
(1, 4, 125.00, '2024-02-01', 'Electric bill', 'Auto-pay'),
(1, 4, 89.99, '2024-02-01', 'Internet bill', 'Auto-pay'),
(1, 7, 156.78, '2024-02-10', 'New running shoes', 'Credit Card');

-- Transactions for User 2
INSERT INTO transactions (user_id, category_id, amount, transaction_date, description, payment_method) VALUES
(2, 1, 92.45, '2024-02-02', 'Weekly groceries', 'Debit Card'),
(2, 2, 65.00, '2024-02-03', 'Sushi dinner', 'Credit Card'),
(2, 3, 38.50, '2024-02-04', 'Uber to work', 'Credit Card'),
(2, 8, 1200.00, '2024-02-01', 'Monthly rent', 'Check'),
(2, 5, 45.00, '2024-02-05', 'Movie tickets', 'Credit Card'),
(2, 1, 56.78, '2024-02-09', 'Farmers market', 'Cash'),
(2, 7, 234.99, '2024-02-11', 'New laptop mouse', 'Credit Card'),
(2, 4, 78.50, '2024-02-01', 'Water bill', 'Auto-pay'),
(2, 2, 34.25, '2024-02-12', 'Coffee shop', 'Debit Card'),
(2, 3, 52.00, '2024-02-13', 'Gas', 'Credit Card');

-- Transactions for User 3
INSERT INTO transactions (user_id, category_id, amount, transaction_date, description, payment_method) VALUES
(3, 1, 67.89, '2024-02-01', 'Grocery shopping', 'Credit Card'),
(3, 11, 350.00, '2024-02-05', 'Flight deposit for summer trip', 'Credit Card'),
(3, 3, 25.00, '2024-02-06', 'Lyft ride', 'Credit Card'),
(3, 2, 18.50, '2024-02-07', 'Fast food lunch', 'Debit Card'),
(3, 4, 145.00, '2024-02-01', 'Utilities', 'Auto-pay'),
(3, 1, 43.21, '2024-02-10', 'Groceries', 'Debit Card'),
(3, 5, 12.99, '2024-02-08', 'Spotify premium', 'Credit Card'),
(3, 3, 48.00, '2024-02-14', 'Gas station', 'Credit Card'),
(3, 2, 55.75, '2024-02-15', 'Dinner date', 'Credit Card'),
(3, 7, 89.99, '2024-02-12', 'New headphones', 'Credit Card');

-- Transactions for User 4 (Student)
INSERT INTO transactions (user_id, category_id, amount, transaction_date, description, payment_method) VALUES
(4, 9, 450.00, '2024-02-01', 'Textbooks for semester', 'Debit Card'),
(4, 1, 34.56, '2024-02-03', 'Groceries', 'Debit Card'),
(4, 2, 12.00, '2024-02-04', 'Campus cafeteria', 'Student Card'),
(4, 3, 2.50, '2024-02-05', 'Bus fare', 'Cash'),
(4, 5, 8.99, '2024-02-02', 'Gaming subscription', 'Credit Card'),
(4, 1, 28.90, '2024-02-08', 'Meal prep groceries', 'Debit Card'),
(4, 2, 15.50, '2024-02-10', 'Pizza night', 'Cash'),
(4, 9, 75.00, '2024-02-06', 'Online course', 'Credit Card'),
(4, 3, 2.50, '2024-02-12', 'Bus fare', 'Cash'),
(4, 1, 41.23, '2024-02-14', 'Grocery store', 'Debit Card');

-- Transactions for User 5 (Family)
INSERT INTO transactions (user_id, category_id, amount, transaction_date, description, payment_method) VALUES
(5, 8, 1500.00, '2024-02-01', 'Mortgage payment', 'Auto-pay'),
(5, 1, 187.45, '2024-02-02', 'Costco family shopping', 'Credit Card'),
(5, 6, 125.00, '2024-02-05', 'Pediatrician visit copay', 'HSA Card'),
(5, 3, 65.00, '2024-02-06', 'Gas for minivan', 'Credit Card'),
(5, 2, 78.50, '2024-02-07', 'Family dinner out', 'Credit Card'),
(5, 4, 234.56, '2024-02-01', 'Electric and gas', 'Auto-pay'),
(5, 7, 345.99, '2024-02-09', 'Kids clothing', 'Credit Card'),
(5, 1, 156.78, '2024-02-11', 'Grocery run', 'Debit Card'),
(5, 5, 45.00, '2024-02-10', 'Family movie night', 'Cash'),
(5, 6, 89.00, '2024-02-13', 'Prescription refills', 'HSA Card');

-- Additional transactions to ensure 50+ total
INSERT INTO transactions (user_id, category_id, amount, transaction_date, description, payment_method) VALUES
(6, 1, 95.00, '2024-02-01', 'Weekly groceries', 'Credit Card'),
(6, 3, 42.00, '2024-02-02', 'Gas', 'Debit Card'),
(7, 1, 58.90, '2024-02-03', 'Groceries', 'Cash'),
(7, 3, 35.00, '2024-02-04', 'Public transit pass', 'Debit Card'),
(8, 2, 89.50, '2024-02-05', 'Business lunch', 'Corporate Card'),
(8, 5, 125.00, '2024-02-06', 'Theater tickets', 'Credit Card'),
(9, 1, 72.34, '2024-02-07', 'Groceries', 'Debit Card'),
(9, 3, 48.00, '2024-02-08', 'Gas', 'Credit Card'),
(10, 12, 500.00, '2024-02-01', 'Investment contribution', 'Transfer'),
(10, 1, 64.50, '2024-02-09', 'Groceries', 'Credit Card');

-- Verify row counts
SELECT 'Users' as TableName, COUNT(*) as RowCount FROM users
UNION ALL
SELECT 'Categories', COUNT(*) FROM categories
UNION ALL
SELECT 'Budgets', COUNT(*) FROM budgets
UNION ALL
SELECT 'Budget Rules', COUNT(*) FROM budget_rules
UNION ALL
SELECT 'Transactions', COUNT(*) FROM transactions
UNION ALL
SELECT 'TOTAL', 
    (SELECT COUNT(*) FROM users) +
    (SELECT COUNT(*) FROM categories) +
    (SELECT COUNT(*) FROM budgets) +
    (SELECT COUNT(*) FROM budget_rules) +
    (SELECT COUNT(*) FROM transactions);
