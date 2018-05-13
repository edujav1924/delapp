$(document).ready(function() {
    console.log(window.location.href);
    document.getElementById("nuevo").disabled = true;
    var pos = 0;

    var method = "";

    var table = $('#example').DataTable({
        columnDefs: [
            { responsivePriority: 1, targets: 0 },
            { responsivePriority: 2, targets: -1 }
        ],
        "order": [[ 3, "desc" ]],
        responsive: true,
    });

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

    $("#nuevo").on('click',function(){
        $('#myModal_2').modal('show');
    })


    $('#myModal_2').on('show.bs.modal', function (event) {
        try {
            var modal = $(this);
            $('#modalprod').empty();
            $('#modalencar').empty();
            modal.find('#selectnombre').val(document.getElementById(pos+'-name').innerHTML);
            modal.find('#selectdist').val(document.getElementById(pos+'-distancia').innerHTML);
            modal.find('#fechamodal').text(document.getElementById(pos+'-fecha').innerHTML);
            modal.find('#horamodal').text(document.getElementById(pos+'-hora').innerHTML);
            $('#'+pos+'-lista').clone().appendTo('#modalprod');
            $('#encargado').clone().appendTo('#modalencar');
            modal.find('#encar').removeAttr('hidden');
            modal.find('#encargado').attr('id','selectencargado');
            modal.find('#selectencargado').attr('required');
            modal.find('#selectencargado').attr('class','custom-select form-control');
        } catch (e) {

            iziToast.warning({
                timeout: 3000,
                title: 'Alerta',
                message: 'Seleccione la fila correspondiente por favor.',
            });
            $('#myModal_2').modal('dispose');

        }


    });
    $('#myModal_2').on("click", "#enviar", function(){
        console.log('click');

        var forms = document.getElementsByClassName('form-signin');
        var validation = Array.prototype.filter.call(forms, function(form) {
            if (form.checkValidity() === false) {
                if($('#selectencargado').val().localeCompare("")==0){
                    iziToast.warning({
                        timeout: 3000,
                        title: 'Alerta',
                        message: 'Seleccione un encargado',
                    });
                    $('#selectencargado').css('border-color','#fc661c');
                }
                console.log('false');

            }
            else {
                var form = {
                    'comando'       :'aceptar',
                    'id'            :pos,
                    'nombre'        :$('#selectnombre').val(),
                    'encargado'     :$('#selectencargado').val()

                }
                console.log(form);
                $.ajax({
                    statusCode: {
                        201: function() {
                            console.log("llego");
                            $('#myModal_2').modal('hide');
                            window.location.reload()
                        },
                        202 :function(){
                            $('#myModal').modal('hide');
                            window.location.reload()
                        },
                        401 :function(){
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
    $('#btn-noti').on('click', function() {
      location.reload()
    });
});
