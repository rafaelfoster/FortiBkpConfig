<?php
//   $timezone = 'America/Sao_Paulo';
//
  require_once ('inc/MysqliDb.php');
  require_once ("inc/gitlib/vendor/autoload.php");
  use Gitonomy\Git\Repository;

Class commit{
  public $db = "";
  public $repo = "";

  public function gitRepo(){
    if (!is_object($this->repo)){
      $repofolder = "/var/repositories/fortibkpconfig";
      $this->repo = new Repository($repofolder);
      chdir ( $repofolder );
    }
    return $this->repo;
  }

  public function database(){
     if (!is_object($this->db))
        $this->db = new MysqliDb ('localhost', 'fgtbkp', '1trMgqrFuUXBAHU5R5VUphjRw5MS', 'you_admin');
     return $this->db;
  }
  public function dbGet($fields,$serial = null){
      $conn = $this->database();
      if (!is_array($fields)){
        $cols = Array ($fields);
      } else {
          $cols = $fields;
      }

      if(!is_null($serial)){
        $conn->where("SERIAL",$serial);
      }
      $dbquery = $conn->get("fgt_devices", null, $cols);
      return $dbquery;
  }
  public function organizeArrayByDate($a, $b){
      $t1 = strtotime($a['Data']);
      $t2 = strtotime($b['Data']);
      return $t2 - $t1;
  }

  function getFileName($serial){
      $cols = Array ("SERIAL", "LOCAL");
      if (!is_null($serial)){
        $FGTDevs = $this->dbGet( Array("SERIAL", "LOCAL"),$serial);
        $fileName = $FGTDevs[0]["LOCAL"] . "/bkp_fgtconfig_" . $FGTDevs[0]["SERIAL"] . ".conf";
        return $fileName;
      } else {
        $FGTDevs = $db->get("fgt_devices", null, $cols);
      }
  }

  public function getFile($revision, $serial){
      $file = $this->getFileName($serial);
      $filerevision = $this->gitRepo()->run("show", array($revision . ":" . $file));
      return $filerevision;
  }



}

?>
