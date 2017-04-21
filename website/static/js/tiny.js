$(document).ready(function(){
  $('#csv-upload').change(function() {
    var rawPath = $(this).val();
    var refinePath = rawPath.replace(/\\/g,'/');

    var arr = refinePath.split("/");
    $('#selected-file').text(arr[arr.length-1]);
  });
});
