document.addEventListener("DOMContentLoaded", () => {
    // Existing code: Search and filter logic
    const searchBar = document.getElementById("search-bar");
    const filterRegion = document.getElementById("filter-region");
    const recipesContainer = document.getElementById("submitted-recipes-container");
    const recipeBoxes = recipesContainer.querySelectorAll(".recipe-box");

    const filterRecipes = () => {
        const searchTerm = searchBar.value.toLowerCase();
        const selectedRegion = filterRegion.value;

        recipeBoxes.forEach((box) => {
            const title = box.getAttribute("data-title").toLowerCase();
            const region = box.getAttribute("data-region");

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

    searchBar.addEventListener("input", filterRecipes);
    filterRegion.addEventListener("change", filterRecipes);

    // New code: Reset filters logic
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