function toggleMenu() {
    const menu = document.getElementById("menu");
    menu.classList.toggle("show");
}

// Sluit het menu als er buiten het menu wordt geklikt
window.onclick = function(event) {
    var menu = document.getElementById("nav-menu");
    var hamburger = document.querySelector(".hamburger-menu");

    // Als de klik buiten de hamburger of het menu is, sluit dan het menu
    if (!hamburger.contains(event.target) && !menu.contains(event.target)) {
        menu.classList.remove("show");
    }
}

// Voeg dit toe om te voorkomen dat het menu wordt gesloten wanneer een item binnen het menu wordt aangeklikt
document.querySelectorAll(".nav-right a").forEach(item => {
    item.addEventListener("click", function(event) {
        event.stopPropagation(); // Voorkom dat het klik-event buiten het menu wordt geregistreerd
    });
});