<?php

class Database {
    var $database;
    function Database($filename){
        $this->database = new SQLite3($filename);
        $this->database->busyTimeout(500);
        $this->database->exec('CREATE TABLE IF NOT EXISTS Person(PersonID INTEGER PRIMARY KEY AUTOINCREMENT, Password TEXT, Salt TEXT, Username TEXT, Token TEXT, Zoobars INTEGER DEFAULT 10, Profile TEXT)');
    }

    function executeQuery($q){
        $result = $this->database->query($q);
        return new ResultSet($result);
    }

    function quote($s){
        return $this->database->escapeString($s);
    }

    function __destruct() {
        $this->database->close();
    }
}

class ResultSet {
    var $result;
    var $currentRow;
    
    function ResultSet(&$result){
        $this->result =& $result;
    }

    function getCurrentValueByName($name){
        if($this->currentRow)
            return $this->currentRow[$name];
        return false;
    }

    function next(){
        $this->currentRow = $this->result->fetchArray();
        return $this->currentRow;
    }
    
    // ignore row number this is so broke
    function getValueByNr($rowno,$colno){
        if(!$this->currentRow)
            $this->next();
        return $this->currentRow[$colno];

    }

    function getCurrentValues(){
        if(!$this->currentRow)
            $this->next();
        return $this->currentRow;
    }

}
?>
