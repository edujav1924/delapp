$(document).ready(function() {
  const messaging = firebase.messaging();
  messaging.requestPermission()
  .then(function() {
    console.log('Notification permission granted.');
    // TODO(developer): Retrieve an Instance ID token for use with FCM.
    // ...
  })
  .catch(function(err) {
    console.log('Unable to get permission to notify.', err);
  });
  console.log("saca");
  messaging.getToken()
    .then(function(currentToken) {
      console.log("aca");
      if (currentToken) {
        console.log(currentToken);
        updateUIForPushEnabled(currentToken);
      } else {
        // Show permission request.
        console.log('No Instance ID token available. Request permission to generate one.');
        // Show permission UI.
        updateUIForPushPermissionRequired();
      }
    })
    .catch(function(err) {
      console.log('An error occurred while retrieving token. ', err);
    });
  messaging.onTokenRefresh(function() {
    messaging.getToken()
    .then(function(refreshedToken) {
      console.log('Token refreshed.');
      // Indicate that the new Instance ID token has not yet been sent to the
      // app server.
      // Send Instance ID token to app server.
      // ...
    })
    .catch(function(err) {
      console.log('Unable to retrieve refreshed token ', err);
    });
  });

});
