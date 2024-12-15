document.addEventListener("DOMContentLoaded", () => {
    const favoriteButtons = document.querySelectorAll(".favorite-button");

    favoriteButtons.forEach(button => {
        button.addEventListener("click", () => {
            const recipeId = button.dataset.recipeId;
            const isFavorited = button.classList.contains("favorited");
            const isFavoritesPage = window.location.pathname.includes("/favorites");

            // Send toggle request
            fetch("/favorites/toggle", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ recipe_id: recipeId })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Toggle heart state
                    button.classList.toggle("favorited");
                    button.innerHTML = button.classList.contains("favorited") ? "❤️" : "🤍";

                    // Remove recipe if on Favorites Page
                    if (isFavoritesPage && !button.classList.contains("favorited")) {
                        const recipeBox = button.closest(".recipe-box");
                        recipeBox.remove();
                    }
                } else {
                    alert(data.message);
                }
            })
            .catch(error => console.error("Error:", error));
        });
    });
});