document.addEventListener('change', function (event) {
    const qs = event.target.name;
    console.log("qs", qs);
    if (!qs.includes("category")) {
        console.log("qs.includes('category')", qs.includes("category"));
        return true;
    }
    const categoryField = document.querySelector(`[name$="${qs}"]`);
    const productField = document.querySelector(`[name$=${qs.replace("category", "product")}]`);
    if (categoryField) {
        const categoryId = event.target.value;
        if (categoryId) {
            fetchProducts(categoryId, productField);
        } else {
            productField.innerHTML = '';
        }
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
