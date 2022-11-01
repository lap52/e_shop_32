import telebot
from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import models


bot = telebot.TeleBot('5526116093:AAGwn4MOPRXsTixPyna1Gp1PTOI-UqQA8eY')


def home_page(request):
    all_categories = models.Category.objects.all() # Получить все

    return render(request,
                  'index.html',
                  {'all_categories': all_categories})


# Получить все товары и вывод их на front
def get_all_products(request):
    all_products = models.Products.objects.all() # Получить все

    return render(request, 'products.html', {'all_products': all_products}) # !Передать на front


# Получить конкретный товар
def get_exact_product(request, pk):
    current_product = models.Products.objects.get(product_name=pk)

    return render(request, 'about_product.html', {'current_product': current_product}) # !Передать на front


# Получить конкретную категорию
def get_exact_categories(request, pk):
    current_category = models.Category.objects.get(id=pk) # Получаем данную категорию
    category_products = models.Products.objects.filter(product_category=current_category) # Выводим продукты

    return render(request, 'categrory_products.html', {'category_products': category_products}) # !Передать на front


# Поиск конкретного товара
def search_exact_product(request):
    if request.method == 'POST':
        get_product = request.POST.get('search_product') # Получаем с html

        try:
            models.Products.objects.get(product_name=get_product) # Поиск в базе

            return redirect(f'/product/{get_product}')

        except:
            return redirect('/')


# Добавляем в корзину
def add_product_to_user_cart(request, pk):
    if request.method == 'POST':
        checker = models.Products.objects.get(id=pk)
        if checker.product_count >= int(request.POST.get('pr_count')):
            models.UserCart.objects.create(user_id=request.user.id,
                                           user_product=checker,
                                           user_product_quantity=int(request.POST.get('pr_count'))).save()


            return redirect('/products')

        else:
            return redirect(f'/product/{checker.product_name}')


# Отображение Корзины
def get_exact_user_cart(request):
    user_cart = models.UserCart.objects.filter(user_id=request.user.id)

    return render(request, 'user_cart.html', {'user_cart': user_cart})


# Удаление из корзины продукта
def delete_exact_user_cart(request, pk):
    product_to_delete = models.Products.objects.get(id=pk)

    models.UserCart.objects.filter(user_id=request.user.id,
                                user_product=product_to_delete).delete()

    return redirect('/user_cart')


# Оформление заказа
def accept_order_from_user(request):
    user_cart = models.UserCart.objects.filter(user_id=request.user.id)
    admin_id = 128401602

    if request.method == "POST":
        main_text = 'Новый заказ\n\n'

        for i in user_cart:
            main_text += f'Товар: {i.user_product} Количество: {i.user_product_quantity}\n'

    bot.send_message(admin_id, main_text)
    user_cart.delete()
    return redirect('/')


