// admin/js/record_dynamic.js
console.log(2)
document.addEventListener('DOMContentLoaded', function() {
    // Находим элементы select
    const typeSelect = document.getElementById('id_type');
    const categorySelect = document.getElementById('id_category');
    const subcategorySelect = document.getElementById('id_subcategory');

    // 1. При изменении Типа грузим Категории
    typeSelect.addEventListener('change', function() {
        const typeId = this.value;
        if (!typeId) return;

        // Запрос к API админки
        fetch(`/admin/api/categories/?type_id=${typeId}`)
            .then(response => response.json())
            .then(categories => {
                // Очищаем и заполняем категории
                categorySelect.innerHTML = '';
                categories.forEach(cat => {
                    categorySelect.add(new Option(cat.title, cat.id));
                });

                // Сбрасываем подкатегории
                subcategorySelect.innerHTML = '';
            });
    });

    // 2. При изменении Категории грузим Подкатегории
    categorySelect.addEventListener('change', function() {
        const categoryId = this.value;
        if (!categoryId) return;

        fetch(`/admin/api/subcategories/?category_id=${categoryId}`)
            .then(response => response.json())
            .then(subcategories => {
                subcategorySelect.innerHTML = '';
                subcategories.forEach(sub => {
                    subcategorySelect.add(new Option(sub.title, sub.id));
                });
            });
    });
});