from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from basketapp.models import Basket
from mainapp.models import Product, ProductCategory
from mainapp.services import get_hot_product, get_same_products, get_basket


def main(request):
    title = 'Главная'
    products = Product.objects.all()[:4]

    content = {
        'title': title,
        'products': products,
        'basket': get_basket(request.user),
    }
    return render(request, 'mainapp/index.html', content)


def products(request, pk=None):
    title = 'продукты'
    links_menu = ProductCategory.objects.all()
    basket = []

    if pk is not None:
        if pk == 0:
            products = Product.objects.all().order_by('price')
            category = {'name': 'Все'}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk).order_by('price')

        # БЛОК ПАГИНАЦИИ ==>
        page = request.GET.get('page')  # получаем станицу
        paginanion = Paginator(products, 2)  # Складываем список продуктов и лиминт 2 объекта от => page
        try:
            pagineted_products = paginanion.page(page)  # итоговой объект для страницы квери сет со страницами
        except PageNotAnInteger:
            pagineted_products = paginanion.page(1)
        except EmptyPage:
            pagineted_products = paginanion.page(paginanion.num_pages)  # Количество страниц всего

        content = {
            'title': 'Категория продуктов',
            'links_menu': links_menu,
            'products': pagineted_products,
            'category': category
        }
        return render(request, 'mainapp/products_list.html', content)

    # same_products = Product.objects.all()[:6]
    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)

    content = {
        'title': title,
        'links_menu': links_menu,
        'same_products': same_products,
        'basket': get_basket(request.user),
        'hot_product': hot_product,

    }
    return render(request, 'mainapp/products.html', content)


def product(request, pk):
    title = 'продукты'
    content = {
        'title': title,
        'links_menu': ProductCategory.objects.all(),
        'product': get_object_or_404(Product, pk=pk),
        'basket': get_basket(request.user)
    }
    return render(request, 'mainapp/product.html', content)


def contact(request):
    return render(request, 'mainapp/contact.html')
