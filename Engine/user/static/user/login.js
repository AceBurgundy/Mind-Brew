import { eyeToggle } from "/static/helper.js";

const toRegister = document.querySelector("#to-register");
// const toLogin = document.querySelector("#to-login");

eyeToggle(
    document.getElementById('logpassword-icon-container'),
    document.getElementById('logpassword'),
    document.getElementById('logeye'),
    document.getElementById('log-eye-off')
)

window.addEventListener("load", () => {

    var formContainer = document.querySelector('.login');
    formContainer.addEventListener('touchmove', preventKeyBoardScroll, { passive: false });

    function preventKeyBoardScroll(e) {
        e.preventDefault();
        e.stopPropagation();
        return false;
    }
})

toRegister.addEventListener("click", () => {
    window.location = "/register"
})