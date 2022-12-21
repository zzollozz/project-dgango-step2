from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from basketapp.models import Basket
from mainapp.models import Product
from django.urls import reverse
from django.template.loader import render_to_string
from django.http import JsonResponse

@login_required  # доступ к корзине только для зарегистрированных пользователей
def basket(request):
    title = 'Корзина'
    basket_items = Basket.objects.filter(user=request.user).order_by('product__category')
    content = {
        'title': title,
        'basket_items': basket_items
    }
    return render(request, 'basketapp/basket.html', content)


@login_required
def basket_add(request, pk):

    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('products:product', args=[pk]))

    product = get_object_or_404(Product, pk=pk)  # Получили продукт по id
    basket = Basket.objects.filter(user=request.user, product=product).first()  # Получили объект по user и Продукту

    if not basket:  # Проверяем, есть ли он в корзине текущего пользователя
        basket = Basket(user=request.user, product=product)
    basket.quantity += 1
    basket.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_remove(request, pk):
    basket_record = get_object_or_404(Basket, pk=pk)
    basket_record.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  # Чтобы вернуться на ту же страницу, где добавляли товар


@login_required
def basket_edit(request, pk, quantity):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        quantity = int(quantity)
        new_basket_item = Basket.objects.get(pk=int(pk))

        if quantity > 0:
            new_basket_item.quantity = quantity
            new_basket_item.save()
        else:
            new_basket_item.delete()

        basket_items = Basket.objects.filter(user=request.user).order_by('product__category')

        content = {
            'basket_items': basket_items,
        }

        result = render_to_string('basketapp/includes/inc_basket_list.html', content)

        return JsonResponse({'result': result})
