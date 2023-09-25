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
            { "data": "id" },
            { "data": "nombre" },
            { "data": "cedula" },
            { "data": null },
        ],
        columnDefs: [
            {
                targets: [0, 1, 2],
                class: 'text-center',
                orderable: true
            },
            {
                targets: [1], render: (data, type, row) => {
                    let html = `${row.nombre} ${row.apellido_paterno} ${row.apellido_materno}`;
                    return html;
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: (data, type, row) => {
                    let buttons = `<a href="/core/paciente/${row.id}/" class="btn btn-primary btn-xs btn-flat mr-2"><i class="fas fa-edit"></i></a>`;
                    buttons += `<a href="/core/mamografia/${row.external_id}/" type="button" class="btn btn-outline-warning btn-xs btn-flat mr-2"><i class="fas fa-solid fa-radiation"></i></a>`;                  
                    return buttons;
                }
            }
        ],
        initComplete: function (settings, json) {

        }
    });
});

