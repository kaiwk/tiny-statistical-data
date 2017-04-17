$(document).ready(function(){
  $('input[name="file-upload"]').change(function () {
    var fileName = $(this).val();
    var arr = fileName.split('/');
    $('#choose-file').text(arr[arr.length-1])
  });
});
