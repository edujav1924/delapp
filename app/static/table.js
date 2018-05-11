$(document).ready(function() {
    $('#example').DataTable( {
        "order": [[ 5, "desc" ]],
        responsive: {
            details: {

              display: $.fn.dataTable.Responsive.display.modal( {
                  header: function ( row ) {
                      var data = row.data();
                      return 'Details for '+data[0];
                  }
              } ),
              renderer: $.fn.dataTable.Responsive.renderer.tableAll( {
                  tableClass: 'table'
              } )
            }
        }
    } );
} );
