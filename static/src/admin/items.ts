import { getAllItems, getClasses, getItem, getItemTypes, getMagicSchools, getRarities, updateItem } from "../api.js";
import { CategoryClass, Item } from "../types.js";

getAllItems()
.then(items => {
    items.forEach(item => {
        // data-bs-toggle="modal" data-bs-target="#item-edit-form"
        $('#item-table-body').append(`
                <tr class="item-row" data-bs-id="${item.id}" data-bs-table="${item.table}">
                    <td>${item.name}</td>
                    <td>${item.table}</td>
                    <td>${item.type.value ? item.type.value : ""}</td>
                    <td>${item.cost}</td>
                    <td>${item.rarity.value}</td>
                </tr>
            `)
    })
})
.then(() => {
    $(document).on('click', '.item-row', function(e){
        const target = e.target.parentElement as HTMLElement
        // @ts-ignore
        const modal = new bootstrap.Modal('#item-edit-form')
        getItem(target.getAttribute('data-bs-table'), parseInt(target.getAttribute('data-bs-id')))
        .then(item => {
            $('#item-edit-form').attr("data-bs-id", item.id)
            $('#item-edit-form').attr("data-bs-table", item.table)

            getRarities()
            .then(rarities => {
                // Basic Defaulting
                $('#item-edit-title').html(item.name)
                $('#item-edit-name').val(item.name)
                $('#item-edit-cost').val(item.cost)
                $('#item-edit-source').val(item.source)
                $('#item-edit-notes').val(item.notes)
                
                // Item Type
                if (item.type.id){
                    $('#type-column').show()
                    $('#item-edit-subtype').html('')
                    getItemTypes(item.table)
                    .then( types => {
                        types.forEach(type => {
                            $('#item-edit-subtype').append(`
                                <option ${item.type.id == type.id ? 'selected':''} value="${type.id}">${type.value}</option>
                                `)
                        })
                    })

                } else {
                    $('#item-edit-subtype').html('')
                    $('#type-column').hide()
                }
                
                // Item Rarity
                $('#item-edit-rarity').html('')
                rarities.forEach(rarity => {
                    $('#item-edit-rarity').append(`
                        <option ${item.rarity.id == rarity.id ? 'selected':''} value="${rarity.id}">${rarity.value}</option>
                        `)
                })
                
                // Item Modifier
                if (item.item_modifier){
                    $('#item-mod-form').show()
                    $('#item-edit-item-modifier').prop('checked', item.item_modifier)
                } else{
                    $('#item-edit-item-modifier').prop('checked', false)
                    $('#item-mod-form').hide()
                }

                // Attunement
                if (item.attunement){
                    $('#item-attunement-form').show()
                    $('#item-edit-attunement').prop('checked', item.attunement)
                } else{
                    $('#item-edit-attunement').prop('checked', false)
                    $('#item-attunement-form').hide()
                }

                // Seeking Only
                if (item.seeking_only){
                    $('#item-seek-form').show()
                    $('#item-edit-seeking').prop('checked', item.seeking_only)
                } else{
                    $('#item-edit-seeking').prop('checked', false)
                    $('#item-seek-form').hide()
                }

                // School and Classes
                if (item.school.id){
                    $('#class-column').show()
                    $('#item-edit-school').html('')

                    getMagicSchools()
                    .then(schools => {
                        schools.forEach(school => {
                            $('#item-edit-school').append(`
                                <option ${item.school.id == school.id ? 'selected':''} value="${school.id}">${school.value}</option>
                                `)
                        })
                    })

                    $('#class-row').show()
                    $('#class-row').html(`
                        <div class="col-auto">Classes:</div>
                        `)
                    getClasses()
                    .then(classes => {
                        classes.forEach(playerClass => {      
                            $('#class-row').append(`
                                <div class="col-auto">
                                    <div class="form-check form-check-inline form-switch">
                                        <input class="form-check-input item-edit" type="checkbox" id="item-edit-class-${playerClass.value}" name="class-${playerClass.value}" value="${playerClass.id}" ${playerClass.id in item.classes.map(c => c.id) ? 'checked' : ''}>
                                        <label class="form-check-label" for="item-edit-class-${playerClass.value}">${playerClass.value}</label>
                                    </div>
                                </div>
                                `)
                        })
                    })
                } else {
                    $('#class-column').hide()
                    $('#item-edit-school').html('')
                    $('#class-row').hide()
                    $('#class-row').html('')
                }

                // Level
                if (item.level){
                    $('#level-column').show()
                    $('#item-edit-level').val(item.level)
                } else {
                    $('#item-edit-level').val('')
                    $('#level-column').hide()
                }
                modal.toggle()
            })
        })
    })

    $('#item-table thead tr')
        .clone(true)
        .addClass('filters')
        .appendTo('#item-table thead')

    // @ts-ignore
    $('#item-table').DataTable({
        orderCellsTop: true,
        fixedHeader: true,
        initComplete: function(){
            var api = this.api()

            api
                .columns()
                .eq(0)
                .each(function (columnIndex){
                    var cell = $('.filters th').eq($(api.column(columnIndex).header()).index())
                    var title = $(cell).text()

                    $(cell).html(`<input type="text" placeholder="${title}"/>`) 
                    $('input', $('.filters th').eq($(api.column(columnIndex).header()).index()))
                        .off('keyup change')
                        .on('change', function(e){
                            var elm = this as HTMLInputElement
                            $(elm).attr('title', $(elm).val())
                            var regexr = '({search})'
                            var cursorPosition = elm.selectionStart

                            api
                                .column(columnIndex)
                                .search(
                                    elm.value != '' ? regexr.replace('{search}', `(((${elm.value})))`) : '',
                                    elm.value != '',
                                    elm.value == ''
                                )
                                .draw()
                        })
                        .on('keyup', function (e){
                            e.stopPropagation()
                            $(this).trigger('change')
                            $(this).trigger('focus')[0]
                        })
                })
        }
    })
})

$('#item-submit').on('click', function(){
    let item = {} as Item
    item.table=$('#item-edit-form').attr('data-bs-table')
    item.id=parseInt($('#item-edit-form').attr('data-bs-id'))

    $('.item-edit[type=checkbox]').map(function() {
        const elm  = this as HTMLInputElement
        const att = elm.name

        if (att.indexOf('class') >= 0){
            if (elm.checked){
                let cat = {} as CategoryClass

                cat.id = parseInt(elm.value)
                cat.value = att.replace('class-', '')
                item.classes ? item.classes.push(cat) : item.classes = [cat]
            }
        } else {
            item[att] = elm.checked
        }
    })

    $('select.item-edit option:selected').map(function() {
        const elm = this as HTMLSelectElement
        let cat = {} as CategoryClass
        cat.id = parseInt(elm.value)
        cat.value = elm.innerText
        item[elm.parentElement.getAttribute('name')] = cat
    })

    $('.item-edit[type=text]').map(function() {
        const elm = this as HTMLInputElement
        item[elm.name] = elm.value
    })

    $('.item-edit[type=number]').map(function() {
        const elm = this as HTMLInputElement
        item[elm.name] = elm.value
    })

    updateItem(item)
})