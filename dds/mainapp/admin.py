from django.contrib import admin
from .models import * 

# Register your models here.

admin.site.register(Record)
admin.site.register(Type)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Status)
