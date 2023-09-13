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
            { "data": "external_id" },
            { "data": "orientacion" },
            { "data": "resultado" },
            { "data": "descripcion" },
        ],
        columnDefs: [
            {
                targets: [0, 1, 2],
                class: 'text-center',
                orderable: true
            },/*
            {
                targets: [1], render: (data, type, row) => {
                    let html = `${row.nombre} ${row.apellido_paterno} ${row.apellido_materno}`;
                    return html;
                }
            },**/
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: (data, type, row) => {
                   return '';
                }
            }
        ],
        initComplete: function (settings, json) {

        }
    });
});

