function toggleDropdown() {
    const dropdown = document.getElementById('dropdownMenu');
    const arrow = document.getElementById('dropdownArrow');

    if (dropdown.style.display === 'block') {
        dropdown.style.display = 'none';
        arrow.classList.remove('open');
    } else {
        dropdown.style.display = 'block';
        arrow.classList.add('open');
    }
}

// Sluit het menu als je ergens anders klikt
window.onclick = function(event) {
    if (!event.target.closest('.profile-dropdown')) {
        const dropdown = document.getElementById('dropdownMenu');
        const arrow = document.getElementById('dropdownArrow');
        if (dropdown.style.display === 'block') {
            dropdown.style.display = 'none';
            arrow.classList.remove('open');
        }
    }
};


