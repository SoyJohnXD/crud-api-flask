
-- Create 'Role' table
CREATE TABLE IF NOT EXISTS Role (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  permissions TEXT 
) ENGINE=InnoDB;

-- Create 'User' table
CREATE TABLE IF NOT EXISTS User (
  id INT AUTO_INCREMENT PRIMARY KEY,
  email VARCHAR(255) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL,
  role_id INT,
  FOREIGN KEY (role_id) REFERENCES Role(id)
) ENGINE=InnoDB;


-- Insert initial data into 'Role' table
INSERT INTO Role (name, description, permissions) VALUES 
('Administrator', 'Full access to the system', '["create", "read", "update", "delete"]'),
('Employee', 'Standard user access', '["read"]'),
('HR Manager', 'Human resources related permissions', '["create", "read", "update"]');

-- Insert initial data into 'User' table
INSERT INTO user (email, password, role_id) VALUES 
('admin@example.com', 'adminpassword', (SELECT id FROM Role WHERE name = 'Administrator')),
('user@example.com', 'userpassword', (SELECT id FROM Role WHERE name = 'Employee')),
('hrmanager@example.com', 'hrpassword', (SELECT id FROM Role WHERE name = 'HR Manager'));

