import { getCharacters } from "../api.js";
getCharacters()
    .then(characters => {
    let table = document.getElementById("player-table");
    let header = document.createElement("thead");
    let body = document.createElement("tbody");
    header.innerHTML = `
        <tr>
            <th data-field="name" data-filter-control="input">Name</th>
            ${characters.length > 0 && characters[0].hasOwnProperty("level") ? `<th data-field="level" data-filter-control="select">Level</th>` : ''}
            <th data-field="race" data-filter-control="select">Race</th>
            <th data-field="subrace" data-filter-control="select">Subrace</th>
            <th data-field="class" data-filter-control="select">Class</th>
            <th data-field="subclass" data-filter-control="select">SubClass</th>
        </tr>
    `;
    characters.forEach(character => {
        let row = document.createElement("tr");
        row.classList.add("item-row");
        row.innerHTML = `
            <td>${character.name}</td>
            ${characters.length > 0 && characters[0].hasOwnProperty("level") ? `<td>${character.level}</td>` : ''}
            <td>${character.race.value}</td>
            <td>${character.subrace.id ? character.subrace.value : ""}</td>
            <td>${character.classes.map(c => c.value).join('<br>')}</td>
            <td>${character.classes.flatMap((c) => c.subclasses.map(sc => sc.value)).join("<br>")}</td>
        `;
        body.appendChild(row);
    });
    table.appendChild(header);
    table.appendChild(body);
})
    .then(() => {
    $('#player-table thead tr')
        .clone(true)
        .addClass('filters')
        .appendTo('#player-table thead');
    // @ts-ignore
    $('#player-table').DataTable({
        orderCellsTop: true,
        fixedHeader: true,
        initComplete: function () {
            var api = this.api();
            api
                .columns()
                .eq(0)
                .each(function (columnIndex) {
                var cell = $('.filters th').eq($(api.column(columnIndex).header()).index());
                var title = $(cell).text();
                $(cell).html(`<input type="text" placeholder="${title}"/>`);
                $('input', $('.filters th').eq($(api.column(columnIndex).header()).index()))
                    .off('keyup change')
                    .on('change', function (e) {
                    var elm = this;
                    $(elm).attr('title', $(elm).val());
                    var regexr = '({search})';
                    var cursorPosition = elm.selectionStart;
                    api
                        .column(columnIndex)
                        .search(elm.value != '' ? regexr.replace('{search}', `(((${elm.value})))`) : '', elm.value != '', elm.value == '')
                        .draw();
                })
                    .on('keyup', function (e) {
                    e.stopPropagation();
                    $(this).trigger('change');
                    $(this).trigger('focus')[0];
                });
            });
        }
    });
});
