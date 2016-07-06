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
  // print_r($FGTDevs);
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
          print "Blaming file " .  $fgtClient . "/" . $fileName;
          $blame = $repository->getBlame('master', $fgtClient . "/" . $fileName);
          print "<pre>";
          // print_r($blame->getGroupedLines());
          //
          // foreach ($blame->getGroupedLines() as $lineNumber => $commits){
          //     foreach($commits as $commitID => $commit){
          //       print $commitID;
          //       print "   -    ";
          //       print $commit->getCommit()->getShortHash();
          //       print "   -    ";
          //       print $commit->getCommit()->getAuthorName();
          //       // print_r($commit);
          //       print "<br><br><br>";
          //     }

          $commits = Array();
          foreach ($blame->getLines() as $lineNumber => $line){
              $commit = $line->getCommit();
              print "<pre>";
              // print_r($commit->getCommitterDate() );
              print "</pre>";
              if (array_key_exists($commit->getShortHash(),$commits))
                  continue;
              $commits[$commit->getShortHash()] = array(
                  "Author" => $commit->getAuthorName(),
                  "Message" => $commit->getMessage(),
              );
              // echo "<br><br>" . $commit->getShortHash()  . "    - (".$commit->getAuthorName() . ") -- " . $commit->getMessage() . "<br><br>";
              // break;
          }
          print_r($commits);
          print "</pre>";
        }
      }
    }
  }
?>
