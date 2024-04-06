document.querySelectorAll(".delete-button").forEach(elm => {
    elm.addEventListener("click", function(event){
        var messageID = $(this).attr("data-id")
        var url = `${window.location.href}/${messageID}`
        var redirectURL = $(this).attr("data-href")

        fetch(url, {
            method: 'DELETE'
        })
            .then(function(response){
            if (!response.ok){
                console.log("Error", response)
            } else{
                console.log(`Deleted message ${messageID}`)
                window.location.href = redirectURL
            }
        })
    })
})

document.querySelectorAll(".edit-button").forEach(elm => {
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
                console.log(`Successfully edited message ${messageID}`)
                window.location.href = redirectURL
            }
        })
    })
})