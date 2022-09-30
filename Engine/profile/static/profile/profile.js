const profileSection = document.getElementById('profile-section')
const profileCancelButton = document.querySelector("#return-to-previous");

window.addEventListener("load", () => {
    profileSection.classList.toggle("active")
})

window.addEventListener("DOMContentLoaded", () => {
    if ((document.querySelector(".error")) !== null) {
        profileSection.style.transform = "translate(-50%, -50%)"
        profileSection.style.transition = "-10ms"
        profileSection.style.opacity = "1"
    }
})

profileCancelButton.addEventListener('click', () => {
    if (profileSection.classList.contains("active")) {
        profileSection.classList.remove("active")
        setTimeout(() => {
            window.location = '/';
        }, 300);
    } else {
        profileSection.style.transition = "500ms"
        profileSection.style.transform = "translate(-50%, -40%)"
        profileSection.style.opacity = "0"
        setTimeout(() => {
            window.location = '/';
        }, 300);
    }
})