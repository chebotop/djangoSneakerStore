from .models import ShoeBrand


def add_brandmodel_to_context(request):
    return {
        'brands': ShoeBrand.objects.all()
    }
