import os
import django
from django.db.models import Q, Count, F

from main_app.models import Product, Profile, Order

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

# Create queries within functions


def populate_db():
    p1 = Profile(full_name='Ívan Ivanov', email='ivancho3@mail.com', phone_number='1234567', address='Lyulin 12')
    p1.save()
    p2 = Profile(full_name='Georgi Georgiev', email='gosho17@mail.com', phone_number='99999999999', address='Obelya 8')
    p2.save()
    pr1 = Product(name='Bira', description='No need', price=2.4, in_stock=1000)
    pr1.save()
    pr2 = Product(name='Caca', description='Good with beer', price=5.2, in_stock=300)
    pr2.save()
    order1 = Order(profile=p1, products=pr1, total_price=20)
    order1.save()
    order2 = Order(profile=p1, products=pr2, total_price=30)


populate_db()


def get_profiles(search_string):
    if search_string is None:
        return ''

    profiles = Profile.objects.filter(
        Q(full_name__icontains=search_string)
        |
        Q(email__icontains=search_string)
        |
        Q(phone_number__icontains=search_string)

    ).order_by('full_name')

    return '/n'.join([f'Profile: {p.full_name}, email: {p.email}, phone number: {p.phone_number}, orders: {p.order_set.count()}'
                     for p in profiles])


def get_loyal_profiles():
    profiles = Profile.objects.get_regular_customers()

    return '/n'.join(
        [f'Profile: {p.full_name}, orders: {p.count_orders}'
         for p in profiles])


def get_last_sold_products():
    last_products = Order.objects.last().products.all()
    last_products = last_products.order_by('name')

    if last_products is None:
        return ''

    return f'Last sold products: {', '.join(p.name for p in last_products)}'


def get_top_products():
    products = Product.objects.annotate(
        order_count=Count('orders'),
    ).filter(order_count__gt=0).order_by('-order_count', 'name')[:5]

    if products is None:
        return ''

    result = 'Top products:'
    for p in products:
        result += f'/n{p.name}, sold {p.order_count} times'

    return result


def apply_discount():
    orders = Order.objects.annotate(
        product_count=Count('products'),
    ).filter(is_completed=False, product_count__gt=1).update(total_price=F('total_price') * 0.9)


def complete_order():
    order = Order.objects.filter(is_completed=False).first()
    if order is None:
        return ''
    products = order.products.all()
    for p in products:
        p.in_stock -= 1
        if p.in_stock == 0:
            p.is_available = False

        p.save()
        
    return 'Order completed.'
