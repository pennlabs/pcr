$(document).ready(function() {
    var cartCount = $("#cart-count");
    if (cartCount.length) {
        function refreshCartCount() {
            if (!localStorage || localStorage.length <= 0) {
                cartCount.hide();
            }
            else {
                cartCount.show().text(localStorage.length);
            }
        }
        refreshCartCount();
        setInterval(refreshCartCount, 1000);
    }
});
