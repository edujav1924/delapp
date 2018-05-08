$(document).ready(function() {
    $('#example').DataTable( {
        responsive: {
            
        }
    } );

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
