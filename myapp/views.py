# Import necessary classes
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Publisher, Book, Member, Order, Review
from .forms import FeedbackForm, SearchForm, OrderForm, ReviewForm
import random
from django.utils import timezone

# Create your views here.


def index(request):
    """Main landing page - shows list of books"""
    booklist = Book.objects.all().order_by('id')[:10]
    # Check if last_login exists in session
    last_login = request.session.get('last_login', 'Your last login was more than one hour ago')
    return render(request, 'myapp/index.html', {'booklist': booklist, 'last_login': last_login})
    # Passing context variable: booklist (list of books), last_login (session value)


def about(request):
    """About page for the eBook APP"""
    # Check for 'lucky_num' cookie
    lucky_num = request.COOKIES.get('lucky_num')
    if lucky_num:
        mynum = int(lucky_num)
    else:
        # Generate random number between 1 and 100
        mynum = random.randint(1, 100)
    response = render(request, 'myapp/about.html', {'mynum': mynum})
    # Set cookie to expire after 5 minutes (300 seconds)
    response.set_cookie('lucky_num', mynum, max_age=300)
    return response
    # Passing context variables: mynum (lucky number from cookie or randomly generated)


def user_login(request):
    """Handle user login"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                # Generate current date and time for session
                last_login = timezone.now()
                request.session['last_login'] = last_login.strftime('%Y-%m-%d %H:%M:%S')
                # Set session expiry to 1 hour
                request.session.set_expiry(10)
                # Check for 'next' parameter to redirect after login
                next_url = request.POST.get('next', '')
                if next_url:
                    return HttpResponseRedirect(next_url)
                return HttpResponseRedirect(reverse('myapp:index'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        next_url = request.GET.get('next', '')
        return render(request, 'myapp/login.html', {'next': next_url})


@login_required
def user_logout(request):
    """Handle user logout"""
    logout(request)
    return HttpResponseRedirect(reverse('myapp:index'))


@login_required
def chk_reviews(request, book_id):
    """Check reviews for a specific book - only for members"""
    book = get_object_or_404(Book, pk=book_id)

    # Check if user is a Member
    if Member.objects.filter(username=request.user.username).exists():
        # User is a Member - get average rating
        reviews = Review.objects.filter(book=book)
        if reviews.exists():
            total_rating = sum(review.rating for review in reviews)
            average_rating = total_rating / reviews.count()
            return render(request, 'myapp/chk_reviews.html', {
                'book': book,
                'average_rating': average_rating,
                'has_reviews': True
            })
        else:
            return render(request, 'myapp/chk_reviews.html', {
                'book': book,
                'has_reviews': False
            })
    else:
        # User is not a Member
        return render(request, 'myapp/chk_reviews.html', {
            'is_member': False
        })


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
                reviewer = form.cleaned_data['reviewer']
                comments = form.cleaned_data.get('comments', '')
                books = form.cleaned_data['book']
                # Create a review for each selected book
                for book in books:
                    review_obj = Review.objects.create(
                        reviewer=reviewer,
                        book=book,
                        rating=rating,
                        comments=comments
                    )
                    # the num_reviews field of the specified book is incremented by 1 and the updated value is saved in the db.
                    book.num_reviews += 1
                    book.save()
                # the user is redirected to the main (index.html) page.
                return redirect('myapp:index')
            else:
                # Redisplay the form with the message: 'You must enter a rating between 1 and 5!'
                return render(request, 'myapp/review.html', {
                    'form': form,
                    'error_message': 'You must enter a rating between 1 and 5!'
                })
        else:
            return render(request, 'myapp/review.html', {'form': form})
    else:
        form = ReviewForm()
        return render(request, 'myapp/review.html', {'form': form})


