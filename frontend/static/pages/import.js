function upload_dataset() {
  var msg = $('#import_result').empty();
  var form = $('form')[0];
  if (!form.checkValidity()) {
    return;
  }
  var post_data = new FormData(form);
  post_data.append('ds_kind', $('#ds_kind option:selected', form).val());
  var wait = $('.wait', form).show();
  $.ajax({
    url: '/_upload_dataset',
    data: post_data,
    processData: false,
    contentType: false,
    type: 'POST',
    error: function(jqXHR, textStatus, errorThrown) {
      wait.hide();
      msg.html(jqXHR.responseText);
    },
    success: function(url) {
      wait.hide();
      $('input', form).val(''); // reset the form inputs
      msg.html('Dataset imported. <a href="' + url + '">Explore</a>.');
    }
  });
}
$(document).ready(function(){
  var si = $('#spectrum_instructions'),
      mi = $('#metadata_instructions');
  $('#spectrum_row').mouseenter(function(){si.show(); mi.hide();});
  $('#metadata_row').mouseenter(function(){mi.show(); si.hide();});
});
