from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# a. Publisher Model
class Publisher(models.Model):
    name = models.CharField(max_length=200)
    website = models.URLField()
    city = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=50, default='Canada')

    def __str__(self):
        return self.name


# b. Book Model
class Book(models.Model):
    CATEGORY_CHOICES = [
        ('S', 'Scinece&Tech'),
        ('F', 'Fiction'),
        ('B', 'Biography'),
        ('T', 'Travel'),
        ('O', 'Other')
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES, default='S')
    num_pages = models.PositiveIntegerField(default=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)

    publisher = models.ForeignKey(Publisher, related_name='books', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


# c. Member Model
class Member(User):
    STATUS_CHOICES = [
        (1, 'Regular member'),
        (2, 'Premium Member'),
        (3, 'Guest Member'),
    ]

    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    address = models.CharField(max_length=300, blank=True)
    city = models.CharField(max_length=20, default='Windsor')
    province = models.CharField(max_length=2, default='ON')
    last_renewal = models.DateField(default=timezone.now)
    auto_renew = models.BooleanField(default=True)
    borrowed_books = models.ManyToManyField(Book, blank=True)

    def __str__(self):
        return self.username


# d. Order Model
class Order(models.Model):
    ORDER_TYPE_CHOICES = [
        (0, 'Purchase'),
        (1, 'Borrow'),
    ]

    books = models.ManyToManyField(Book)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    order_type = models.IntegerField(choices=ORDER_TYPE_CHOICES, default=1)
    order_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Order {self.id} by {self.member.username}"

    def total_items(self):
        return self.books.count()