from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib import messages
import datetime
from main.models import *


def index(request):
    # This checks if a cart already exists in session. If not, it creates a cart and saves its id to session.
    if 'cart_id' not in request.session:
        cart = Cart.objects.create(total=0)
        request.session['cart_id']=cart.id

    # Grabs the 6 most recent shoes created in the DB.
    recent_shoes = ShoeModel.objects.all().order_by('-created_at')[0:6]

    # Also grabs all the models of the three brands, for display in the top bar.
    context = {
        'recent_shoes': recent_shoes,
        'air_jordans': Brand.objects.get(name="Air Jordan").models.all(),
        'nikes': Brand.objects.get(name="Nike").models.all(),
        'adidases': Brand.objects.get(name="Adidas").models.all(),
    }
    return render(request, 'home.html', context)

# Catalog Page, works for Browse all, but also catagories and filters. Default filter is "all".
def catalog_page(request, browse_filter = "all"):
    if 'cart' not in request.session:
        cart = Cart.objects.create(total=0)
        request.session['cart']=cart.id

    # Info for the side-bar.
    all_brands = Brand.objects.all().order_by('name')
    all_models = ShoeModel.objects.all().order_by('model')

    # Checks if there are min and max price filters in the GET url, otherwise sets min and max to default values.
    if request.method == 'GET' and request.GET.get('min'):
        min_price = request.GET['min']
    else:
        min_price = 0

    if request.method == 'GET' and request.GET.get('max'):
        max_price = request.GET['max']
    else:
        max_price = 10000

    # Assigns display_shoes to either all, a brand, or a specific model in the else statement. "browse_filter" can include brand or model info. Always filters for price as well. 
    if browse_filter == "all":
        category = "All Sneakers"
        display_shoes = ShoeModel.objects.filter(price__gte=min_price, price__lte=max_price)
    elif browse_filter == "air jordan":
        category = "Air Jordan"
        display_shoes = ShoeModel.objects.filter(model__brand__name="Air Jordan", price__gte=min_price, price__lte=max_price)
    elif browse_filter == "nike":
        category = "Nike"
        display_shoes = ShoeModel.objects.filter(model__brand__name="Nike", price__gte=min_price, price__lte=max_price)
    elif browse_filter == "adidas":
        category = "Adidas"
        display_shoes = ShoeModel.objects.filter(model__brand__name="Adidas", price__gte=min_price, price__lte=max_price)
    else:
        model = ShoeModel.objects.get(id=int(browse_filter))
        category = model.model
        display_shoes = ShoeModel.objects.filter(model=model, price__gte=min_price, price__lte=max_price)

        context = {
            'shoes': display_shoes,
            'all_brands': all_brands,
            'all_models': all_models,
            'category': category,
            'air_jordans': Brand.objects.get(name="Air Jordan").models.all(),
            'nikes': Brand.objects.get(name="Nike").models.all(),
            'adidases': Brand.objects.get(name="Adidas").models.all(),
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

    }
    return render(request,"add_shoe_page.html", context)

def add_shoe(request):
    if request.method == 'POST':
        brand_name = request.POST.get('brand')
        model_name = request.POST.get('model')
        sizes = request.POST.getlist('size')

        # Check if the brand already exists or create a new one
        brand, created = Brand.objects.get_or_create(name=brand_name)

        # Check if the model already exists or create a new one
        model, created = ShoeModel.objects.get_or_create(
            model=model_name,
            brand=brand,
            defaults={
                'price': request.POST.get('price', 0),
                'desc': request.POST.get('desc', ''),
                'color': request.POST.get('color', ''),  # Assuming color is a field in your ShoeModel.
            }
        )

        sizes = Size.objects.filter(id__in=sizes)

        model.size.set(sizes)

        return redirect('/admin/shoe_list')




# Inventory Management Page.
def shoe_list(request):
    if 'admin' not in request.session:
        return redirect('/admin')

    shoes = ShoeModel.objects.all()

    context = {
        'shoes': shoes,
    }

    return render(request, 'shoe_list.html', context)

# Updates inventory of specific size.
# def update_desc(request):
#     shoe = ShoeSize.objects.get(id=request.POST['shoe_id'])
#     shoe.inventory = request.POST['new_inventory']
#     shoe.save()

#     return redirect('/admin/shoe_list')
def update_desc(request):
    shoe = ShoeModel.objects.get(id=request.POST['desc'])
    shoe.desc = request.POST['new_description']
    shoe.save()

    return redirect('/admin/shoe_list')

# Updates image upload of specific color. Applies to all sizes.
def update_img(request):
    shoe = ShoeModel.objects.get(id=request.POST['shoe_color_id'])
    shoe.image = request.FILES.get('new_image', False)
    shoe.save()

    return redirect('/admin/shoe_list')

#Updates price of specific model. Prices are constant across all colors/sizes of the same model.
def update_price(request):
    shoe = ShoeModel.objects.get(id=request.POST['shoe_id'])
    shoe.price = request.POST['new_price']
    shoe.save()

    return redirect('/admin/shoe_list')

# def filter_list(request):
#     model_id=request.POST['model_id']
#     shoes_of_model = ShoeSize.objects.filter(color__model__id = model_id)
#     context ={
#         'shoes': shoes_of_model,
#         'models': ShoeModel.objects.all(),
#         'filtered': True,
#     }

