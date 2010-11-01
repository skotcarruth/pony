(function($) {

  pony.fb_init = function() {
    // Construct the authorization URL
    var callback_url = pony.get_root_uri() + pony.settings.facebook_callback_url;
    var extended_permissions = 'publish_stream,user_birthday,friends_birthday,email';
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
      // Got the access token, so save it and trigger response
      console.log(response['access_token']);
    }
    else {
      console.log('nono');
    }
  };

})(jQuery);
