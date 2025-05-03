from django.shortcuts import render
from django.views.generic import TemplateView, ListView, FormView, UpdateView, DetailView
from .models import * 
from django.shortcuts import get_object_or_404, redirect
from .forms import *
from django.urls import reverse_lazy
from django.http import Http404
from datetime import datetime


class Main(ListView):
    model = Record
    template_name = 'mainapp/main.html'
    context_object_name = 'records'

    def get_queryset(self):
        queryset = Record.objects.all()
        sort = self.request.GET.get('sort', 'date')
        start = self.request.GET.get('start_date')
        end = self.request.GET.get('end_date')

        if start:
            try:
                start_date = datetime.strptime(start, "%Y-%m-%d").date()
                queryset = queryset.filter(date__gte=start_date)
            except ValueError:
                pass
        
        if end:
            try:
                end_date = datetime.strptime(end, "%Y-%m-%d").date()
                queryset = queryset.filter(date__lte=end_date)
            except ValueError:
                pass

        if sort.lstrip('-') not in ['date', 'status', 'type', 'amount', 'category', 'subcategory']:
            sort = 'id'
        return queryset.order_by(sort)
    
class RecordDetailView(UpdateView):
    model = Record
    template_name = 'mainapp/record_detail.html'  
    context_object_name = 'record'
    form_class = RecordForm 
    success_url = reverse_lazy('home') 


    
class AppendRecord(FormView):
    template_name = 'mainapp/form_add_record.html'
    form_class = RecordForm
    success_url = reverse_lazy('home') 

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

class AppendToBook(FormView):
    template_name = 'mainapp/add_to_book.html'
    
    MODEL_FORM_MAP = {
    'status': (Status, StatusForm),
    'type': (Type, TypeForm),
    'category': (Category,  CategoryForm),
    'subcategory': (SubCategory, SubCategoryForm)
    }   
    
    def get(self, request, *args, **kwargs):
        title = kwargs.get('title')

        if title not in self.MODEL_FORM_MAP:
            raise Http404("Model and form for this title not found.")

        model, form_class = self.MODEL_FORM_MAP[title]

        records = model.objects.all()
        form = form_class()

        context = {
            'form': form,
            'records': records,
            'value': title
        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        title = kwargs.get('title')

        if title not in self.MODEL_FORM_MAP:
            raise Http404("Model and form for this title not found.")

        model, form_class = self.MODEL_FORM_MAP[title]
        form = form_class(request.POST)


        if form.is_valid():
            form.save()
            return redirect(reverse('append_to_book', kwargs={'title': title}))
        
        context = {
            'form':    form,
            'records': model.objects.all(),
            'value':   title,
        }
        return render(request, self.template_name, context)  
    

    
class BooksView(TemplateView):
    template_name = 'mainapp/books.html'

    titles = (
        ('Статус', 'status'),
        ('Тип', 'type'),
        ('Категория', 'category'),
        ('Подкатегория', 'subcategory')
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['titles'] = self.titles
        return context




def delete_record(request, pk):
    record = get_object_or_404(Record, pk=pk)
    record.delete()
    return redirect('home')


        


