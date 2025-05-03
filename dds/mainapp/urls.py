from django.contrib import admin
from django.urls import path
from .views import *
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    path('', Main.as_view(), name='home'),
    path('delete/<int:pk>/', delete_record, name='delete_record'),
    path('append_record/', AppendRecord.as_view(), name='append_record'),
    path('record/<int:pk>/', RecordDetailView.as_view(), name='record'),
    path('books/', BooksView.as_view(), name='books'),
    path('books/<str:title>/', AppendToBook.as_view(), name='append_to_book')
]