#     return render(request, 'shoe_list.html', context)

# Catalog page for individual Model-Color
def shoe_page(request, shoe_id):
    if 'cart' not in request.session:
        cart = Cart.objects.create(total=0)
        request.session['cart']=cart.id

    shoe = ShoeModel.objects.get(id=shoe_id)
    current_brand_id = shoe.brand.id
    related_shoes = ShoeModel.objects.filter(brand_id = current_brand_id).exclude(id = shoe.id)[0:6]
    sizes = Size.objects.all()

    context = {
        'sizes': sizes,
        'shoe': ShoeModel.objects.get(id=shoe_id),
        'related_shoes': related_shoes,
        'air_jordans': Brand.objects.get(name="Air Jordan").models.all(),
        'nikes': Brand.objects.get(name="Nike").models.all(),
        'adidases': Brand.objects.get(name="Adidas").models.all(),
    }

    return render(request, 'shoe_page.html', context)

# Function used within views.py for refreshing the total of a cart when things are added or removed.
def refresh_cart_total(cart):
    total = 0
    for item in cart.cart_items.all():
        total+= item.quantity * item.shoe.color.model.price
    cart.total = total
    cart.save()

# Add shoe size instance to cart.
def add_to_cart(request):
    shoe = ShoeModel.objects.get(id=request.POST['size_id'])
    cart = Cart.objects.get(id=request.session['cart_id'])
    cart_item = CartItem.objects.create(shoe=shoe, quantity=1, cart=cart)

    refresh_cart_total(cart)

    return redirect('/cart')

# Show cart to user.
def cart(request):
    if 'cart_id' not in request.session:
        cart = Cart.objects.create(total=0)
        request.session['cart_id']=cart.id
    context = {
        'cart': Cart.objects.get(id=request.session['cart_id']),
        'air_jordans': Brand.objects.get(name="Air Jordan").models.all(),
        'nikes': Brand.objects.get(name="Nike").models.all(),
        'adidases': Brand.objects.get(name="Adidas").models.all(),
    }

    return render(request, 'cart.html', context)

# Update the quantity in the cart.
def update_quantity(request):
    item = CartItem.objects.get(id=request.POST['item_id'])

    # Checks to make sure the new updated quantity is in stock.
    if item.shoe.inventory<int(request.POST['new_quantity']):
        messages.error(request, "Sorry, that quantity is not currently in stock.")
        return redirect('/cart')
    item.quantity = request.POST['new_quantity']

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
        address = shipping_address
    )
    # Credit Card expiration date set as a datetime, where it's the first of the month of the MM/YYYY provided
    expiration_date = datetime.date(int(request.POST['expireYYYY']),int(request.POST['expireM']),1)
    # Creates the credit card.
    credit_card = CreditCard.objects.create(
        number = request.POST['cc_number'],
        security_code = request.POST['cc_security_code'],
        expiration_date = expiration_date,
        first_name = cc_first_name,
        last_name = cc_last_name,
        address = billing_address,
        user = guest_user,
    )
    # Retrieves the cart from the session cart_id. Creates an Order object with it, the User, and Credit Card
    cart = Cart.objects.get(id=request.session['cart_id'])
    new_order = Order.objects.create(
        status = "Processing",
        cart = cart,
        user = guest_user,
        credit_card = credit_card,
    )

    # Removes the purchased items from the store inventory.
    for item in cart.cart_items.all():
        shoe = item.shoe
        shoe.inventory = shoe.inventory-item.quantity
        shoe.quantity_sold = shoe.quantity_sold+item.quantity
        shoe.save()

    # Places order_id in session to retrieve for confirmation page.
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
def orders_page(request):
    if 'admin' not in request.session:
        return render(request, "admin_login.html")

    context = {
        'orders': Order.objects.all().order_by('-created_at')
    }

    return render(request, 'orders_page.html', context)

# Update the status of the order between "Processing", "Shipped", or "Canceled"
def update_status(request):
    order = Order.objects.get(id=request.POST['order_id'])
    order.status = request.POST['status']
    order.save()

    return redirect('/admin/orders')

# Order details page. This is an order summary that can be used by the store to fullfill orders.
def order_details(request, order_id):
    if 'admin' not in request.session:
        return redirect('/admin')
    order = Order.objects.get(id=order_id)
    # Because credit card expiration date is stored as a date with the first of the month,
    # this reformats it as a MM/YY
    cc_expiration_date = order.credit_card.expiration_date.strftime('%m/%y')
    context = {
        'order': order,
        'cc_expiration_date': cc_expiration_date
    }
    return render(request,"order_details.html", context)

# Basic navigation menu for admin pages.
def admin_menu(request):
    # If admin hasn't been logged in, redirect to login page.
    if 'admin' not in request.session:
        return render(request, "admin_login.html")
    
    return render(request, "admin_menu.html")

# Logs in admin. Checks to see if password is "admin". This probably isn't secure.
def admin_login(request):
    if request.POST['password']=="admin":
        request.session['admin']=True
        return redirect('/admin')
    messages.error(request, "Incorrect Password")
    return redirect('/admin')

# Remove admin from session on logout.
def admin_logout(request):
    request.session.pop("admin")

    return redirect('/admin')