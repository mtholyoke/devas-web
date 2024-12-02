function toggle_extra(elt) {
  $(elt).parents('tr.dataset').nextUntil('tr.dataset')
        .find('.hideme').slideToggle();
  return false;
}
$(document).ready(function() {
  $('#datasets').tablesorter();
})
