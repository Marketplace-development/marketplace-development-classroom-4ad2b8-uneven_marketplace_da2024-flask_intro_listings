function purchaseAll() {
    fetch("/cart/purchase", { method: "POST" })
        .then((response) => response.json())
        .then((data) => {
            alert(data.message);
            window.location.href = "/purchased-recipes"; // Redirect to purchased recipes
        });
}