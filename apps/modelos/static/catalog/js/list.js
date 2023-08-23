$(document).ready(() => {
    $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "id"},
            {"data": "nombre"},
            {"data": "cedula"},
            {"data": null},
        ],
        columnDefs: [
            {
                targets: [0, 1, 2],
                class: 'text-center',
                orderable: true
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/core/pacientes/edit/' + row.id + '/" class="btn btn-warning btn-xs btn-flat mr-2"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/core/mamografia/create/' + row.external_id + '/" type="button" class="btn btn-outline-secondary btn-xs btn-flat mr-2"><i class="fas fa-trash-alt"></i></a>';
                    buttons += '<a href="/core/catalog/delete/' + row.id + '/" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                }
            }
        ],
        initComplete: function (settings, json) {

        }
    });
});

