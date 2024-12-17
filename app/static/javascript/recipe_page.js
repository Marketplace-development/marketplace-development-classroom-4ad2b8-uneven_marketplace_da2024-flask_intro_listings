document.addEventListener("DOMContentLoaded", () => {
    // Toggle Favorites
    function toggleFavorite(button) {
        const recipeId = button.getAttribute("data-recipe-id");

        fetch("/favorites/toggle", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ recipe_id: recipeId }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Update button text and style
                button.textContent = data.is_favorite ? "❤️ Remove from Favorites" : "🤍 Add to Favorites";
                button.classList.toggle("favorited", data.is_favorite);
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("An error occurred while updating favorites.");
        });
    }

    // Add to Cart
    function addToCart(button) {
        const recipeId = button.getAttribute("data-recipe-id");

        fetch("/add-to-cart", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ recipe_id: recipeId }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                button.textContent = "✅ Added to Cart";
                button.disabled = true;
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("An error occurred while adding to the cart.");
        });
    }

    // Attach functions to global scope
    window.toggleFavorite = toggleFavorite;
    window.addToCart = addToCart;
});