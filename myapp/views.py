# Import necessary classes
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Publisher, Book, Member, Order
from .forms import FeedbackForm, SearchForm

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

def getFeedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.cleaned_data['feedback']
            if feedback == 'B':
                choice = ' to borrow books.'
            elif feedback == 'P':
                choice = ' to purchase books.'
            else: 
                choice = ' None.'
            return render(request, 'myapp/fb_results.html', {'choice':choice})
        else:
            return HttpResponse('Invalid data')
    else:
        form = FeedbackForm()
        return render(request, 'myapp/feedback.html', {'form':form})


def findbooks(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            category = form.cleaned_data['category']
            max_price = form.cleaned_data['max_price']
            
            if category:
                booklist = Book.objects.filter(price__lte=max_price, category=category)
            else:
                booklist = Book.objects.filter(price__lte=max_price)
                
            return render(request, 'myapp/results.html', {'name': name, 'category': category, 'booklist': booklist})
        else:
            return HttpResponse('Invalid data')
    else:
        form = SearchForm()
        return render(request, 'myapp/findbooks.html', {'form': form})

