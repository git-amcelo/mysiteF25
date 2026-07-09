from django.contrib import admin
from .models import Publisher, Book, Member, Order, Review


# Customize Review admin to display ratings
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'reviewer', 'rating', 'date', 'comments')
    list_filter = ('rating', 'date')
    search_fields = ('reviewer', 'book__title')


# Register your models here.
admin.site.register(Publisher)
admin.site.register(Book)
admin.site.register(Member)
admin.site.register(Order)
admin.site.register(Review, ReviewAdmin)