document.addEventListener("DOMContentLoaded", () => {
    const searchBar = document.getElementById("search-bar");
    const filterRegion = document.getElementById("filter-region");
    const recipesContainer = document.getElementById("submitted-recipes-container");
    const recipeBoxes = recipesContainer.querySelectorAll(".recipe-box");

    // Filter Recipes Function
    const filterRecipes = () => {
        const searchTerm = searchBar.value.toLowerCase();
        const selectedRegion = filterRegion.value;

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

    searchBar.addEventListener("input", filterRecipes);
    filterRegion.addEventListener("change", filterRecipes);

    // Reset Filters
    const resetButton = document.querySelector(".btn-reset-filters");
    if (resetButton) {
        resetButton.addEventListener("click", () => {
            searchBar.value = "";
            filterRegion.value = "";
            filterRecipes(); // Reset and reapply filters
        });
    }

    // Favorite Button Toggle
    const favoriteButtons = document.querySelectorAll(".favorite-button");
    favoriteButtons.forEach((button) => {
        button.addEventListener("click", () => {
            const recipeId = button.dataset.recipeId;
            const isFavorited = button.classList.contains("favorited");

            fetch("/favorites/toggle", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ recipe_id: recipeId }),
            })
                .then((response) => response.json())
                .then((data) => {
                    if (data.success) {
                        button.classList.toggle("favorited", !isFavorited);
                        button.textContent = isFavorited ? "🤍" : "❤️";
                    }
                })
                .catch((error) => console.error("Error:", error));
        });
    });
});