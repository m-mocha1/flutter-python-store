function increaseQty(btn) {
    const input = btn.parentElement.querySelector('input');
    input.value = parseInt(input.value) + 1;
    updateTotal();
}

function decreaseQty(btn) {
    const input = btn.parentElement.querySelector('input');
    if (input.value > 1) {
        input.value = parseInt(input.value) - 1;
        updateTotal();
    }
}

function removeItem(btn) {
    btn.closest('.cart-item').remove();
    updateTotal();
    checkEmptyCart();
}

function updateTotal() {
    // Update individual totals and grand total
    const rows = document.querySelectorAll('.cart-item');
    let grandTotal = 0;

    rows.forEach(row => {
        const price = parseFloat(row.querySelector('.price').textContent.replace('$', ''));
        const qty = parseInt(row.querySelector('.quantity input').value);
        const total = price * qty;
        row.querySelector('.total').textContent = '$' + total.toFixed(2);
        grandTotal += total;
    });
}

function checkEmptyCart() {
    const items = document.querySelectorAll('.cart-item').length;
    if (items === 0) {
        document.querySelector('.empty-cart').style.display = 'block';
        document.querySelector('.cart-table').style.display = 'none';
    }
}