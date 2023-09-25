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
            { "data": "lado_mamario" },
            { "data": "resultado" },
            { "data":  null},
        ],
        columnDefs: [
            {
                targets: [0, 1, 2],
                class: 'text-center',
                orderable: true
            },
            {
                targets: [1], render: (data, type, row) => {
                    let orientacion = row.lado_mamario == 0 ? 'Derecha' : 'Izquerda';
                    let html = `${orientacion} `;
                    return html;
                }
            },
            {
                targets: [2], render: (data, type, row) => {
                    let cancer = row.resultado == 0 ? 'Cancer' : 'Normal';
                    let html = `${cancer} `;
                    return html;
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: (data, type, row) => {
                    let buttons = `<a href="/core/mamografia/edit/${row.id}/" class="btn btn-primary btn-xs btn-flat mr-2"><i class="fas fa-edit"></i></a>`;
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
});

