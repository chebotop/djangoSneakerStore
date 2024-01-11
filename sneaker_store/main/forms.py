from django import forms
from .models import ShoeModel


class ShoeModelForm(forms.ModelForm):
    images = forms.FileField(required=False, label='Загрузка изображений для галереи')

    class Meta:
        model = ShoeModel
        fields = '__all__'  