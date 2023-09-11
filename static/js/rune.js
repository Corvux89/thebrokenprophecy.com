function onLoad(){
    // Button
    document.getElementById('generate-button').addEventListener('click', function(event){
        var fields = {}
        $('#weaponForm').find("input, textarea").each(function(){
            if (this.type == 'radio' || this.type == 'checkbox'){
                if (this.checked){
                    fields[this.name] = $(this).val()
                }
            } else{
                fields[this.name] = $(this).val()
            }
        })

        console.log(fields)

        if (fields['weapon-name'] !== "" && fields['damage-die'] !== "" && fields['damage-type'] !== ""){
            $.ajax({
                url: document.getElementById('weaponURL').innerHTML,
                data: fields,
                dataType: 'json',
                type: "post",
                success: function(response){
                    document.getElementById('command-text').innerHTML = `!a import ` + JSON.stringify(response)
                    $('#weaponModal').modal('show')

                    document.getElementById('command-copy').addEventListener('click', function(event){
                        var text = document.getElementById('command-text').innerHTML

                        if (text){
                            navigator.clipboard.writeText(text)
                        }
                    })
                }
            })
        }
    })

    // Runes
    var all_runes = document.getElementsByClassName('rune')
    Array.from(all_runes).forEach((rune) => {
        console.log(rune)
        document.getElementById(rune.id).onclick = function(){
            var runeDom = document.getElementById('rune-count')
            var runeCount = parseInt(runeDom.innerHTML)
            var runeMax = parseInt(document.getElementById('rune-total').innerHTML)

            if (this.checked){
                runeCount += 1
            } else {
                runeCount -= 1
            }

            runeDom.innerText = runeCount

            if (runeCount == runeMax){
                runeDom.classList.add("text-success")
                runeDom.classList.remove("text-danger")
            } else if (runeCount < runeMax){
                runeDom.classList.remove("text-success")
                runeDom.classList.remove("text-danger")
            } else if (runeCount > runeMax){
                runeDom.classList.add("text-danger")
                runeDom.classList.remove("text-success")
            }

        }
    })

    // Upgrades
    var upgradeable_runes = document.getElementsByClassName('upgrade')
    Array.from(upgradeable_runes).forEach((rune) =>{
        document.getElementById(rune.id).onchange = function(){
            var sections = document.getElementsByClassName(`${rune.id}-upgrades`)
            Array.from(sections).forEach((section) =>{
                if (this.checked){
                    section.hidden=false
                } else {
                    section.hidden=true
                }
            })
        }
    })

    // Inputs
    var inputFields = document.querySelectorAll('input')
    inputFields.forEach(input => {
        input.addEventListener('input', saveToLocalStorage)
        loadFromLocalStorage(input)
    })

    var textArea = document.querySelectorAll('textarea')
    textArea.forEach(input =>{
        input.addEventListener('input', saveToLocalStorage)
        loadFromLocalStorage(input)
    })
}

function saveToLocalStorage(){
    var weapon = JSON.parse(localStorage.getItem("customWeapon") || "{}")
    var inputName = this.name
    var inputValue = this.value
    if (this.type == 'checkbox' && this.checked == false){
        delete weapon[inputName]
    } else {
        weapon[inputName] = inputValue
    }
    localStorage.setItem("customWeapon", JSON.stringify(weapon))
}

function loadFromLocalStorage(input){
    var weapon = JSON.parse(localStorage.getItem("customWeapon") || "{}")
    var inputName = input.name
    var value = weapon[inputName]
    var change = new Event('change')
    var click = new Event('click')

    if (value !== null && value){
        if (input.type === 'radio' || input.type == 'checkbox'){
            if (input.value == value){
                input.checked = true
                input.dispatchEvent(change)
                input.dispatchEvent(click)
            }
        } else{
            input.value = value
        }
    }
}

onLoad()