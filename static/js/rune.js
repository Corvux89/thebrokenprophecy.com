

function getTotal(){
    document.addEventListener('click', function(event){
        fetch(url)
            .then(console.log(url))

        var form = document.forms.runeForm;
        var data = new FormData(form);
        var object = {}
        data.forEach((value, key) => object[key] = value);
        $.ajax({
            url: "/runes/total",
            data: JSON.stringify(object),
            contentType: 'application/json;charset=UTF-8',
            type: 'POST',
            success: function(response){
                console.log(response)

                var x = document.getElementById("totalPoints");
                x.innerHTML = response.total
            }
        });
    })
}

getTotal()
