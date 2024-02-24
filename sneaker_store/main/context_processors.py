from .models import ShoeBrand, ShoeModel
from django.db.models import Q


def add_brandmodel_to_context(request):
    query = request.GET.get('query', '')
    shoe_search = []
    if query:  # Проверяем, есть ли параметр запроса
        shoe_search = ShoeModel.objects.filter(
            Q(name__icontains=query) |
            Q(brand__name__icontains=query)
        ).order_by('name')

    return {
        'brands': ShoeBrand.objects.all(),
        'shoe_search': shoe_search,
        'search_query': query,  # Добавляем сам запрос в контекст, чтобы его можно было использовать в шаблоне
    }
