<?php
//   $timezone = 'America/Sao_Paulo';
//
  require_once ('config.php');
  require_once ('inc/MysqliDb.php');
  require_once ("inc/gitlib/vendor/autoload.php");
  use Gitonomy\Git\Repository;

Class commit{
  public $db = "";
  public $repo = "";
  public $cnf = array();
  public $cnfDB = array();

  public function __construct() {
    global $config;
    global $configDB;
    $this->cnf = $config;
    $this->cnfDB = $configDB;
  }

  public function gitRepo(){
    if (!is_object($this->repo)){
      $repofolder = $this->cnf["repoFolder"];
      $this->repo = new Repository($repofolder);
      chdir ( $repofolder );
    }
    return $this->repo;
  }

  public function database(){
     if (!is_object($this->db))
        $this->db = new MysqliDb ($this->cnfDB["db_host"], $this->cnfDB["user"],$this->cnfDB["pass"], $this->cnfDB["database"] );
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

  private function getFileName($serial){
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

  public function getLastChanges($serial){
    $fileName = $this->getFileName($serial);
    $repo = $this->gitRepo();
    $diff = $repo->run("log", array("-p", "--follow", "-1", $fileName));
    $lastDiff = $this->str_chop_lines($diff, 11);
    $count = 1;
    print "<table border='0' style='border: 1px dashed gray;'>";
    foreach(preg_split("/((\r?\n)|(\r\n?))/", $lastDiff) as $line){
          if( preg_match("/^\-(.*)/",  $line) ){
            $class = "chDelLine";
          } elseif ( preg_match("/^\+(.*)/",  $line) ){
            $class = "chAddLine";
          }
          $line = preg_replace("/\-(.*)/", "$1", $line);
          $line = preg_replace("/\+(.*)/", "$1", $line);
          print '<tr class="$class" style="border: 1px dashed gray;">';
            print "<td width='50px' style='border: 1px dashed gray;'> $count </td>";
            print "<td width='200px' style='border: 1px dashed gray;'> $line </td>";
        print "</tr>";
        $count++;
    }
    print "</table>";
    // $lastDiff = preg_replace("/\-(.*)/", '<span class="remove"> $1 </span><br>', $lastDiff);
    // $lastDiff = preg_replace("/\+(.*)/", '<span class="add"> $1 </span><br>', $lastDiff);
    // print $lastDiff;

  }

  private function str_chop_lines($str, $lines = 4) {
    return implode("\n", array_slice(explode("\n", $str), $lines));
  }


}

?>
