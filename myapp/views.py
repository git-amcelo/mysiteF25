# Import necessary classes
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Publisher, Book, Member, Order

# Create your views here.


def index(request):
    """Main landing page - shows list of books"""
    booklist = Book.objects.all().order_by('id')[:10]
    return render(request, 'myapp/index.html', {'booklist': booklist})
    # Passing context variable: booklist (list of books)


def about(request):
    """About page for the eBook APP"""
    return render(request, 'myapp/about.html')
    # Passing context variables: NO - no extra context variables needed


def detail(request, book_id):
    """Detail page for a specific book"""
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'myapp/detail.html', {'book': book})
    # Passing context variable: book (the specific book object)
