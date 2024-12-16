document.addEventListener("DOMContentLoaded", () => {
    const favoriteButtons = document.querySelectorAll(".favorite-button");

    favoriteButtons.forEach(button => {
        button.addEventListener("click", (event) => {
            event.preventDefault(); // Prevent default action like link navigation
            event.stopPropagation(); // Stop event bubbling to parent elements

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

                    // Remove recipe box dynamically if unfavorited on Favorites Page
                    if (isFavoritesPage && !button.classList.contains("favorited")) {
                        const recipeBox = button.closest(".recipe-box");
                        if (recipeBox) recipeBox.remove();
                    }
                } else {
                    alert(data.message || "An error occurred while updating favorites.");
                }
            })
            .catch(error => {
                console.error("Error:", error);
                alert("An error occurred. Please try again.");
            });
        });
    });
});