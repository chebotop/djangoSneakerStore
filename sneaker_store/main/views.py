from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.http import HttpResponseBadRequest
from django.contrib import messages
from django.db.models import Q
import datetime
from main.models import *
import logging


logger = logging.getLogger(__name__)


def base_head(request):
    brands = ShoeBrand.objects.all()
    context = {
        'brands': brands,
    }
    return render(request, 'base_head.html', context)


def index(request):
    if 'cart_id' not in request.session:
        cart = Cart.objects.create(total=0)
        request.session['cart_id'] = cart.id
    recent_shoes = ShoeModel.objects.all().order_by('-created_at')[0:6]
    context = {
        'recent_shoes': recent_shoes,
        # 'air_jordans': ShoeBrand.objects.get(name="Air Jordan").models.all(),
        # 'nikes': ShoeBrand.objects.get(name="Nike").models.all(),
        # 'adidases': ShoeBrand.objects.get(name="Adidas").models.all(),
    }
    return render(request, 'home.html', context)


def search_view(request):
    query = request.GET.get('query')
    shoe_search = ShoeModel.objects.filter(
        Q(name__icontains=query) |
        Q(brand__name__icontains=query)
        ).order_by('name')
    context = {
    'shoe_search': shoe_search,
    }
    def catalog_page(request, brand_filter="all", category_filter="all"):
    if 'cart' not in request.session:
        cart = Cart.objects.create(total=0)
        request.session['cart'] = cart.id
    all_models = ShoeModel.objects.all()
    if request.method == 'GET' and request.GET.get('min'):
        min_price = request.GET['min']
    else:
        min_price = min([model.price for model in all_models])
    if request.method == 'GET' and request.GET.get('max'):
        max_price = request.GET['max']
    else:
        max_price = max([model.price for model in all_models])
    display_models = all_models.filter(price__gte=min_price, price__lte=max_price)
    if brand_filter != 'all':
        display_models = display_models.filter(brand__name=brand_filter)
    shoebrands = ShoeBrand.objects.all()
    title = "Обзор"
    if brand_filter != 'all' and category_filter == 'all':
        title += f" {brand_filter}"
    elif category_filter != 'all':
        title = f"Обзор {brand_filter} {category_filter}"
    context = {
        'selected_title': title,
        'shoes': display_models,
        'brand': brand_filter,
        'all_brands_names': sorted(set([model.brand.name for model in all_models])),
        'all_models_names': sorted(set([model.name for model in all_models])),
        'all_brands': [brand for brand in shoebrands],
        'all_models': [model for model in all_models],

        # 'category': category,
        'air_jordans': ShoeBrand.objects.get(name="Air Jordan").models.all(),
        'nikes': ShoeBrand.objects.get(name="Nike").models.all(),
        'adidases': ShoeBrand.objects.get(name="Adidas").models.all(),
        'max_price': max_price,
        'min_price': min_price,
    }
    return render(request, 'catalog.html', context)


# Add a shoe form page.
def add_shoe_page(request):
    # Kicks out user to /admin if they are not logged in as admin
    if 'admin' not in request.session:
        return redirect('/admin')
    
    context = {
        'form': ShoeModelForm()
    }
    return render(request,"add_shoe_page.html", context)

# Inventory Management Page.
def shoe_list(request):
    if 'admin' not in request.session:
        return redirect('/admin')

    shoes = ShoeModel.objects.all()

    context = {
        'shoes': shoes,
        'models': ShoeModel.objects.all(),
    }

    return render(request, 'shoe_list.html', context)


# Catalog page for individual Model-Color

def shoe_page(request, shoe_id):
    if 'cart' not in request.session:
        cart = Cart.objects.create(total=0)
        request.session['cart'] = cart.id

    shoe = get_object_or_404(ShoeModel, id=shoe_id)
    current_brand_id = shoe.brand.id
    related_shoes = ShoeModel.objects.filter(brand_id=current_brand_id).exclude(id=shoe.id)[:6]
    shoe_images = shoe.shoe_gallery.all()
    sizes = shoe.sizes.all()

    if request.method == 'POST':
        selected_size = request.POST.get('selected_size')
        if not selected_size:
            return HttpResponseBadRequest("Selected size not found")

        cart_id = request.session.get('cart_id')
        if not cart_id:
            return HttpResponseBadRequest("No cart found")

        cart = Cart.objects.get(id=cart_id)
        CartItem.objects.create(shoe=shoe, cart=cart, size=selected_size) # Ранее создавал обьект корзины без передачи size
        refresh_cart_total(cart)
        # Добавить кнопку "перейти в корзину", после добавления товара в корзину"

    context = {
        'shoe': shoe,
        'sizes': sizes,
        'shoe_images': shoe_images,
        'related_shoes': related_shoes,
        'air_jordans': ShoeBrand.objects.get(name="Air Jordan").models.all(),
        'nikes': ShoeBrand.objects.get(name="Nike").models.all(),
        'adidases': ShoeBrand.objects.get(name="Adidas").models.all(),
    }

    return render(request, 'shoe_page.html', context)


def refresh_cart_total(cart):
    total = 0
    for item in cart.cart_items.all():
        total+= item.shoe.price
    cart.total = total
    cart.save()


