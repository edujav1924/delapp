$(document).ready(function() {
    var pos = 0;
    var k=0;
    var new_precio="";
    var new_producto = "";
    document.getElementById("editar").disabled = true;
    var table = $('#example').DataTable();

    $('#example tbody').on( 'click', 'tr', function (e) {
        pos = e.currentTarget.id;
        if ( $(this).hasClass('selected') ) {
            $(this).removeClass('selected');
            document.getElementById("editar").disabled = true;

        }
        else {
            table.$('tr.selected').removeClass('selected');
            $(this).addClass('selected');
            document.getElementById("editar").disabled = false;


        }
    } );

    $('#editar').click( function () {
        $('#myModal').modal('show');
    } );
    $('#myModal').on('show.bs.modal', function (event) {
        var modal = $(this);
        console.log(pos+'-row');
        modal.find('#selectprod').val(document.getElementById(pos+'-prod').innerHTML);
        modal.find('#selectprec').val(parseInt(document.getElementById(pos+'-prec').innerHTML));

    });
    $('#myModal').on("click", "#submit", function(){
        var forms = document.getElementsByClassName('form-signin');
        var validation = Array.prototype.filter.call(forms, function(form) {
            if (form.checkValidity() === false) {
            }
            else {
                var form = {
                    'method'        :'edit',
                    'id'            :pos,
                    'producto'      :$('#selectprod').val(),
                    'precio'        :parseInt($('#selectprec').val()),

                }
                console.log(form);
                $.ajax({
                    type: 'POST', // define the type of HTTP verb we want to use (POST for our form)
                    url: 'https://192.168.43.158/home/misproductos/1', // the url where we want to POST
                    encode: true,
                    contentType: 'application/json',
                    data: JSON.stringify(form)
                  }).done(function() {
                    $('myModal').modal('hide');
                  })
                  .fail(function(e) {
                      console.log("falla");
                      console.log(e);
                  })
                  .always(function() {});
                //$('#myModal').modal('hide');
            }

        });

    });

});
