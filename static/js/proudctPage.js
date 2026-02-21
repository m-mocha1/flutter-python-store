function changeImage(src) {
    document.getElementById('mainImage').src = src;
}

function increaseQty() {
    let qty = document.getElementById('quantity');
    if (parseInt(qty.value) < parseInt(qty.max)) {
        qty.value = parseInt(qty.value) + 1;
    }
}

function decreaseQty() {
    let qty = document.getElementById('quantity');
    if (qty.value > 1) {
        qty.value = parseInt(qty.value) - 1;
    }
}

function addToCart(productId, productName) {
    let qty = document.getElementById('quantity').value;
    alert(qty + ' x ' + productName + ' added to cart!');
    // You can add cart logic here later
}