# Show cart to user.
def cart(request):
    if 'cart_id' not in request.session:
        cart = Cart.objects.create(total=0)
        request.session['cart_id']=cart.id

    cart = Cart.objects.get(id=request.session['cart_id'])
    cart_items = cart.cart_items.all()

    context = {
        'cart': Cart.objects.get(id=request.session['cart_id']),
        'cart_items': cart_items,
        'air_jordans': ShoeBrand.objects.get(name="Air Jordan").models.all(),
        'nikes': ShoeBrand.objects.get(name="Nike").models.all(),
        'adidases': ShoeBrand.objects.get(name="Adidas").models.all(),
    }

    return render(request, 'cart.html', context)


def remove_from_cart(request, item_id):
    if request.method == 'POST':
        try:
            item = CartItem.objects.get(id=item_id, cart__id=request.session.get('cart_id'))
            item.delete()
            cart = Cart.objects.get(id=request.session['cart_id'])
            refresh_cart_total(cart)
        except CartItem.DoesNotExist:
            pass
        return redirect('cart')


# Update the quantity in the cart.
def update_quantity(request):
    item = CartItem.objects.get(id=request.POST['item_id'])
    item.quantity = request.POST['new_quantity']
    print(item)
    #Updates quantity or deletes the CartItem if quantity has been updated to 0.
    if int(request.POST['new_quantity'])>0:
        item.save()
    else:
        item.delete()
    cart = Cart.objects.get(id=request.session['cart_id'])

    refresh_cart_total(cart)

    return redirect('/cart')


# Checkout page. Goes to form to input checkout information.
def checkout(request):
    if 'cart_id' not in request.session:
        return redirect("/")

    cart = Cart.objects.get(id=request.session['cart_id'])

    # Returns user to home is cart is empty.
    if not cart.cart_items.exists():
        return redirect("/")

    context = {
        'cart': Cart.objects.get(id=request.session['cart_id']),
    }

    return render(request,'checkout_guest.html',context)


# Checkout processing function.
def checkout_process_guest(request):
    # Creates shipping address.
    shipping_address = Address.objects.create(
        address = request.POST['address'],
        address2 = request.POST['address2'],
        city = request.POST['city'],
        state = request.POST['state'],
        zipcode = request.POST['zipcode'],
    )
    # Checks to see if Billing Address was marked same as Shipping Address.
    if 'same_address' in request.POST:
        billing_address = shipping_address
        # Uses shipping first and last name for credit card later.
        cc_first_name = request.POST['first_name']
        cc_last_name = request.POST['last_name']
    else:
        # Creates new address and saves the billing first name and last name for credit card.
        billing_address = Address.objects.create(
            address = request.POST['cc_address'],
            address2 = request.POST['cc_address2'],
            city = request.POST['cc_city'],
            state = request.POST['cc_state'],
            zipcode = request.POST['cc_zipcode'],
        )
        cc_first_name = request.POST['cc_first_name']
        cc_last_name = request.POST['cc_last_name']

    # Creates guest user. Assigns Shipping Address to user.
    guest_user = User.objects.create(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        email = request.POST['email'],
        password = "",
        address = shipping_address)
    # Retrieves the cart from the session cart_id. Creates an Order object with it, the User, and Credit Card
    cart = Cart.objects.get(id=request.session['cart_id'])
    new_order = Order.objects.create(
        status = "Processing",
        cart = cart,
        user = guest_user,
        # credit_card = credit_card,
    )

    # Removes the purchased items from the store inventory.
    for item in cart.cart_items.all():
        shoe = item.shoe
        shoe.inventory = shoe.inventory-item.quantity
        shoe.quantity_sold = shoe.quantity_sold+item.quantity
        shoe.save()
#     # Places order_id in session to retrieve for confirmation page.
    request.session['order_id'] = new_order.id

    # Removes cart from session. The next visit to the store page will create a new cart.
    request.session.pop("cart_id")

    return redirect('/confirmation')


# Order confirmation page.
def confirmation(request):
    # Retrieves order from session.
    current_order = Order.objects.get(id = request.session['order_id'])

    # Formats credit card number to just show last digits.
    # This may be a security vulnerability. Not sure.
    cc_last_digits = current_order.credit_card.number % 10000

    # Because credit card expiration date is stored as a date with the first of the month,
    # this reformats it as a MM/YY
    cc_expiration_date = current_order.credit_card.expiration_date.strftime('%m/%y')

    context = {
        'order': current_order,
        'cc_last_digits': cc_last_digits,
        'cc_expiration_date': cc_expiration_date
    }

    return render(request, 'confirmation.html', context)

# Admin page for viewing all orders.
# def orders_page(request):
#     if 'admin' not in request.session:
#         return render(request, "admin_login.html")
#
#     context = {
#         'orders': Order.objects.all().order_by('-created_at')
#     }
#
#     return render(request, 'orders_page.html', context)

# def update_status(request):
#     order = Order.objects.get(id=request.POST['order_id'])
#     order.status = request.POST['status']
#     order.save()
#
#     return redirect('/admin/orders')

# def order_details(request, order_id):
#     if 'admin' not in request.session:
#         return redirect('/admin')
#     order = Order.objects.get(id=order_id)
#     # Because credit card expiration date is stored as a date with the first of the month,
#     # this reformats it as a MM/YY
#     cc_expiration_date = order.credit_card.expiration_date.strftime('%m/%y')
#     context = {
#         'order': order,
#         'cc_expiration_date': cc_expiration_date
#     }
#     return render(request,"order_details.html", context)

