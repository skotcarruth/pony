(function($) {

  pony.fb_query = function(id, callback) {
    var graph_url = 'https://graph.facebook.com/';
    if (!pony.settings.facebook_token) return;
    $.getJSON(
      graph_url + id + '?callback=?&access_token=' + pony.settings.facebook_token,
      callback
    );
  };

  pony.fb_init = function() {
    // Construct the authorization URL
    var callback_url = pony.get_root_uri() + pony.settings.facebook_callback_url;
    var extended_permissions = 'offline_access,publish_stream,user_birthday,friends_birthday,email';
    var auth_url = 'https://graph.facebook.com/oauth/authorize?client_id=' +
      pony.settings.facebook_app_id + '&redirect_uri=' +
      encodeURIComponent(callback_url) + '&type=user_agent&display=popup' +
      '&scope=' + extended_permissions;

    // Hook up the button to pop up the connect dialog
    var connect_button = $('#fb_connect_button');
    connect_button.click(function() {
      var popup_left = (window.screen.width / 2) - 335;
      var popup_top = (window.screen.height / 2) - 200;
      var auth_popup = window.open(
        auth_url,
        'auth_window',
        'status=0,toolbar=0,location=0,menubar=0,height=350,width=650,left=' +
          popup_left + ',top=' + popup_top + ',screenX=' + popup_left +
          ',screenY=' + popup_top
      );
      return false;
    });
  };
  $(pony.fb_init);

  pony.fb_handle_callback = function(hash) {
    response = pony.parse_querystring(hash.substr(1));
    if (response['access_token']) {
      // Got the access token, so take the appropriate response
      pony.settings.facebook_token = response['access_token'];
      var connect_button = $('#fb_connect_button');
      if (connect_button.attr('rel') == 'register') {
        pony.fb_handle_register(response);
      }
      else if (connect_button.attr('rel') == 'share') {
        pony.fb_handle_share(response);
      }
    }
    else {
      pony.fb_handle_cancel();
    }
  };

  pony.fb_handle_cancel = function(response) {
    // Ah well, better luck next time...
  };

  pony.fb_handle_share = function(response) {
    // Share it!
    console.log(response);
  };

  pony.fb_handle_register = function(response) {
    // Stuff the token into the form for user registration
    $('#id_facebook_token').val(response['access_token']);

    // Update the registration fields with facebook info
    pony.fb_query('me', function(data) {
      if (data.name) $('#id_name').val(data.name);
      if (data.email) $('#id_email').val(data.email);
      if (data.birthday) $('#id_birthday').val(data.birthday);
    });

    // Hide the connect box
    pony.hide_connect_box();
  };

  pony.hide_connect_box = function() {
    var connect = $('#connect');
    connect.css('height', connect.height());
    connect.empty().append('<span class="connect_thanks purple">Thanks for connecting.</span>');
    connect.delay(1250).animate({'opacity': 0}, 250, function() {
      connect.slideUp(250);
    });
  };

})(jQuery);
