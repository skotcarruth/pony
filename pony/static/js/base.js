(function($) {

  var pony = window.pony = {};

  pony.get_root_uri = function() {
    return 'http' + (pony.settings.request_secure ? 's' : '') +
      '://' + pony.settings.request_domain;
  };

  pony.parse_querystring = function(querystring) {
    // Parses a querystring and returns a decoded js object
    var parsed = {};
    var pairs = querystring.split('&');
    for (var i = 0; i < pairs.length; i++) {
      pair = pairs[i].split('=');
      parsed[pair[0]] = decodeURIComponent(pair[1]);
    }
    return parsed;
  };

  pony.style_file_inputs = function() {
    // Crazy js fakery to mimic styles on file inputs
    var file_inputs = $('input[type=file]').addClass('file_input');
    // Set up the wrapping html
    file_inputs.wrap('<div class="file_input"></div>');
    file_inputs.after('<div class="fake_file_input"><input type="text" disabled="disabled" /><span>Browse...</span></div>');
    // Set up the onchange event to update the fake input
    file_inputs.change(function() {
      var file_input = $(this);
      file_input.parents('div.file_input').find('div.fake_file_input input').val(file_input.val());
    });
  };
  $(pony.style_file_inputs);

})(jQuery);
