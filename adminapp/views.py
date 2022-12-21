from pyexpat import model

from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView

from authapp.forms import ShopUserRegisterForm
from adminapp.forms import ShopUserAdminEditForm, ProductCategoryEditForm, ProductEditForm
from authapp.models import ShopUser
from django.shortcuts import get_object_or_404, render
from mainapp.models import Product, ProductCategory
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse, reverse_lazy

from django.views.generic.list import ListView
from django.utils.decorators import method_decorator


# @user_passes_test(lambda u: u.is_superuser) # ==>> Заменен на класс
# def users(request):
#     title = 'админка/пользователи'
#     users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')
#
#     content = {
#         'title': title,
#         'objects': users_list,
#     }
#     return render(request, 'adminapp/users.html', content)

class AccessMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class UsersListView(AccessMixin, ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'
    paginate_by = 2     # <== это для пагинации

    extra_context = {
        'title': 'админка/пользователи'
    }
# Первый Метод проверки ауинтификации
    # @method_decorator(user_passes_test(lambda u: u.is_superuser))
    # def dispatch(self, *args, **kwargs):
    #     return super().dispatch(*args, **kwargs)

# Второй Метод Комплекс проверки ауинтификации это ==>>
# 1)  Создали доп класс AccessMixin на базе ( UserPassesTestMixin )
    #   и переопределение метода test_func
# 2)  Дальше можно использовать свой минксин для проверки ауинтификации

# def user_create(request):
#     title = 'пользователи/создание'
#
#     if request.method == 'POST':
#         user_form = ShopUserRegisterForm(request.POST, request.FILES)
#
#         if user_form.is_valid():
#             user_form.save()
#             return HttpResponseRedirect(reverse('admin:users'))
#     else:
#         user_form = ShopUserRegisterForm()
#
#     content = {
#         'title': title,
#         'update_form': user_form
#     }
#     return render(request, 'adminapp/user_update.html', content)


class UserCreateView(AccessMixin, CreateView):  # <== ВАРИАНТ 1 < == CBV
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin:users')
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'пользователи/создание'
        return context

# def user_update(request, pk):
#     title = 'пользователи/редактирование'
#     edit_user = get_object_or_404(ShopUser, pk=pk)
#     if request.method == 'POST':
#         edit_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=edit_user)
#         if edit_form.is_valid():
#             edit_form.save()
#             return HttpResponseRedirect(reverse('admin:user_update', args=[edit_user.pk]))
#
#     else:
#         edit_form = ShopUserAdminEditForm(instance=edit_user)
#
#     content = {
#         'title': title,
#         'update_form': edit_form
#     }
#     return render(request, 'adminapp/user_update.html', content)

class UserUpdateView(AccessMixin, UpdateView):  # <== ВАРИАНТ 2 < == CBV
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin:users')
    form_class = ShopUserAdminEditForm
    extra_context = {
        'title': 'пользователи/редактирование'
    }



def user_delete(request, pk):
    title = 'пользователи/удаление'
    user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':  # user.delete()
        # вместо удаления лучше сделаем неактивным
        user.is_active = False
        user.save()
        return HttpResponseRedirect(reverse('admin:users'))

    content = {
        'title': title,
        'user_to_delete': user
    }
    return render(request, 'adminapp/user_delete.html', content)


def categories(request):
    title = 'админка/категории'
    categories_list = ProductCategory.objects.all()

    content = {
        'title': title,
        'objects': categories_list,
    }
    return render(request, 'adminapp/categories.html', content)


def category_create(request):
    title = 'категории/создание'

    if request.method == 'POST':
        edit_form_category = ProductCategoryEditForm(request.POST, request.FILES)

        if edit_form_category.is_valid():
            edit_form_category.save()
            return HttpResponseRedirect(reverse('admin:categories'))
    else:
        edit_form_category = ProductCategoryEditForm()

    content = {
        'title': title,
        'update_category_form': edit_form_category
    }
    return render(request, 'adminapp/category_update.html', content)


def category_update(request, pk):
    title = 'категории/редактирование'
    edit_category = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        edit_form_category = ProductCategoryEditForm(request.POST, instance=edit_category)
        if edit_form_category.is_valid():
            edit_form_category.save()
            # return HttpResponseRedirect(reverse('admin:categories', args=[edit_category.pk]))
            return HttpResponseRedirect(reverse('admin:categories'))
    else:
        edit_form_category = ProductCategoryEditForm(instance=edit_category)
    content = {
        'title': title,
        'update_category_form': edit_form_category
    }
    return render(request, 'adminapp/category_update.html', content)

#
# def category_delete(request, pk):
#     title = 'категория/удаление'
#     category = get_object_or_404(ProductCategory, pk=pk)
#     if request.method == 'POST':
#         category.is_active = False
#         category.save()
#         return HttpResponseRedirect(reverse('admin:categories'))
#     content = {
#         'title': title,
#         'category_delete': category
#     }
#     return render(request, 'adminapp/category_delete.html', content)

class ProductCategoryDeleteView(AccessMixin, DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('admin:categories')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())




def products(request, pk):
    title = 'админка/продукт'
    category = get_object_or_404(ProductCategory, pk=pk)
    products_list = Product.objects.filter(category__pk=pk).order_by('name')

    content = {
        'title': title,
        'category': category,
        'objects': products_list
    }
    return render(request, 'adminapp/products.html', content)


def product_create(request, pk):
    title = 'продукт/создание'
    category = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        product_form = ProductEditForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            return HttpResponseRedirect(reverse('admin:products', args=[pk]))
    else:
        product_form = ProductEditForm(initial={'category': category})

    content = {
        'title': title,
        'update_form': product_form,
        'category': category
    }
    return render(request, 'adminapp/product_update.html', content)


# def product_create(request, pk): # <<---== Обратить внимание и изучить метод для !!!! <<---==
#     title = 'продукт/создание'
#     category = get_object_or_404(ProductCategory, pk=pk)
#     if request.method == 'POST':
#         product_form = ProductEditForm(request.POST, request.FILES)
#         if product_form.is_valid():
#             product_form.save()
#             return HttpResponseRedirect(reverse('admin:products', args=[pk]))
#     else:
#         product_form = ProductEditForm(initial={'category': category})
#
#     content = {
#         'title': title,
#         'update_form': product_form,
#         'category': category
#     }
#     return render(request, 'adminapp/product_update.html', content)



# def product_read(request, pk):
#     title = 'продукт/подробнее'
#     product = get_object_or_404(Product, pk=pk)
#     content = {
#         'title': title,
#         'object': product
#     }
#     return render(request, 'adminapp/product_read.html', content)


class ProductDetailView(AccessMixin, DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'




def product_update(request, pk):
    title = 'продукт/редактирование'
    edit_product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        edit_form = ProductEditForm(request.POST, request.FILES, instance=edit_product)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin:product_update', args=[edit_product.pk]))
    else:
        edit_form = ProductEditForm(instance=edit_product)
    content = {
        'title': title,
        'update_form': edit_form,
        'category': edit_product.category.pk
    }
    return render(request, 'adminapp/product_update.html', content)


def product_delete(request, pk):
    title = 'продукт/удаление'
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.is_active = False
        product.save()
        return HttpResponseRedirect(reverse('admin:products', args=[product.category.pk]))
    content = {
        'title': title,
        'product_to_delete': product
    }
    return render(request, 'adminapp/product_delete.html', content)
