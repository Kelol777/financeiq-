-- FinanceIQ Schema
-- Dimension Tables

CREATE TABLE dim_date (
    date_id INT PRIMARY KEY,
    full_date DATE,
    year INT,
    quarter INT,
    month INT,
    month_name VARCHAR(20),
    week INT,
    day INT,
    day_name VARCHAR(20)
);


CREATE TABLE dim_account (
    account_id INT PRIMARY KEY,
    account_code VARCHAR(20),
    account_name VARCHAR(100),
    category VARCHAR(50)
);

CREATE TABLE dim_costcenter (
    costcenter_id INT PRIMARY KEY,
    costcenter_code VARCHAR(20),
    costcenter_name VARCHAR(100),
    department VARCHAR(50),
    manager VARCHAR(100)
);


CREATE TABLE fact_transaction (
    transaction_id INT PRIMARY KEY,
    date_id INT,
    account_id INT,
    costcenter_id INT,
    amount DECIMAL(18, 2),
    currency VARCHAR(10),
    transaction_type VARCHAR(20) CHECK (transaction_type IN ('actual', 'budget')),
    description TEXT,
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
    FOREIGN KEY (account_id) REFERENCES dim_account(account_id),
    FOREIGN KEY (costcenter_id) REFERENCES dim_costcenter(costcenter_id)
);
-- usw.