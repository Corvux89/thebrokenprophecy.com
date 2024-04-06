document.querySelectorAll(".delete-button").forEach(elm => {
    elm.addEventListener("click", function(event){
        var url = `${window.location.href}`
        var redirect = $(this).attr('data-href')
        fetch(url, {
            method: 'DELETE'
        })
        .then(function(response){
            if (!response.ok){
                conole.log("Error", response)
            } else{
                window.location.href = redirect
            }
        })
    })
})

document.querySelectorAll(".edit-button").forEach(elm => {
    elm.addEventListener("click", function(event){
        var elm = event.target
        var table = $(this).attr("data-table")
        var item_id = elm.getAttribute("data-item-id")
        var form = document.querySelector(`#item-edit`)
        var formData = new FormData(form)
        var url = `${window.location.href}`
        var redirect = $(this).attr('data-href')

        fetch(url, {
            method: 'PATCH',
            body: formData
        })
        .then(function(response){
          if (!response.ok){
              console.log("Error", response)
          } else{
              console.log(`Success editing item ${item_id}`)
              window.location.href = redirect
          }
        })
    })
})