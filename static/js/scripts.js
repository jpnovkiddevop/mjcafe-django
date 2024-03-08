

function addToCart(event) {
    console.log("clicked")
    event.preventDefault(); // This prevents the default behavior of the anchor tag
    // You can add your custom logic here, such as making an AJAX request to add the item to the cart
    // For example:
    var url = event.target.href; // Get the href attribute of the clicked anchor tag
    console.log(url)
    // Perform AJAX request
    fetch(url, {
        method: 'GET', // or 'POST' if your view requires POST method
        headers: {
            'Accept': 'application/json',
            // Add any headers required by your server
        },
        // Add any additional configurations or data as needed
    })
    .then(response => {
        // Handle the response as needed
        console.log('Item added to cart');
        updateCartQuantity();
    })
    .catch(error => {
        console.error('Error adding item to cart:', error);
    });
}


// function updateCartQuantity() {
//     var cartQuantity = 5
//     document.getElementById('cart-quantity').innerText = cartQuantity;
//     console.log(cartQuantity)
// }

