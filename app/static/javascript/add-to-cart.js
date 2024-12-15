document.addEventListener("DOMContentLoaded", () => {
    // Function to add recipe to the cart
    async function addToCart(button) {
        const recipeId = button.getAttribute("data-recipe-id");

        try {
            const response = await fetch("{{ url_for('routes.add_to_cart') }}", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ recipe_id: recipeId }),
            });

            const data = await response.json();

            if (data.success) {
                button.innerHTML = "✔️ Added!";
                button.disabled = true;
            } else {
                alert("Failed to add to cart: " + data.message);
            }
        } catch (error) {
            console.error("Error:", error);
            alert("An error occurred. Please try again.");
        }
    }

    // Attach the function to all "Add to Cart" buttons
    document.querySelectorAll(".btn-add-to-cart").forEach((button) => {
        button.addEventListener("click", function () {
            addToCart(this);
        });
    });
});