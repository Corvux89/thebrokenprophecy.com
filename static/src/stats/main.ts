import { getCharacters, getClasses, getRaces } from "../api.js";
import { Counts, PlayerClass } from "../types.js";

getRaces()
.then(races => {
    getClasses()
    .then (classes => {
        var multiclass = {} as PlayerClass
        multiclass.id = 99999
        multiclass.value = "Multiclass",
        multiclass.subclasses = []
        classes.push(multiclass)
        getCharacters()
        .then (characters => {
            const classCount: Counts = {}
            const subclassCount: Counts = {}
            const raceCount: Counts = {}
            const subraceCount: Counts = {}
            $('#total-players').html(`${characters.length}`)
            characters.forEach(character => {
                character.classes.forEach(primaryClass => {
                    classCount[primaryClass.id] ? classCount[primaryClass.id]++ : classCount[primaryClass.id] = 1

                    primaryClass.subclasses.forEach(subClass => {
                        subclassCount[subClass.id] ? subclassCount[subClass.id]++ : subclassCount[subClass.id] = 1
                    })
                })

                if (character.classes.length > 1){
                    classCount[multiclass.id] ? classCount[multiclass.id]++ : classCount[multiclass.id] = 1
                }
                raceCount[character.race.id] ? raceCount[character.race.id]++ : raceCount[character.race.id]=1
                if (character.subrace){
                    subraceCount[character.subrace.id] ? subraceCount[character.subrace.id]++ : subraceCount[character.subrace.id]=1
                }
            })

            races.forEach(race => {
                $("#race-dropdown").append(`<a class="dropdown-item" href="#${race.value}">${race.value}</a>`)
                let row1=document.createElement("tr")
                const raceNum = raceCount[race.id] ? raceCount[race.id] : 0
                if (race.subraces.length > 0){
                    row1.classList.add("accordion-toggle")
                    row1.id = race.value
                    row1.setAttribute("data-bs-toggle", "collapse")
                    row1.setAttribute("data-bs-target", `#${race.value}collapse`)

                    row1.innerHTML = `<td class="label"><button class="btn btn-xs"><span class="race-name text-white">${race.value}*</span></button></td>`
                } else {
                    row1.innerHTML = `<td class="label ps-4">${race.value}</td>`
                }
                row1.innerHTML += `<td class="count">${raceNum}</td>`

                $('#race-table-body').append(row1)

                if (race.subraces.length > 0){
                    let row2 = document.createElement("tr")
                    let subRows = ""
                    
                    race.subraces.forEach(subrace => {
                        const subraceNum = subraceCount[subrace.id] ? subraceCount[subrace.id] : 0
                        subRows += `
                            <tr>
                                <td class="label">${subrace.value}</td>
                                <td class="count">${subraceNum}</td>
                            </tr>
                        `
                    })

                    row2.innerHTML = `
                        <td colspan="1" class="hiddenRow p-0">
                            <div class="accordion-body collapse show subrace-collapse" id="${race.value}collapse">
                                <table class="table table-secondary table-sm mb-0">
                                    <thead>
                                        <tr>
                                            <th scope="col" class="columnLabel">Subrace</th>
                                            <th scole="col" class="columnCount">#</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        ${subRows}
                                    </tbody>
                                </table>
                            </div>
                        </td>
                    `
                    $('#race-table-body').append(row2)
                }
            })

            classes.forEach(cls => {
                $("#class-dropdown").append(`<a class="dropdown-item" href="#${cls.value}">${cls.value}</a>`)
                let row1=document.createElement("tr")
                const classNum = classCount[cls.id] ? classCount[cls.id] : 0
                if (cls.subclasses.length > 0){
                    row1.classList.add("accordion-toggle")
                    row1.id = cls.value
                    row1.setAttribute("data-bs-toggle", "collapse")
                    row1.setAttribute("data-bs-target", `#${cls.value}collapse`)

                    row1.innerHTML = `<td><button class="btn btn-xs"><span class="class-name text-white">${cls.value}*</span></button></td>`
                } else {
                    row1.innerHTML = `<td class="label ps-4">${cls.value}</td>`
                }
                row1.innerHTML += `<td class="count">${classNum}</td>`

                $('#class-table-body').append(row1)

                if (cls.subclasses.length > 0){
                    let row2 = document.createElement("tr")
                    let subRows = ""

                    cls.subclasses.forEach(subclass => {
                        const subclassNum = subclassCount[subclass.id] ? subclassCount[subclass.id] : 0

                        subRows += `
                            <tr>
                                <td class="label">${subclass.value}</td>
                                <td class="count">${subclassNum}</td>
                            </tr>
                        `
                    })

                    row2.innerHTML = `
                        <tr>
                            <td colspan="1" class="hiddenRow p-0">
                                <div class="accordion-body show subclass-collapse" id="${cls.value}collapse">
                                    <table class="table table-secondary table-sm mb-0">
                                        <thead>
                                            <tr>
                                                <th scope="col" class="columnLabel">Subclass</th>
                                                <th scope="col" class="columnCount">#</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            ${subRows}
                                        </tbody>
                                    </table>
                                </div>
                            </td>
                        </tr>
                    `

                    $('#class-table-body').append(row2)
                }
            })
        })
    })
})



$('#subraceCollapse').on('click', function() {
    if ($(this).data("closedAll")){
        $(".subrace-collapse").collapse("show")
    } else {
        $(".subrace-collapse").collapse("hide")
    }

    $(this).data("closedAll",!$(this).data("closedAll"));
})

$('#subclassCollapse').on('click', function(){
    if ($(this).data("closedAll")) {
        $(".subclass-collapse").collapse("show");
    } else {
        $(".subclass-collapse").collapse("hide");
    }

    // save last state
    $(this).data("closedAll",!$(this).data("closedAll"));
});