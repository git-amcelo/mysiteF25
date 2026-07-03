# Import necessary classes
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Publisher, Book, Member, Order, Review
from .forms import FeedbackForm, SearchForm, OrderForm, ReviewForm

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
            feedbacks = form.cleaned_data['feedback']
            choice_parts = []
            if 'B' in feedbacks:
                choice_parts.append('to borrow books')
            if 'P' in feedbacks:
                choice_parts.append('to purchase books')
            
            if choice_parts:
                choice = ' ' + ' and '.join(choice_parts) + '.'
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

def place_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            books = form.cleaned_data['books']
            order = form.save(commit=False)
            member = order.member
            type = order.order_type
            order.save()
            form.save_m2m()
            if type == 1:
                for b in order.books.all():
                    member.borrowed_books.add(b)
            return render(request, 'myapp/order_response.html', {'books': books, 'order':order})
        else:
            return render(request, 'myapp/placeorder.html', {'form':form})
    else:
        form = OrderForm()
        return render(request, 'myapp/placeorder.html', {'form':form})

def review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data['rating']
            if rating >= 1 and rating <= 5:
                # new Review object is created based on the information submitted and stored in the db
                review_obj = form.save()
                # the num_reviews field of the specified book is incremented by 1 and the updated value is saved in the db.
                book = review_obj.book
                book.num_reviews += 1
                book.save()
                # the user is redirected to the main (index.html) page.
                return redirect('myapp:index')
            else:
                # Redisplay the form with the message: ‘You must enter a rating between 1 and 5!’
                return render(request, 'myapp/review.html', {
                    'form': form,
                    'error_message': 'You must enter a rating between 1 and 5!'
                })
        else:
            return render(request, 'myapp/review.html', {'form': form})
    else:
        form = ReviewForm()
        return render(request, 'myapp/review.html', {'form': form})

