document.addEventListener("DOMContentLoaded", () => {
    // Favorite Button Logic
    document.querySelectorAll(".btn-favorite").forEach(button => {
        button.addEventListener("click", () => {
            const recipeId = button.dataset.recipeId;

            fetch("/favorites/toggle", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ recipe_id: recipeId })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    button.textContent = data.is_favorite 
                        ? "❤️ Remove from Favorites" 
                        : "🤍 Add to Favorites";
                } else {
                    alert(data.message);
                }
            })
            .catch(error => console.error("Error:", error));
        });
    });

    // Add to Cart Button Logic
    document.querySelectorAll(".btn-cart").forEach(button => {
        button.addEventListener("click", () => {
            const recipeId = button.dataset.recipeId;

            fetch("/add-to-cart", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ recipe_id: recipeId })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert("Recipe added to cart!");
                } else {
                    alert(data.message);
                }
            })
            .catch(error => console.error("Error:", error));
        });
    });

    // Filter Recipes Logic
    const searchBar = document.getElementById("search-bar");
    const filterRegion = document.getElementById("region-filter");
    const recipesContainer = document.getElementById("recipes-container");
    const recipeBoxes = recipesContainer.querySelectorAll(".recipe-box");

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
                box.style.display = "flex"; // Show matching recipes
            } else {
                box.style.display = "none"; // Hide non-matching recipes
            }
        });
    };

    // Attach events to search bar and region dropdown
    searchBar.addEventListener("input", filterRecipes);
    filterRegion.addEventListener("change", filterRecipes);

    // Reset Button Logic
    const resetButton = document.getElementById("reset-button");
    if (resetButton) {
        resetButton.addEventListener("click", () => {
            searchBar.value = ""; // Clear search bar
            filterRegion.selectedIndex = 0; // Reset dropdown to default

            // Show all recipes
            recipeBoxes.forEach((box) => {
                box.style.display = "flex";
            });
        });
    }
});