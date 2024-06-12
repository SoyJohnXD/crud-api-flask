
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
('Administrator', 'Acceso total al sistema 🥸', '["create", "read", "update", "delete"]'),
('Employee', 'Acceso estandar a las funciones del sistema 👨‍🦱', '["read"]'),
('HR Administrad', 'Permisos relacionados con recursos Humanos', '["create", "read", "update"]');

-- Insert initial data into 'User' table
INSERT INTO user (`email`, `password`, `role_id`) VALUES 
('admin@admin.com', 'pass', 1),
('user@user.com', 'user', 2);

