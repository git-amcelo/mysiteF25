# Import necessary classes
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Publisher, Book, Member, Order

# Create your views here.


def index(request):
    """Main landing page - shows list of books and publishers"""
    response = HttpResponse()

    # Display list of books ordered by primary key
    heading1 = '<p>' + 'List of available books: ' + '</p>'
    response.write(heading1)
    booklist = Book.objects.all().order_by('id')[:10]
    for book in booklist:
        para = '<p>' + str(book.id) + ': ' + str(book) + '</p>'
        response.write(para)

    # Display list of Publishers sorted by city (descending)
    heading2 = '<p>' + 'List of Publishers: ' + '</p>'
    response.write(heading2)
    publisherlist = Publisher.objects.all().order_by('-city')
    for publisher in publisherlist:
        para = '<p>' + publisher.name + ' - ' + publisher.city + '</p>'
        response.write(para)

    return response


def about(request):
    """About page for the eBook APP"""
    return HttpResponse("This is an eBook APP.")


def detail(request, book_id):
    """Detail page for a specific book"""
    book = get_object_or_404(Book, pk=book_id)

    response = HttpResponse()
    para = '<p>' + 'Title: ' + book.title.upper() + '</p>'
    response.write(para)
    para = '<p>' + 'Price: $' + str(book.price) + '</p>'
    response.write(para)
    para = '<p>' + 'Publisher: ' + str(book.publisher) + '</p>'
    response.write(para)

    return response
