function addToCart(ghe_id, chuyen_bay_id, khach_hang_id, gia_ve) {
    fetch('/api/cart', {
        method: 'post',
        body: JSON.stringify({
            "ghe_id": ghe_id,
            "chuyen_bay_id": chuyen_bay_id,
            "khach_hang_id": khach_hang_id,
            "gia_ve": gia_ve
        }),
        headers: {
            'Context-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        var cart = document.getElementById("cart-info");
        cart.innerText = `${data.total_quantity} - ${data.total_amount} VND`;
        console.info(data);
    }).catch(err => {
        console.log(err);
    });

    // promise --> await/async
}

function pay() {
    fetch('/api/pay', {
        method: 'post',
        headers: {
            'Context-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        alert(data.message);
    }).catch(res => {
        console.log(res);
    });
}