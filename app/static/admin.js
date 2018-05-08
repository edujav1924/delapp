$(document).ready(function() {
  $("#picker").keydown(false);
  $("#form").submit(function(e) {
    desde = document.querySelector('input[name="desde"]');
    console.log(desde);
    hasta = document.querySelector('input[name="hasta"]');
    empresa = document.querySelector('input[name="empresa"]');
    console.log(hasta);
    if (desde.value.localeCompare("")==0 || hasta.value.localeCompare("")==0 || empresa.value.localeCompare("")==0) {
      e.preventDefault();
      alert("complete con fechas validas")
    }
  });
});
