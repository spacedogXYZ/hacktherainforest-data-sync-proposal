chrome.app.runtime.onLaunched.addListener(function() {
  var win = chrome.app.window.create('app.html', {
    'bounds': {
      'width': 400,
      'height': 500
    }
  });
});