<?php
    require_once './config/constants.php';

    class Database {
        static $db = "";
        
        static function getConnection() {
            if(Database::$db != null)
                return Database::$db;
            
            $dsn = "mysql:dbname=".DB_NAME.";host=".DB_SERVER.";port=".DB_PORT.";charset=utf8mb4";
            $username = DB_USER;
            $password = DB_PASSWORD;
            $options = [
                PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
                PDO::MYSQL_ATTR_INIT_COMMAND => "SET NAMES utf8mb4" // <-- Ligne magique
            ];

            try {
                $conn = new PDO($dsn, $username, $password, $options);
            } catch (PDOException $e) {
                error_log("Error while connection to database: ".$e->getMessage());
                return false;
            }
            
            Database::$db = $conn;
            return $conn;
        }
        
        static function preparedQuery(string $request, array $params) {
            try {
                $conn = Database::getConnection();
                if(!$conn) return false;
                
                $statement = $conn->prepare($request);

                foreach ($params as $key => $value) {
                    $type = PDO::PARAM_STR;
                    if (is_int($value)) {
                        $type = PDO::PARAM_INT;
                    } elseif (is_bool($value)) {
                        $type = PDO::PARAM_BOOL;
                    } elseif (is_null($value)) {
                        $type = PDO::PARAM_NULL;
                    }
                    
                    $paramKey = is_int($key) ? $key + 1 : $key;
                    
                    $statement->bindValue($paramKey, $value, $type);
                }

                $statement->execute();
                
                return $statement;
            } catch(PDOException $e) {
                error_log('Prepared query error: '.$e->getMessage());
                return false;
            }
        }
    }
?>