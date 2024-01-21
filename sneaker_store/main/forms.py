from django import forms
from .models import ShoeModel, CategoryModel


class ShoeModelForm(forms.ModelForm):
    images = forms.FileField(required=False, label='Загрузка изображений для галереи')

    class Meta:
        model = ShoeModel
        fields = '__all__'


class CategoryModelForm(forms.ModelForm):
    class Meta:
        category = CategoryModel
        field = '__all__'
