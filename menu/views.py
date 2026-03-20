from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Item, MEAL_TYPE, Cart, Order


class MenuList(generic.ListView):
    queryset = Item.objects.order_by("-date_created")
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["meals"] = MEAL_TYPE
        return context


class MenuItemDetail(generic.DetailView):
    model = Item
    template_name = "menu_item_detail.html"


# ADD TO CART
@login_required
def add_to_cart(request, pk):
    item = get_object_or_404(Item, id=pk)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        item=item
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('home')


# CART VIEW
@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)

    total = sum(i.item.price * i.quantity for i in cart_items)

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })


# REMOVE ITEM
@login_required
def remove_from_cart(request, pk):
    cart_item = get_object_or_404(Cart, id=pk)
    cart_item.delete()
    return redirect('cart')


# PLACE ORDER
@login_required
def place_order(request):
    cart_items = Cart.objects.filter(user=request.user)

    total = sum(i.item.price * i.quantity for i in cart_items)

    order = Order.objects.create(
        user=request.user,
        total_price=total
    )

    for item in cart_items:
        order.items.add(item.item)

    cart_items.delete()

    return redirect('home')