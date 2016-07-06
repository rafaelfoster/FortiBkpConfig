<?php
  require_once ('inc/MysqliDb.php');
  // require_once ("inc/gitlib/Repository.php");
  require_once ("inc/gitlib/vendor/autoload.php");

  use Gitonomy\Git\Repository;

  $db = new MysqliDb ('localhost', 'fgtbkp', '1trMgqrFuUXBAHU5R5VUphjRw5MS', 'you_admin');

  $repofolder = "/var/repositories/fortibkpconfig";
  $repository = new Repository($repofolder);
  chdir ( $repofolder );
  // List fgt_devices
  $cols = Array ("NAME", "SERIAL", "CLIENT");
  $FGTDevs = $db->get("fgt_devices", null, $cols);
  // echo "Last executed query was ". $db->getLastQuery() . "<br><br>";
  print "<pre>";
  print_r($FGTDevs);
  print "</pre><br><br>";
  if ($db->count > 0){
    for($i = 0; $i < sizeof($FGTDevs); $i++){
      $fgtName   = $FGTDevs[$i]["NAME"];
      $fgtSerial = $FGTDevs[$i]["SERIAL"];
      $fgtClient = $FGTDevs[$i]["CLIENT"];
      $clientfolder = $repofolder . "/" . $fgtClient . "/";
      $clientRepoDir = "";
      if (!file_exists($clientfolder) && !is_dir($clientfolder)) {
          // print "$fgtClient Error: Repository of $fgtClient does not exists! <br>";
          continue;
      } else {
        // $clientRepoDir = array_diff(scandir($clientfolder), array());
        $clientRepoDir = array_diff(scandir($clientfolder), array('..', '.','.git'));
        // print_r($clientRepoDir);
        $fileName = null;
        foreach($clientRepoDir as $id => $file){
          if (strpos($file, $fgtSerial) !== false) {
            // print "$id -> $file <BR>";
            $fileName = $file;
            break;
          }
        }
        if (!is_null($fileName)){
          print "$fgtClient OK -> $fileName <br><br>";
          print "git log --follow " .  $clientfolder . $fileName;
          // $log = $repository->getLog('master', $fileName, 0, 10);
          $log = $repository->getLog('master');
          echo sprintf("<br>This log contains %s commits\n <br>", $log->countCommits());
          print "<br><br><pre>";
          print_r($log);
          print "</pre>";
        }
      }
    }
  }
?>
