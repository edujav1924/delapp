$(document).ready(function() {
  // agregar nuevo
  $('#alerta').hide();
  console.log($('#empresa').text());
  var a ='<option value="">--seleccione--</option>';
  var b = a;
  $.get( "http://192.168.43.158:8000/en", function( data ) {
     $.each(data, function(index, element) {
        $.each(element, function(indea,value) {
           if (index.localeCompare("productos")==0) {
             b = b + '<option value="'+value.producto+'">'+value.producto+'</option>'
           }
           else {
             a = a + '<option value="'+value.nombre+'">'+value.nombre+'</option>'
           }
        });
     });
     var objTo = document.getElementById("encargado");
     var divtest = document.createElement("select");
     divtest.setAttribute("class","custom-select");
     divtest.setAttribute("id","select-encargado");
     divtest.setAttribute("required","");
     divtest.innerHTML = a
     objTo.appendChild(divtest);
  });


  $('#agregar').on('click', function() {
    education_fields()
  });
  $('#eliminar').on('click', function() {
    remove_education_fields(room);
  });
var room = 0;
function education_fields() {
    room++;

    var objTo = document.getElementById("productos-col");
    var divtest = document.createElement("select");
    divtest.setAttribute("class","custom-select");
    divtest.setAttribute("name","producto");
    divtest.setAttribute("id","producto-"+room);
    divtest.setAttribute("required","");
    divtest.innerHTML = b
    objTo.appendChild(divtest);
    var objTo = document.getElementById("cantidad-col");
    var divtest = document.createElement("input");
    divtest.setAttribute("class","form-control");
    divtest.setAttribute("id","cantidad-"+room);
    divtest.setAttribute("name","cantidad");
    divtest.setAttribute("placeholder","cantidad");
    divtest.setAttribute("style","text-align:center;");
    divtest.setAttribute("type","number");
    divtest.setAttribute("required","");
    objTo.appendChild(divtest);


}
   function remove_education_fields(rid) {
    if (room>0) {
       console.log("div-"+rid);
  	   $('#producto-'+rid).remove();
       $('#cantidad-'+rid).remove();
         room--;
     }

   }
   (function() {
  'use strict';
  window.addEventListener('load', function() {
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.getElementsByClassName('needs-validation');
    // Loop over them and prevent submission
    var validation = Array.prototype.filter.call(forms, function(form) {
      form.addEventListener('submit', function(event) {
        if (form.checkValidity() === false) {
          event.preventDefault();
          event.stopPropagation();
        }
        else {
          event.preventDefault();
          event.stopPropagation();
          console.log("listo");

          var b = [];
          var c =0;
          var nuevo=true;
          for (var i = 0; i <=room; i++) {
            var prod = $('#producto-'+i+ ' option:selected').val();
            var cant = $('#cantidad-'+i).val();
            for (var j = 0; j < b.length; j++) {
              var aux = prod.localeCompare(b[j]['producto'])  ;
              if (aux==0) {
                c++;
                b[j]['cantidad'] = parseInt(b[j]['cantidad']) +parseInt(cant);
                nuevo = false;
              }
            }
            if (nuevo===true) {
              b[i]={'producto':prod,'cantidad':parseInt(cant)};
            }
            else {
              nuevo=true;
            }
          }
          var formData = {
            'nombre'            : $('input[name=nombre]').val(),
            'apellido'          : $('input[name=apellido]').val(),
            'celular'          : $('input[name=telefono]').val(),
            'empresa'           :$('#empresa').text(),
            'pedidos'           : b,
            'ubicacion'         : $('input[name=ubicacion]').val(),
            'encargado'         : $('#select-encargado' + ' option:selected').val(),
            'status'            : true,
          };
            console.log(formData);
            $.ajax({
                type: 'POST', // define the type of HTTP verb we want to use (POST for our form)
                url: 'http://192.168.43.158:8000/cliente/', // the url where we want to POST
                encode: true,
                contentType: 'application/json',
                data: JSON.stringify( formData)
              }).done(function() {
                $('#alerta').show();
                myFunction();
                $(":input").prop('disabled', true);
                $("#form")[0].reset();

              })
              .fail(function() {})
              .always(function() {});
        }
        form.classList.add('was-validated');
      }, false);
    });
  }, false);
})();
function myFunction() {

    setTimeout(function(){ $('#alerta').hide();
    $(":input").prop('disabled', false);
   }, 3000);

}
});
