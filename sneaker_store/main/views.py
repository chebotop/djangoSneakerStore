from django.shortcuts import render, get_object_or_404
from .models import Category, Product



def index(request):
    return render(request, 'main/index.html')


def sheets_bot(request):
    return render(request, 'main/sheets_bot.html')


def catalog(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request, 'main/catalog.html', {'categories': categories, 'products': products})

def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'main/product_detail.html', {'product': product})

def category(request, category_id):
    # Получение категории по ID
    current_category = get_object_or_404(Category, id=category_id)
    
    # Получение всех товаров для этой категории
    products = Product.objects.filter(category=current_category)

    context = {
        'current_category': current_category,
        'products': products
    }

    return render(request, 'main/category_detail.html', context)