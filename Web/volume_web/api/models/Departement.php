<?php

class Departement {
    public static function getAll() {
        try {
            $statement = Database::preparedQuery(
                "SELECT id_departement, denomination FROM departement ORDER BY id_departement ASC;",
                []
            );
            return $statement ? $statement->fetchAll(PDO::FETCH_ASSOC) : false;
        } catch (PDOException $exception) {
            error_log('Request error: '.$exception->getMessage());
            return false;
        }
    }
}
?>
