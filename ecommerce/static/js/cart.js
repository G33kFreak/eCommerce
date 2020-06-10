var addBtns = document.getElementsByClassName('add-product')

for (i = 0; i < addBtns.length; i++) {
    addBtns[i].addEventListener('click', function () {
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId: ', productId, 'action: ', action)

        console.log('User: ', user)

        if (user === "AnonymousUser") {
            addCookieItem(productId, action)
        } else {
            updateUserOrder(productId, action)
        }
    })
}

function updateUserOrder(productId, action) {
    var url = '/update_item/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({ 'productId': productId, 'action': action })
    })

        .then((response) => {
            return response.json()
        })

        .then((data) => {
            console.log('data:', data)
            location.reload()
        })
}

function addCookieItem(productId, action) {
    if (action == 'add') {
        if (cart[productId] == undefined) {
            cart[productId] = { 'count': 1 }
        } else {
            cart[productId]['count'] += 1
        }
    }

    if (action == 'remove') {
        cart[productId]['count'] -= 1

        if (cart[productId]['count'] <= 0) {
            delete cart[productId]
        }
    }

    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
}