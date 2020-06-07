var addBtns = document.getElementsByClassName('add-product')

for (i = 0; i < addBtns.length; i++) {
    addBtns[i].addEventListener('click', function () {
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId: ', productId, 'action: ', action)

        console.log('User: ', user)

        if (user === "AnonymousUser") {
            console.log("Not logged in")
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
