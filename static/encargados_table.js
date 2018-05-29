$(document).ready(function() {
  document.getElementById("nuevo").disabled = true;
  pos = 0;
  var table = $('#example').DataTable( {
  "order": [],
  responsive: true,
} );

  $('#example tbody').on( 'click', 'tr', function (e) {
      pos = e.currentTarget.id;
      if ( $(this).hasClass('selected') ) {
          $(this).removeClass('selected');
          document.getElementById("nuevo").disabled = true;
      }
      else {
          table.$('tr.selected').removeClass('selected');
          $(this).addClass('selected');
          document.getElementById("nuevo").disabled = false;
      }
  } );
  $("#nuevo").on("click",function(){
    console.log(pos);
    var form = {
      'id':pos,
      'method':'confirmar'
    }
    $.ajax({
        statusCode: {
            201: function() {
                console.log("eliminado");
                window.location.reload();
            },
            401 :function(){
                alert("Inicie Sesion primero");
            },
        },
        type: 'POST', // define the type of HTTP verb we want to use (POST for our form)
        url: window.location.href, // the url where we want to POST
        encode: true,
        contentType: 'application/json',
        data: JSON.stringify(form)
    }).fail(function(e) {
          console.log("falla");
          console.log(e);
          alert("error de envio");
      });
  })
  $("#form").submit(function(e) {
    desde = document.querySelector('input[name="fecha_desde"]');
    console.log(desde);
    hasta = document.querySelector('input[name="fecha_hasta"]');
    console.log(hasta);
    if (desde.value.localeCompare("")==0 || hasta.value.localeCompare("")==0) {
      e.preventDefault();
      alert("complete con fechas validas")
    }
  });
});
