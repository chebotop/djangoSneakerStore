from admin_tools.dashboard import modules, Dashboard
from .models import ShoeBrand, CategoryModel, ShoeModel
from django.urls import reverse


class CustomTreeModule(modules.DashboardModule):
    title = 'My Tree Module'
    template = '../templates/dashboard.html'

    def init_with_context(self, context):
        brands = ShoeBrand.objects.all()
        categories = CategoryModel.objects.all()
        shoes = ShoeModel.objects.all()
        self.children = [
            {
                'brand': brand,
                'brand_url': reverse('catalog_page_filter', args=[brand, 'all']),
                'brand_edit': reverse('admin:main_shoebrand_change', args=[brand.pk]),

                'categories': [
                    {
                        'category': category,
                        'category_url': reverse('catalog_page_filter', args=[brand, category]),
                        'category_edit': reverse('admin:main_categorymodel_change', args=[category.pk]),

                        'shoes': [
                            {
                                'shoe': shoe,
                                'shoe_url': reverse('admin:main_shoemodel_change', args=[shoe.pk])
                            } for shoe in shoes if shoe.parent == category
                        ]}
                    for category in categories if category.parent == brand
                ]
            } for brand in brands
        ]


class CustomDashboard(Dashboard):
    def init_with_context(self, context):
        self.children.append(CustomTreeModule(title='My Tree'))


