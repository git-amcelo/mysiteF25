from django.core.management.base import BaseCommand
from django.utils import timezone
from myapp.models import Publisher, Book, Member, Order


class Command(BaseCommand):
    help = 'Import sample data for Publishers, Books, Members, and Orders'

    def handle(self, *args, **options):
        # Clear existing data
        Order.objects.all().delete()
        Book.objects.all().delete()
        Member.objects.all().delete()
        Publisher.objects.all().delete()
        self.stdout.write(self.style.WARNING('Cleared existing data'))

        # Create Publishers
        publishers_data = [
            {'name': 'Wiley', 'website': 'https://www.wiley.com/', 'city': 'Hoboken', 'country': 'USA'},
            {'name': 'Pearson', 'website': 'https://www.pearson.com/', 'city': 'London', 'country': 'UK'},
            {'name': 'Penguin Random House', 'website': 'https://www.penguinrandomhouse.com', 'city': 'New York', 'country': 'USA'},
        ]

        publishers = {}
        for pub_data in publishers_data:
            publisher = Publisher.objects.create(**pub_data)
            publishers[publisher.name] = publisher
            self.stdout.write(self.style.SUCCESS(f'Created Publisher: {publisher.name}'))

        # Create Books
        books_data = [
            {'title': 'Machine Learning For Dummies', 'category': 'S', 'num_pages': 464, 'price': 34.99, 'publisher': publishers['Wiley']},
            {'title': 'Data Science For Dummies', 'category': 'S', 'num_pages': 432, 'price': 36.99, 'publisher': publishers['Wiley']},
            {'title': 'Artificial Intelligence', 'category': 'S', 'num_pages': 1136, 'price': 197.32, 'publisher': publishers['Pearson']},
            {'title': 'Computer Networking', 'category': 'S', 'num_pages': 720, 'price': 143.99, 'publisher': publishers['Pearson']},
            {'title': 'The Night Circus', 'category': 'F', 'num_pages': 400, 'price': 41.00, 'publisher': publishers['Penguin Random House']},
            {'title': 'The Underground Railroad', 'category': 'F', 'num_pages': 320, 'price': 26.95, 'publisher': publishers['Penguin Random House']},
            {'title': 'Becoming', 'category': 'B', 'num_pages': 464, 'price': 45.00, 'publisher': publishers['Penguin Random House']},
            {'title': 'A Walk in the Woods', 'category': 'T', 'num_pages': 304, 'price': 19.00, 'publisher': publishers['Penguin Random House']},
        ]

        books = {}
        for i, book_data in enumerate(books_data, start=1):
            book = Book.objects.create(**book_data)
            books[i] = book
            self.stdout.write(self.style.SUCCESS(f'Created Book {i}: {book.title}'))

        # Create Members
        members_data = [
            {'username': 'elena', 'first_name': 'Elena', 'last_name': 'Kwon', 'email': 'elena@example.com', 'status': 2, 'address': '102 Elm Avenue', 'city': 'Vancouver', 'province': 'BC', 'last_renewal': '2024-04-30', 'auto_renew': True},
            {'username': 'marcus', 'first_name': 'Marcus', 'last_name': 'Reed', 'email': 'marcus@example.com', 'status': 3, 'address': '88 Forest Hill Dr', 'city': 'Ottawa', 'province': 'ON', 'last_renewal': '2024-03-20', 'auto_renew': True},
            {'username': 'priya', 'first_name': 'Priya', 'last_name': 'Shah', 'email': 'priya@example.com', 'status': 3, 'address': '21 Lakeview Terrace', 'city': 'Saskatoon', 'province': 'SK', 'last_renewal': '2024-02-15', 'auto_renew': False},
            {'username': 'james', 'first_name': 'James', 'last_name': 'Bennett', 'email': 'james@example.com', 'status': 1, 'address': '65 Cedar Avenue', 'city': 'Ottawa', 'province': 'ON', 'last_renewal': '2024-04-10', 'auto_renew': True},
            {'username': 'aisha', 'first_name': 'Aisha', 'last_name': 'Ncube', 'email': 'aisha@example.com', 'status': 2, 'address': '400 Heritage Blvd', 'city': 'Winnipeg', 'province': 'MB', 'last_renewal': '2024-05-12', 'auto_renew': True},
            {'username': 'leo', 'first_name': 'Leo', 'last_name': 'Kwon', 'email': 'leo@example.com', 'status': 2, 'address': '77 Riverstone Crescent', 'city': 'Ottawa', 'province': 'ON', 'last_renewal': '2024-03-05', 'auto_renew': False},
        ]

        members = {}
        passwords = {
            'elena': 'Elena@102',
            'marcus': 'Marcus!88',
            'priya': 'Priya#21',
            'james': 'James2024',
            'aisha': 'Aisha!400',
            'leo': 'Leo@River',
        }

        for member_data in members_data:
            username = member_data['username']
            password = passwords[username]
            member = Member.objects.create_user(username=username, password=password, **{k: v for k, v in member_data.items() if k != 'username'})
            members[username] = member
            self.stdout.write(self.style.SUCCESS(f'Created Member: {member.username}'))

        # Add borrowed_books to Members
        members['elena'].borrowed_books.add(books[1], books[5])
        members['marcus'].borrowed_books.add(books[3], books[5])
        members['aisha'].borrowed_books.add(books[6], books[7], books[8])
        members['james'].borrowed_books.add(books[2], books[5])
        self.stdout.write(self.style.SUCCESS('Added borrowed books to members'))

        # Create Orders
        orders_data = [
            {'member': members['elena'], 'books': [books[1], books[5]], 'order_type': 1, 'order_date': '2024-04-02'},
            {'member': members['marcus'], 'books': [books[3], books[5]], 'order_type': 1, 'order_date': '2024-03-19'},
            {'member': members['aisha'], 'books': [books[6], books[7], books[8]], 'order_type': 1, 'order_date': '2024-04-05'},
            {'member': members['james'], 'books': [books[2], books[5]], 'order_type': 1, 'order_date': '2024-03-29'},
            {'member': members['leo'], 'books': [books[5], books[8]], 'order_type': 0, 'order_date': '2024-03-01'},
            {'member': members['elena'], 'books': [books[3]], 'order_type': 0, 'order_date': '2024-04-01'},
            {'member': members['aisha'], 'books': [books[4]], 'order_type': 0, 'order_date': '2024-04-06'},
        ]

        for order_data in orders_data:
            books_list = order_data.pop('books')
            order = Order.objects.create(**order_data)
            order.books.set(books_list)
            self.stdout.write(self.style.SUCCESS(f'Created Order {order.id} for {order.member.username}'))

        self.stdout.write(self.style.SUCCESS('Data import completed successfully!'))
