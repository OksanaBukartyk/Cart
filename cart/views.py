from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from django.contrib import messages
from coupons.forms import CouponApplyForm

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)

    product = get_object_or_404(Product, id=product_id)
    count=product.stock
    form = CartAddProductForm(request.POST,initial={'count':count})
    if form.is_valid():
        cd = form.cleaned_data
        if int(cd['quantity']) < count:
            cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
        else:
            messages.info(request,'На сайті не має такої наявності')
            return render(request,
                          'shop/product/detail.html',
                          {'product': product,
                           'cart_product_form': form})

    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
                            initial={'quantity': item['quantity'],
                            'update': True})
    coupon_apply_form = CouponApplyForm()

    return render(request,
                  'cart/detail.html',
                  {'cart': cart,
                   'coupon_apply_form': coupon_apply_form})