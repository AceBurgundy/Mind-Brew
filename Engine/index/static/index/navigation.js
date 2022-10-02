const bell = document.getElementById('message-icon')

document.querySelectorAll(".nav-icon").forEach(icon => {
    icon.classList.add("load")
})

document.addEventListener("beforeunload", () => {
    document.querySelectorAll(".nav-icon").forEach(icon => {
        icon.classList.remove("load")
    })

})

bell.addEventListener("click", () => {

    if (bell.nextElementSibling.classList.contains("active") == false) {

        const link = $('.messages').attr('link')

        let request = $.get(link, "json")

        request.done(function(messages) {

            if (messages.length == 0) {
                let html = $(`<p>`)
                html.addClass("notif")
                html.text("No Notifications Yet")
                $('.messages').append(html)
            } else {
                for (message of messages) {
                    let html = $(`<p>`)
                    html.addClass("notif")
                    html.text(message)
                    $('.messages').append(html)
                }
            }

        })

        bell.nextElementSibling.classList.add("active")
    } else {

        while (bell.nextElementSibling.firstChild) {
            bell.nextElementSibling.firstChild.remove()
        }

        bell.nextElementSibling.classList.remove("active")

    }

})