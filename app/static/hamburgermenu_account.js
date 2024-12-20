// Wait for the DOM to be fully loaded before executing the script
document.addEventListener('DOMContentLoaded', function() {
    // Select elements
    var menu = document.querySelector(".nav-right");  // Select the nav-right by class
    var hamburger = document.querySelector(".hamburger-menu");

    // If the elements are not found, do nothing
    if (!menu || !hamburger) return;

    // Toggle the mobile menu (show/hide)
    hamburger.addEventListener("click", function() {
        menu.classList.toggle("show");  // Toggle the 'show' class to display/hide the menu
    });

    // Close the menu if the user clicks outside of it
    window.onclick = function(event) {
        // Close the menu if the click is outside the hamburger or menu
        if (!hamburger.contains(event.target) && !menu.contains(event.target)) {
            menu.classList.remove("show");
        }
    };
});
