$(document).ready(function() {
    console.log(window.location.href);
    var pos = 0;
    var edit = false;
    var newe = false;
    var erase = false;
    var method = "";
    document.getElementById("editar").disabled = true;
    document.getElementById("eliminar").disabled = true;

    var table = $('#example').DataTable();

    $('#example tbody').on( 'click', 'tr', function (e) {
        pos = e.currentTarget.id;
        if ( $(this).hasClass('selected') ) {
            $(this).removeClass('selected');
            document.getElementById("editar").disabled = true;
            document.getElementById("eliminar").disabled = true;

        }
        else {
            table.$('tr.selected').removeClass('selected');
            $(this).addClass('selected');
            document.getElementById("editar").disabled = false;
            document.getElementById("eliminar").disabled = false;
        }
    } );
    $("#editar").on('click',function(){
        edit = true;
        newe = false;
        $('#myModal').modal('show');


    })
    $("#nuevo").on('click',function(){
        newe = true;
        edit= false;
        $('#myModal').modal('show');
    })

    $("#eliminar").on('click',function(){
        $('#modal_delete').modal('show');
    })

    $('#myModal').on('show.bs.modal', function (event) {
        var modal = $(this);
        console.log(pos+'-row');
        if (edit) {
            console.log("editar");
            modal.find('#selectprod').val(document.getElementById(pos+'-prod').innerHTML);
            modal.find('#selectprec').val(parseInt(document.getElementById(pos+'-prec').innerHTML));
            method = 'edit';
        }
        else if (newe) {
            console.log("nuevo");
            modal.find('#selectprod').val("");
            modal.find('#selectprec').val("");
            method = 'new'
        }
    });

    $('#modal_delete').on('show.bs.modal', function (event) {
        var modal = $(this);
        modal.find('#producto_delete').text(document.getElementById(pos+'-prod').innerHTML);
        modal.find('#precio_delete').text(document.getElementById(pos+'-prec').innerHTML);

    });
    $('#myModal').on("click", "#submit", function(){
        var forms = document.getElementsByClassName('form-signin');
        var validation = Array.prototype.filter.call(forms, function(form) {
            if (form.checkValidity() === false) {
            }
            else {
                var form = {
                    'method'        :method,
                    'id'            :pos,
                    'producto'      :$('#selectprod').val(),
                    'precio'        :parseInt($('#selectprec').val()),

                }
                document.getElementById("loader").style.display = "visible";
                $.ajax({
                    statusCode: {
                        201: function() {
                            console.log("llego");
                            document.getElementById("env").style.display = "none";
                            $('#myModal').modal('hide');
                            window.location.reload()
                        },
                        202 :function(){
                            document.getElementById("env").style.display = "none";
                            $('#myModal').modal('hide');
                            window.location.reload()
                        },
                        401 :function(){
                            document.getElementById("env").style.display = "none";
                            alert("Inicie Sesion primero")
                        },
                    },
                    type: 'POST', // define the type of HTTP verb we want to use (POST for our form)
                    url: window.location.href, // the url where we want to POST
                    encode: true,
                    contentType: 'application/json',
                    data: JSON.stringify(form)
                })
                  .fail(function(e) {
                      console.log("falla");
                      console.log(e);
                      document.getElementById("env").style.display = "none";
                      alert("error de envio")

                  });
            }
        });
    });
    $('#modal_delete').on("click", "#delete", function(){
        document.getElementById("loader").style.display = "visible";
        var form = {
            'method'        :'delete',
            'id'            :pos,
        }
        $.ajax({
                statusCode: {
                201: function() {
                    console.log("llego");
                    document.getElementById("env").style.display = "none";
                    $('#modal_delete').modal('hide');
                    window.location.reload()

                }
            },
            type: 'POST', // define the type of HTTP verb we want to use (POST for our form)
            url: window.location.href, // the url where we want to POST
            encode: true,
            contentType: 'application/json',
            data: JSON.stringify(form)
        })
          .fail(function(e) {
              alert("error de envio")
              console.log("falla");
              console.log(e);
              document.getElementById("env").style.display = "none";

          });

      });
});
