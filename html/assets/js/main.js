$(function(){
  $("#btnAddDevice").on("click", function(e){
      $("#ModalAddDevice").modal();
  });
  $("#tbFortigateDevices").DataTable();

  $("#tblLastFgtBackup").DataTable({
    "ajax": "api.php?method=getAllDevices",
    "initComplete": function(settings, json) {
      $(".getHashFile").on("click", function (e) {
        var hash = this.getAttribute("data-hash");
        var serial = this.getAttribute("data-serial");
        document.getElementById("fgtSerial").value = serial
        document.getElementById("fgtRevision").value = hash
        openModalLastChanges(serial);
      })
      $(".hashPopOver").popover({
          html: true,
          container: 'body',
          content: function() {
            return this.html();
          }
        });
     }
  });
  $("#HashFile").on("click", function(){
    $("#FileChanges").toggle();
    $("#FileAndDownload").toggle();
    var serial = document.getElementById("fgtSerial").value
    var hashID = document.getElementById("fgtRevision").value
    var HashFile = "api.php?method=getFile&revision=" + hashID + "&serial=" + serial ;
    $("#HashFileDownload").attr("href", HashFile + "&download=true")
    $('#hashFileContent').load(HashFile);
  });
  $("#HashFileChanges").on("click", function(){
    $("#FileChanges").toggle();
    $("#FileAndDownload").toggle();
    var serial = document.getElementById("fgtSerial").value
    var HashFile = "api.php?method=getChanges&serial=" + serial ;
    $('#hashFileContent').load(HashFile);
  });

});

function openModalLastChanges(fgtSerial){
  $("#FileAndDownload").hide();
  $("#FileChanges").show();
  var HashFile = "api.php?method=getChanges&serial=" + fgtSerial ;
  $('#hashFileContent').load(HashFile);
  $('#ModalHashFile').modal('show');
}
