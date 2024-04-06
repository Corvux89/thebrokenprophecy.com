document.querySelectorAll(".delete-button").forEach(elm => {
    elm.addEventListener("click", function(event){
        var parentID = $(this).attr("data-id")
        var url = $(this).attr("data-href")

        fetch(url, {
            method: 'DELETE'
        })
        .then(function(response){
          if (!response.ok){
              console.log("Error", response)
          } else{
              console.log(`Success deleting message ${parentID}`)
              window.location.href = url
          }
        })
    })
})

document.querySelectorAll(".edit-button").forEach(elm => {
    console.log(elm)
    elm.addEventListener("click", function(event){
        var messageID = $(this).attr("data-id")
        var form = document.querySelector(`#message-${messageID}`)
        var formData = new FormData(form)
        var url = `${window.location.href}/${messageID}`
        var redirectURL = $(this).attr("data-href")

        fetch(url, {
            method: 'PATCH',
            body: formData
        })
        .then(function(response){
          if (!response.ok){
              console.log("Error", response)
          } else{
              console.log(`Success editing message ${messageID}`)
              window.location.href = redirectURL
          }
        })
    })
})