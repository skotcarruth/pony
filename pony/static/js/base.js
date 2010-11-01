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

})(jQuery);
