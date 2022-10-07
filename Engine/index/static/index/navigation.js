import { makeToastNotification } from "/static/helper.js"

const bell = document.getElementById('message-icon')


document.querySelectorAll(".nav-icon").forEach(icon => {
    icon.classList.add("load")
})

document.addEventListener("beforeunload", () => {
    document.querySelectorAll(".nav-icon").forEach(icon => {
        icon.classList.remove("load")
    })

})

function refreshMessages() {

    while (bell.nextElementSibling.firstChild) {
        bell.nextElementSibling.firstChild.remove()
    }
    const link = $('.messages').attr('link')

    let request = $.get(link, "json")

    request.done(function(messages) {
        if (messages.length == 0) {
            let html = $(`<p>`)
            html.addClass("message-body")
            html.text("No Notifications Yet")
            $('.messages').append(html)
        } else {
            for (const message of messages) {
                let messageContainer = $('<div>')
                messageContainer.addClass("message-container")
                if (message.type == 'buy') {
                    let html = $(`<p>`)

                    let htmlOption = $('<form>')
                    htmlOption.addClass("message-options")

                    let allowButton = $('<button>')
                    let denyButton = $('<button>')

                    allowButton.addClass("button request-button")
                    allowButton.attr('data-link', '/allow')
                    allowButton.attr('data-message-id', message.id)
                    allowButton.attr('data-user-id', message.sender)
                    allowButton.attr('type', 'submit')
                    allowButton.attr('data-reviewer-id', message.reviewer_id)
                    allowButton.text("Allow")

                    denyButton.addClass("button request-button")
                    denyButton.attr('data-link', '/deny')
                    denyButton.attr('data-message-id', message.id)
                    denyButton.attr('data-user-id', message.sender)
                    denyButton.attr('type', 'submit')
                    denyButton.attr('data-reviewer-id', message.reviewer_id)
                    denyButton.text("Deny")

                    html.addClass("message-body")
                    html.text(message.body)
                    htmlOption.append(denyButton)
                    htmlOption.append(allowButton)
                    messageContainer.append(html)
                    messageContainer.append(htmlOption)
                } else if (message.type == 'notification') {
                    let html = $(`<p>`)
                    html.addClass("message-body")
                    html.text(message.body)
                    messageContainer.append(html)
                }
                $('.messages').append(messageContainer)
            }
        }

    })

}

bell.addEventListener("click", () => {

    if (bell.nextElementSibling.classList.contains("active") == false) {

        const link = $('.messages').attr('link')

        let request = $.get(link, "json")

        request.done(function(messages) {
            if (messages.length == 0) {
                let html = $(`<p>`)
                html.addClass("message-body")
                html.text("No Notifications Yet")
                $('.messages').append(html)
            } else {
                for (const message of messages) {
                    let messageContainer = $('<div>')
                    messageContainer.addClass("message-container")
                    if (message.type == 'buy') {
                        let html = $(`<p>`)

                        let htmlOption = $('<form>')
                        htmlOption.addClass("message-options")

                        let allowButton = $('<button>')
                        let denyButton = $('<button>')

                        allowButton.addClass("button request-button")
                        allowButton.attr('data-link', '/allow')
                        allowButton.attr('data-message-id', message.id)
                        allowButton.attr('data-user-id', message.sender)
                        allowButton.attr('type', 'submit')
                        allowButton.attr('data-reviewer-id', message.reviewer_id)
                        allowButton.text("Allow")

                        denyButton.addClass("button request-button")
                        denyButton.attr('data-link', '/deny')
                        denyButton.attr('data-message-id', message.id)
                        denyButton.attr('data-user-id', message.sender)
                        denyButton.attr('type', 'submit')
                        denyButton.attr('data-reviewer-id', message.reviewer_id)
                        denyButton.text("Deny")

                        html.addClass("message-body")
                        html.text(message.body)
                        htmlOption.append(denyButton)
                        htmlOption.append(allowButton)
                        messageContainer.append(html)
                        messageContainer.append(htmlOption)
                    } else if (message.type == 'notification') {
                        let html = $(`<p>`)
                        html.addClass("message-body")
                        html.text(message.body)
                        messageContainer.append(html)
                    }
                    $('.messages').append(messageContainer)
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

$(document).ready(function() {
    if (document.querySelectorAll(".request-button") != null) {
        $(document).on('click', ".request-button", function(e) {

            e.preventDefault()

            const link = $(this).attr("data-link")
            const user_id = $(this).attr("data-user-id")
            const reviewer_id = $(this).attr("data-reviewer-id")
            const message_id = $(this).attr("data-message-id")

            let request = $.post(link, {
                user_id: user_id,
                reviewer_id: reviewer_id,
                message_id: message_id
            })

            request.done(function(data) {
                makeToastNotification(data.message)
            })

            request.fail(function() {
                makeToastNotification("Request Failed")
            })

            $(this).closest(".message-container").remove()
            refreshMessages()

        })
    }
})