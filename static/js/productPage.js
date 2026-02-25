document.addEventListener("DOMContentLoaded", () => {
    const display = document.getElementById("qty-display");
    const decBtn = document.getElementById("qty-decrease");
    const incBtn = document.getElementById("qty-increase");
    const hiddenQtyInput = document.getElementById("add-to-cart-qty");

    if (!display || !decBtn || !incBtn || !hiddenQtyInput) return;

    const maxStock = parseInt(display.dataset.maxStock || "1", 10);
    let qty = 1;

    function update() {
        display.textContent = qty;
        hiddenQtyInput.value = qty;
        decBtn.disabled = qty <= 1;
        incBtn.disabled = qty >= maxStock;
    }

    decBtn.addEventListener("click", () => {
        if (qty > 1) {
            qty -= 1;
            update();
        }
    });

    incBtn.addEventListener("click", () => {
        if (qty < maxStock) {
            qty += 1;
            update();
        }
    });

    update();
});