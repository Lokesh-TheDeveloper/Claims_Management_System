CREATE DATABASE claims_db;

DROP USER IF EXISTS 'flaskuser'@'localhost';
CREATE USER 'flaskuser'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON claims_db.* TO 'flaskuser'@'localhost';
FLUSH PRIVILEGES;

USE claims_db;

CREATE TABLE policyholders (
    holder_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE policies (
    policy_id INT AUTO_INCREMENT PRIMARY KEY,
    policyholder_id INT,
    coverage_amount DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (policyholder_id) REFERENCES policyholders(holder_id) ON DELETE CASCADE
);

CREATE TABLE claims (
    claim_id INT AUTO_INCREMENT PRIMARY KEY,
    policy_id INT,
    amount DECIMAL(10,2) NOT NULL,
    status ENUM('Pending', 'Approved', 'Rejected') DEFAULT 'Pending',
    FOREIGN KEY (policy_id) REFERENCES policies(policy_id) ON DELETE CASCADE
);








