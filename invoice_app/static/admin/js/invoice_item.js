document.addEventListener('DOMContentLoaded', function () {
    const categoryField = document.querySelector('[name$="-category"]');
    const productField = document.querySelector('[name$="-product"]');

    if (categoryField) {
        categoryField.addEventListener('change', function () {
            const categoryId = this.value;

            if (categoryId) {
                fetchProducts(categoryId, productField);
            } else {
                productField.innerHTML = '';
            }
        });
    }

    function fetchProducts(categoryId, productField) {
        const url = `/invoice/get_products_by_category/${categoryId}/`;

        fetch(url)
            .then(response => response.json())
            .then(data => {
                productField.innerHTML = '';
                data.products.forEach(product => {
                    const option = document.createElement('option');
                    option.value = product.id;
                    option.textContent = product.name;
                    productField.appendChild(option);
                });
            });
    }
});
