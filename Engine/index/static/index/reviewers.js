import { makeToastNotification } from "/static/helper.js"

if (document.querySelectorAll(".unavailable") != false) {
    document.querySelectorAll(".unavailable").forEach(unavailbleReviewer => {
        unavailbleReviewer.parentElement.style.opacity = 0.6;
        unavailbleReviewer.parentElement.style.pointerEvents = 'none';
    })
}

document.querySelectorAll(".shopping-cart-line").forEach(shoppingCart => {
    shoppingCart.addEventListener("mouseover", () => {
        shoppingCart.children[3].style.transition = '300ms'
        shoppingCart.children[3].setAttribute("fill", "#c4c3cd")
    })
    shoppingCart.addEventListener("mouseout", () => {
        shoppingCart.children[3].setAttribute("fill", "none")
    })
})

$(document).ready(function() {
    $(".buy-button").on('click', function(event) {
        makeToastNotification("Notifying Admin")
        const link = $(this).attr('data-link')
        event.preventDefault()
        let request = $.get(
            link, "json")
        request.done(function(data) {
            makeToastNotification(data.message)
        })
        request.fail(function() {
            makeToastNotification("Failed to buy reviewer")
        })
    })
})