-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS portfolio_dev_db;
CREATE USER IF NOT EXISTS 'portfolio_dev'@'localhost' IDENTIFIED BY 'Pp_2389913116';
GRANT ALL PRIVILEGES ON `portfolio_dev_db`.* TO 'portfolio_dev'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'portfolio_dev'@'localhost';
FLUSH PRIVILEGES;
