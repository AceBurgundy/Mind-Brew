import { counter, eyeToggle } from "/static/helper.js"

const profileSection = document.getElementById('profile-section')
const profileCancelButton = document.querySelector(".profile-close-button");
const profileXButton = document.querySelector(".profile-x-button");

window.addEventListener("load", () => {
    profileSection.classList.toggle("active")
    if ((document.querySelector(".error")) === null) {
        if (document.readyState == "complete") {
            profileSection.classList.toggle("active")
        }
    }
})

window.addEventListener("DOMContentLoaded", () => {
    if ((document.querySelector(".error")) !== null) {
        profileSection.style.transform = "translate(-50%, -50%)"
        profileSection.style.transition = "-10ms"
        profileSection.style.opacity = "1"
    }
})

profileXButton.addEventListener('click', () => {
    if (profileSection.classList.contains("active")) {
        profileSection.classList.remove("active")
        setTimeout(() => {
            window.history.back();
        }, 300);
    } else {
        profileSection.style.transition = "500ms"
        profileSection.style.transform = "translate(-50%, -40%)"
        profileSection.style.opacity = "0"
        setTimeout(() => {
            window.history.back();
        }, 300);
    }
})



profileCancelButton.addEventListener('click', () => {
    if (profileSection.classList.contains("active")) {
        profileSection.classList.remove("active")
        setTimeout(() => {
            window.history.back();
        }, 300);
    } else {
        profileSection.style.transition = "500ms"
        profileSection.style.transform = "translate(-50%, -40%)"
        profileSection.style.opacity = "0"
        setTimeout(() => {
            window.history.back();
        }, 300);
    }
})

counter(
    document.getElementById("first-name"),
    document.getElementById("first-name-counter"),
    60
)

counter(
    document.getElementById("last-name"),
    document.getElementById("last-name-counter"),
    60
)

counter(
    document.getElementById("school"),
    document.getElementById("school-counter"),
    300
)

counter(
    document.getElementById("course"),
    document.getElementById("course-counter"),
    200
)

document.querySelector("#save-button").addEventListener("submit", function(event) {
    event.preventDefault();

    const profileSection = document.getElementById('profile-section')

    profileSection.classList.toggle("active")
})

const newPasswordModal = document.querySelector(".new-password-modal")
const changePasswordButton = document.querySelector(".change-password")

changePasswordButton.addEventListener(("click"), () => {
    newPasswordModal.classList.add("active")
})

const newPasswordModalCloseButton = document.querySelector("#new-password-close-button");

newPasswordModalCloseButton.addEventListener(("click"), () => {
    newPasswordModal.classList.remove("active")
})

eyeToggle(
    document.getElementById("verify-eyes-icon-container"),
    document.querySelector("#old-password-input"),
    document.querySelector("#verify-eye"),
    document.querySelector("#verify-eye-off")
)

eyeToggle(
    document.getElementById("new-password-eyes-icon-container"),
    document.querySelector("#old-password-input"),
    document.querySelector("#verify-eye"),
    document.querySelector("#verify-eye-off")
)