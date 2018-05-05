$(document).ready(function() {
  //para actualizacion de notificacion
  var myFunction = function() {
    $.ajax({
      type: "GET",
      url: window.location.origin+"/otro.json",
      success: function(data) {
        console.log(data.length);
        console.log(document.getElementById("jola").innerHTML);
        if ((data.length-document.getElementById("jola").innerHTML)>=0) {
          document.getElementById("noti").innerHTML=data.length-document.getElementById("jola").innerHTML;
        }
      }
    });
  };
  /*  myFunction();
    setInterval(myFunction, 120000);
*/
});
