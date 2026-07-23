from django.contrib import admin
from .models import Publisher, Book, Member, Order, Review


# Customize Book admin to display fields in groups and list attributes
class BookAdmin(admin.ModelAdmin):
    fields = [('title', 'category', 'publisher'), ('num_pages', 'price', 'num_reviews')]
    list_display = ('title', 'category', 'price')


# Customize Order admin to display fields in groups and list attributes
class OrderAdmin(admin.ModelAdmin):
    fields = ['books', ('member', 'order_type', 'order_date')]
    list_display = ('id', 'member', 'order_type', 'order_date', 'total_items')


# Customize Review admin to display ratings
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'reviewer', 'rating', 'date', 'comments')
    list_filter = ('rating', 'date')
    search_fields = ('reviewer', 'book__title')


# Customize Member admin to display more list attributes
class MemberAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'status', 'city', 'last_renewal')


# Register your models here.
admin.site.register(Publisher)
admin.site.register(Book, BookAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Review, ReviewAdmin)