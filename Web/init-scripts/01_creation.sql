CREATE DATABASE IF NOT EXISTS projet_irve;
CREATE USER IF NOT EXISTS 'projet_a3'@'localhost' IDENTIFIED BY 'SuperMotDePasseDeLaMortQuiTuePourLeProjetDinfoA3Semestre6';
GRANT ALL PRIVILEGES ON projet_irve.* TO 'projet_a3'@'localhost';
FLUSH PRIVILEGES;