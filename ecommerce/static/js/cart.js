var addBtns = document.getElementsByClassName('add-product')

for (i = 0; i < addBtns.length; i++) {
    addBtns[i].addEventListener('click', function () {
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId: ', productId, 'action: ', action)

        console.log('User: ', user)
    })
}