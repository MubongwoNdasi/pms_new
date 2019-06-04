from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from cart.models import Cart
from drug.models import Drugs

# Create your views here.


# def cart_create(user=None):
#     cart_obj = Cart.objects.create(user=None)
#     print('New cart created')
#     return cart_obj


@login_required(login_url='accounts/login')
def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    # print(cart_obj)

    return render(request, 'cart/cart.html', {'cart': cart_obj})


@login_required(login_url='accounts/login')
def cart_update(request):
    print(request.POST)
    try:
        drug_id = request.POST.get('drug_id')
    except Drugs.DoesNotExist:
        print('drug does not exist')
        return redirect('cart:home')
    drug_obj = Drugs.objects.get(id=drug_id)
    cart_obj, new_obj = Cart.objects.new_or_get(request)

    if drug_obj in cart_obj.drugs.all():
        cart_obj.drugs.remove(drug_obj)
    else:
        cart_obj.drugs.add(drug_obj)

    return redirect('cart:home')


# @login_required(login_url='core/login')
# def cart_update(request):
#     print(request.POST)
#     try:
#         product_id = request.POST.get('product_id')
#     except Products.DoesNotExist:
#         print('product does not exist')
#         return redirect('cart:home')
#     product_obj = Products.objects.get(id=product_id)
#     cart_obj, new_obj = Cart.objects.new_or_get(request)
#
#     if product_obj in cart_obj.products.all():
#         cart_obj.products.remove(product_obj)
#     else:
#         cart_obj.products.add(product_obj)
#
#     return redirect('cart:home')

