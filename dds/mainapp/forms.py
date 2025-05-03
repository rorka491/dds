from django import forms
from .models import *

class RecordForm(forms.ModelForm):

    class Meta:
        fields = '__all__'
        model = Record
        widgets = {
            'date': forms.DateInput(
                attrs={
                    'type': 'date',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'border border-black',
                'placeholder': field.label
            })

class BaseTitleForm(forms.ModelForm):
    class Meta:
        fields = '__all__'  

    title = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control border border-black'}), label='')


class CategoryForm(BaseTitleForm):
    class Meta(BaseTitleForm.Meta):
        model = Category
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class SubCategoryForm(BaseTitleForm):
    class Meta(BaseTitleForm.Meta):
        model = SubCategory
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'


class StatusForm(BaseTitleForm):
    class Meta(BaseTitleForm.Meta):
        model = Status
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'

class TypeForm(BaseTitleForm):
    class Meta(BaseTitleForm.Meta):
        model = Type
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'

