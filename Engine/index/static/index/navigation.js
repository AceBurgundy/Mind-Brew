const bell = document.getElementById('message-icon')

bell.addEventListener("click", () => {

    if (bell.nextElementSibling.classList.contains("active") == false) {

        const link = $('.messages').attr('link')

        let request = $.get(link, "json")

        request.done(function(newMessageList) {

            for (message of newMessageList) {
                let html = $(`<p>`)
                html.addClass("notif")
                html.text(message)
                $('.messages').append(html)
            }

            previousMessageList = newMessageList

        })

        bell.nextElementSibling.classList.add("active")
    } else {

        while (bell.nextElementSibling.firstChild) {
            bell.nextElementSibling.firstChild.remove()
        }

        bell.nextElementSibling.classList.remove("active")

    }

})

// $(function() {
//     setInterval(function() {
//         const link = $('.messages').attr('link')

//         let request = $.get(link, "json")

//         request.done(function(data) {
//             for (const message of data) {
//                 let html = $(`<p>`)
//                 html.addClass("notif")
//                 html.text(message)
//                 $('.messages').append(html)
//             }
//     }, 100000);
// });

// unfinished poll for new Messages