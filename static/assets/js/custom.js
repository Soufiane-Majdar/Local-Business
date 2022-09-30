// =============  Data Table - (Start) ================= //

$(document).ready(function() {

    var table = $('#example').DataTable({

        buttons: ['copy', 'csv', 'excel', 'pdf', 'print']

    });

    // appendTo buttons of table to div with id "outer"


    div.buttons().container()
        .appendTo('#example_wrapper .col-md-12:eq(0)');

});

// =============  Data Table - (End) ================= //

$(document).ready(function() {
    $('table tr').click(function() {
        // open window in new tab
        if ($(this).attr('href')) {
            window.open($(this).attr('href'), '_blank');

        }

        return false;
    });
});