function addToCart(button) {
    const recipeId = button.getAttribute("data-recipe-id");

    fetch("/add-to-cart", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ recipe_id: recipeId }),
    })
    .then((response) => {
        if (response.ok) {
            return response.json();
        }
        throw new Error("Failed to add to cart");
    })
    .then((data) => {
        if (data.success) {
            button.textContent = "✅ Added!";
            button.disabled = true;

            // Fetch and update the cart count
            updateCartCount();
        } else {
            alert(data.message || "An error occurred. Please try again.");
        }
    })
    .catch((error) => {
        console.error("Error:", error);
        alert("An error occurred. Please try again.");
    });
}

// Function to update the cart count dynamically
function updateCartCount() {
    fetch("/cart-count", {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
    })
    .then((response) => response.json())
    .then((data) => {
        if (data.success) {
            // Update the cart count in the navbar
            const cartCountElement = document.getElementById("cart-count");
            if (cartCountElement) {
                cartCountElement.textContent = data.count;
            }
        }
    })
    .catch((error) => {
        console.error("Error updating cart count:", error);
    });
}

function removeFromCart(button) {
    const recipeId = button.getAttribute("data-recipe-id"); // Fetch recipe ID

    fetch("/remove-from-cart", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ recipe_id: recipeId }),
    })
    .then((response) => {
        if (response.ok) {
            return response.json();
        }
        throw new Error("Failed to remove from cart");
    })
    .then((data) => {
        if (data.success) {
            // Find and remove the cart-item element dynamically
            const cartItem = button.closest(".cart-item");
            if (cartItem) {
                cartItem.remove(); // Remove the element from the DOM
            }

            // Update the cart count dynamically
            updateCartCount();

            // Optional: Show a success confirmation
            alert("Recipe removed from cart!");
        } else {
            alert("Could not remove the recipe. Please try again.");
        }
    })
    .catch((error) => {
        console.error("Error:", error);
        alert("An error occurred while removing the recipe.");
    });
}

// Function to update the cart count
function updateCartCount() {
    fetch("/cart-count", {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
    })
    .then((response) => response.json())
    .then((data) => {
        if (data.success) {
            // Update the cart count element in the navbar
            const cartCountElement = document.getElementById("cart-count");
            if (cartCountElement) {
                cartCountElement.textContent = data.count;
            }
        }
    })
    .catch((error) => {
        console.error("Error updating cart count:", error);
    });
}

function purchaseAll() {
    fetch("/purchase-all", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
    })
    .then((response) => {
        if (response.ok) {
            return response.json();
        }
        throw new Error("Failed to purchase items");
    })
    .then((data) => {
        if (data.success) {
            alert("All recipes purchased successfully!");

            // Clear all cart items from the DOM
            const cartContainer = document.querySelector(".cart-items");
            if (cartContainer) {
                cartContainer.innerHTML = ""; // Remove all cart items
            }

            // Update the cart count dynamically
            updateCartCount();
        } else {
            alert(data.message || "Failed to complete the purchase.");
        }
    })
    .catch((error) => {
        console.error("Error:", error);
        alert("An error occurred while processing the purchase.");
    });
}