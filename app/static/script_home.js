$(document).ready(function() {
  //pagina inicial
  var ip = window.location.href;
  console.log(window.location.origin);
  console.log(ip);
  $(function() {
    $('.confirm').on('click', function() {

      var texto = this.id;
      texto = texto.split("-");
      seleccion = $('#' + texto[1] + '-encargado' + ' option:selected').val();
      if (seleccion.localeCompare("value") == 0) {
        document.getElementById(texto[1] + '-encargado').style.borderColor = "red";
      } else {
        if (texto[0].localeCompare("aceptar") == 0) {
          var formData = {
            'id': texto[1],
            'encargado': $('#' + texto[1] + '-encargado' + ' option:selected').val(),
            'comando': 'aceptar',
          };
          console.log(formData);
          $.ajax({
              type: 'POST', // define the type of HTTP verb we want to use (POST for our form)
              url: ip, // the url where we want to POST
              data:formData, // our data object // what type of data do we expect back from the server
              encode: true,

            }).done(function() {
              console.log('#row-' + texto[1]);
              //document.getElementById('row-'+texto[1]).style.display = 'none';
              $('#row-' + texto[1]).hide(1000);
              document.getElementById("jola").innerHTML=document.getElementById("jola").innerHTML-1
            })
            .fail(function() {
              "fallalalalal"
            })
            .always(function() {});

        };
      };

    });
  });
  $('.delete').on('click', function() {
    console.log(this.id);
    var texto2 = this.id;
    texto2 = texto2.split("-");
    if (texto2[0].localeCompare("rechazar") == 0) {
      var formData = {
        'id': texto2[1],
        'encargado': '',
        'comando': 'eliminar',
      };
      console.log(formData);
      $.ajax({
          type: 'POST', // define the type of HTTP verb we want to use (POST for our form)
          url: ip, // the url where we want to POST
          data: formData, // our data object // what type of data do we expect back from the server
          encode: true,
        }).done(function() {
          console.log('#row-' + texto2[1]);
          //document.getElementById('row-'+texto[1]).style.display = 'none';
          $('#row-' + texto2[1]).hide(1000);
        })
        .fail(function() {
          console.log("falla");
        })
        .always(function() {});

    };
  });
  $('#btn-noti').on('click', function() {
    location.reload()
  });
  /* */
});
