from django.db import models
from django.urls import reverse
from django import forms

class BaseTitleModel(models.Model):
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        abstract = True 

class Category(BaseTitleModel):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class SubCategory(BaseTitleModel):
    parent = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategories'
    )

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'


class Status(BaseTitleModel):
    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'

class Type(BaseTitleModel):
    class Meta:
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'


class Record(models.Model):
    date = models.DateField()
    status = models.ForeignKey(
        Status,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='status'
    )
    type = models.ForeignKey(
        Type,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='type'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    comment = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='category'
    )
    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subcategory'
    )

    
    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'

    def __str__(self):
        return super().__str__()
    
    def get_absolute_url(self):
        return reverse('record', kwargs={'pk': self.pk})