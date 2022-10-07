// =============  Data Table - (Start) ================= //

$(document).ready(function () {

    var table = $('#example').DataTable({

        buttons: ['copy', 'csv', 'excel', 'pdf', 'print']

    });

    // appendTo buttons of table to div with id "outer"


    div.buttons().container()
        .appendTo('#example_wrapper .col-md-12:eq(0)');

});

// =============  Data Table - (End) ================= //

$(document).ready(function () {
    $('table tr').click(function () {
        // open window in new tab
        if ($(this).attr('href')) {
            window.open($(this).attr('href'), '_blank');

        }

        return false;
    });
});

function go_detail(element) {

    if ($(element).attr('href')) {

        window.open($(element).attr('href'), '_blank');

    }

    return false;

}


// =============  Messsage post ================= //
$('#save').on('click', function (e) {
    e.preventDefault()
    const csrf_token = $('input[name=csrfmiddlewaretoken]').val()
    const contents = $('#message').text()

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader('X-CSRFToken', csrf_token)
        }
    })

    $.ajax({
        type: 'post',
        url: '/contact',
        data: {
            contents: contents
        },
        success: function (data, status, jqXHR) {
            console.log('Here you could update your frontend if needed')
        }
    })
})