document.addEventListener("click", (e) => {
    if (e.target.classList.contains("remove-btn")) {
        const recipeId = e.target.dataset.recipeId;

        fetch("/cart/remove", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ recipe_id: recipeId }),
        })
            .then((response) => response.json())
            .then((data) => {
                alert(data.message);
                window.location.reload(); // Reload the page
            });
    }
});