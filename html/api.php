<?php

  $method   = $_REQUEST['method'];
  $method();

  function getAllDevices(){
    $repofolder = "/var/repositories/fortibkpconfig";
    chdir ( $repofolder );
    $timezone = "America/Sao_Paulo";
    require_once("commits.php");
    $commit = new commit();
    $cols = Array ("NAME", "SERIAL", "LOCAL");
    $devices = $commit->dbGet($cols);
    // foreach($devices as )
    $commits = Array();
    for ($i = 0; $i < sizeof($devices); $i++){
      $fileName = $devices[$i]["LOCAL"] . "/bkp_fgtconfig_" . $devices[$i]["SERIAL"] . ".conf";
      // print $fileName . "<br>";
      if (!file_exists($fileName))
            continue;
      $lastBackupEntries = "";
      $blame = $commit->gitRepo()->getBlame('master', $fileName);
      $commitList = "<table>";
      foreach ($blame->getLines() as $lineNumber => $line){
            $fgtCommit = $line->getCommit();
            if (array_key_exists($fgtCommit->getShortHash(),$commits) || ($fgtCommit->getShortHash() == "facbc76"))
                continue;
            $commitDate = $fgtCommit->getCommitterDate();
            date_timezone_set($commitDate, timezone_open($timezone));
            $commitDate = date_format($commitDate, 'Y-m-d H:i:s');
            $message = str_replace (array("\r\n", "\n", "\r"), ' ', $fgtCommit->getMessage() );
            $commits[$fgtCommit->getShortHash()] = array(
                "Hash"    => $fgtCommit->getShortHash(),
                "Author"  => $fgtCommit->getAuthorName(),
                "Message" => $message,
                "Data"    => $commitDate
            );
            $commitList = $commitList . "<tr><td style='padding-right: 20px'><a class='getHashFile aPointer' data-serial='" .  $devices[$i]["SERIAL"] .  "'data-hash=" . $fgtCommit->getShortHash() . ">         <b>" . $fgtCommit->getShortHash() . "</b></a></td><td>" . $commitDate . "</td></tr>";
        }
        $commitList = $commitList . "</table>";
        usort($commits, "organizeArrayByDate");
        $arrayClients[] = array(
            $devices[$i]["NAME"],
            $devices[$i]["SERIAL"],
            $devices[$i]["LOCAL"],
            $commits[0]["Data"],
            '<a class="getHashFile aPointer"  data-serial="' .  $devices[$i]["SERIAL"] .  '" data-hash="' . $commits[0]["Hash"] . '">' . $commits[0]["Hash"] . '</a>',
            '<span data-html="true" data-toggle="popover" data-original-title="Old backups" data-trigger="click" class="glyphicon glyphicon-th-list hashPopOver aPointer"  data-content="' . $commitList . '"> </span>'

        );
    }
    $data = array();
    $data['success'] = true;
    $data["aaData"] = $arrayClients;
    print json_encode($data);
    exit();
  }

  function organizeArrayByDate($a, $b){
      $t1 = strtotime($a['Data']);
      $t2 = strtotime($b['Data']);
      return $t2 - $t1;
  }

  function getFile(){
    global $method;
    $serial   = $_REQUEST['serial'];
    $revision = $_REQUEST['revision'];
    require_once("commits.php");
    $commit = new commit();
    $bkpFileContent = $commit->$method($revision, $serial);
    if (isset($_REQUEST['download'])){
        $headerFileDownload = "Content-Disposition: attachment; filename=\"restore_backup_$serial.cfg\"";
        header($headerFileDownload);
        header('Content-Type: text/plain');
        header('Content-Length: ' . strlen($str));
        header('Connection: close');
        print $bkpFileContent;
    } else {
      print "<pre>";
      print $bkpFileContent;
      print "</pre>";
    }
  }
