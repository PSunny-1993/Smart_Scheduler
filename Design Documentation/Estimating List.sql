-- ===============================
-- 1. Table: customers (was builders)
-- ===============================
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    bill_to VARCHAR(255),
    fname VARCHAR(100),
    lname VARCHAR(100),
    phone VARCHAR(50),
    mob VARCHAR(50),
    street1 VARCHAR(255),
    street2 VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(100),
    postcode VARCHAR(20),
    email VARCHAR(255),
    on_stop BOOLEAN DEFAULT FALSE,
    is_unverified BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE
);

-- ===============================
-- 2. Table: tender_list (was estimating_list)
-- ===============================
CREATE TABLE tender_list (
    tender_id SERIAL PRIMARY KEY,
    tender_name VARCHAR(255) NOT NULL,
    tender_received_date DATE NOT NULL,
    tender_due_date DATE,
    remarks TEXT,
    is_not_quoting BOOLEAN DEFAULT FALSE,
    is_completed BOOLEAN DEFAULT FALSE,
    quote_created BOOLEAN DEFAULT FALSE,
    added_by VARCHAR(255),
    estimator VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    email_id VARCHAR(255) UNIQUE
);

-- ===============================
-- 3. Table: tender_list_customers (many-to-many)
-- ===============================
CREATE TABLE tender_list_customers (
    id SERIAL PRIMARY KEY,
    tender_id INTEGER NOT NULL REFERENCES tender_list(tender_id) ON DELETE CASCADE,
    customer_id INTEGER NOT NULL REFERENCES customers(customer_id) ON DELETE CASCADE
);

-- ===============================
-- 4. Table: completed_tender_list
-- ===============================
CREATE TABLE completed_tender_list (
    completed_tender_id SERIAL PRIMARY KEY,
    tender_name VARCHAR(255) NOT NULL,
    tender_received_date DATE NOT NULL,
    tender_due_date DATE,
    remarks TEXT,
    added_by VARCHAR(255),
    estimator VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    email_id VARCHAR(255) UNIQUE
);

-- ===============================
-- 5. Table: completed_tender_customers (many-to-many)
-- ===============================
CREATE TABLE completed_tender_customers (
    id SERIAL PRIMARY KEY,
    completed_tender_id INTEGER NOT NULL REFERENCES completed_tender_list(completed_tender_id) ON DELETE CASCADE,
    customer_id INTEGER NOT NULL REFERENCES customers(customer_id) ON DELETE CASCADE
);

-- ===============================
-- 6. Table: not_quoting_list
-- ===============================
CREATE TABLE not_quoting_list (
    not_quoting_id SERIAL PRIMARY KEY,
    tender_name VARCHAR(255) NOT NULL,
    tender_received_date DATE NOT NULL,
    tender_due_date DATE,
    remarks TEXT,
    added_by VARCHAR(255),
    estimator VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    email_id VARCHAR(255) UNIQUE
);

-- ===============================
-- 7. Table: not_quoting_customers (many-to-many)
-- ===============================
CREATE TABLE not_quoting_customers (
    id SERIAL PRIMARY KEY,
    not_quoting_id INTEGER NOT NULL REFERENCES not_quoting_list(not_quoting_id) ON DELETE CASCADE,
    customer_id INTEGER NOT NULL REFERENCES customers(customer_id) ON DELETE CASCADE
);


