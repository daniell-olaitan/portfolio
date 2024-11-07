-- prepares a MySQL server for the project

CREATE DATABASE portfolio_db;
CREATE USER IF NOT EXISTS 'portfolio'@'localhost' IDENTIFIED BY 'Pp_2389913116';
GRANT ALL PRIVILEGES ON `portfolio_db`.* TO 'portfolio'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'hbnb_dev'@'localhost';
FLUSH PRIVILEGES;
