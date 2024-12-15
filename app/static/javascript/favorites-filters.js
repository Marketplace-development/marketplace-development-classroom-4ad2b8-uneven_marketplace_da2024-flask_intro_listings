document.addEventListener("DOMContentLoaded", () => {
    // Get DOM elements
    const searchBar = document.getElementById("search-bar");
    const filterRegion = document.getElementById("filter-region");
    const recipesContainer = document.getElementById("favorites-recipes-container");
    const recipeBoxes = recipesContainer.querySelectorAll(".recipe-box");

    // Filter logic
    const filterRecipes = () => {
        const searchTerm = searchBar.value.toLowerCase();
        const selectedRegion = filterRegion.value.toLowerCase();

        recipeBoxes.forEach((box) => {
            const title = box.getAttribute("data-title").toLowerCase();
            const region = box.getAttribute("data-region").toLowerCase();

            // Check if recipe matches search and region filter
            const matchesSearch = title.includes(searchTerm);
            const matchesRegion = !selectedRegion || region === selectedRegion;

            if (matchesSearch && matchesRegion) {
                box.style.display = "flex";
            } else {
                box.style.display = "none";
            }
        });
    };

    // Attach events
    searchBar.addEventListener("input", filterRecipes);
    filterRegion.addEventListener("change", filterRecipes);

    // Reset filters logic
    const resetFilters = () => {
        const form = document.querySelector(".filter-form");
        form.querySelector('input[name="search"]').value = ""; // Clear search input
        form.querySelector('select[name="region"]').value = ""; // Reset dropdown
        form.submit(); // Submit the form to reload the page without filters
    };

    // Attach reset functionality to the reset button
    const resetButton = document.querySelector(".btn-reset-filters");
    if (resetButton) {
        resetButton.addEventListener("click", resetFilters);
    }
});