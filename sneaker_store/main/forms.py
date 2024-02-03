from django import forms
from .models import ShoeModel, CategoryModel, ShoeBrand


class ShoeModelForm(forms.ModelForm):
    images = forms.FileField(required=False, label='Загрузка изображений для галереи')

    class Meta:
        model = ShoeModel
        fields = '__all__'


class CategoryModelForm(forms.ModelForm):
    class Meta:
        model = CategoryModel
        fields = '__all__'


class ShoeBrandForm(forms.ModelForm):
    image = forms.FileField(required=False, label='Загрузить изображение логотипа')

    class Meta:
        model = ShoeBrand
        fields = '__all__'
