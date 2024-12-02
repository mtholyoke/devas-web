function do_search() {
  var form = $('form')[0];
  var post_data = {
    query: form.query.value,
    case_sensitive: +form.case_sensitive.checked,
    full_text: +form.full_text.checked,
    ds_kind: multi_val($('#ds_kind option:selected')),
  };
  var result_div = $('#search_result'),
      err_span = $('.err_msg', form).empty(),
      wait = $('.wait', form).show();
  $.ajax({
    url: '/_search_metadata',
    data: post_data,
    type: 'POST',
    error: function(jqXHR, textStatus, errorThrown) {
      wait.hide();
      result_div.empty();
      err_span.text(jqXHR.responseText);
    },
    success: function(data) {
      wait.hide();
      result_div.html(data);
    }
  });
}
$(document).ready(function(){
  $('#ds_kind').select2();
});
