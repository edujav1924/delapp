$(document).ready(function() {
    document.getElementById("nuevo").disabled = true;
    console.log(window.location.href);
    var pos = 0;
    var edit = false;
    var newe = false;
    var erase = false;
    var method = "";

    var table = $('#example').DataTable();

    $('#example tbody').on( 'click', 'tr', function (e) {
        pos = e.currentTarget.id;
        console.log(pos);
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
        var modal = $(this);
        $('#modalprod').empty();
        $('#modalencar').empty();
        console.log(pos);
        modal.find('#selectnombre').val(document.getElementById(pos+'-name').innerHTML);
        modal.find('#selectdist').val(document.getElementById(pos+'-distancia').innerHTML);
        modal.find('#fechamodal').text(document.getElementById(pos+'-fecha').innerHTML);
        modal.find('#horamodal').text(document.getElementById(pos+'-hora').innerHTML);

        $('.po-'+pos).clone().appendTo('#modalprod');
        $('#encar').clone().appendTo('#modalencar');
        modal.find('#encar').removeAttr('hidden')

    });

});
