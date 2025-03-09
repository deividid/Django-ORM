import os


import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Profile, Order, Product
from django.db.models import Q, Count
from decimal import Decimal


def get_profiles(search_string=None):

    if search_string is None:
        return ""

    match_profiles = Profile.objects.filter(
        Q(full_name__icontains=search_string)
        | Q(email__icontains=search_string)
        | Q(phone_number__icontains=search_string)
    ).order_by('full_name')

    if match_profiles is None:
        return ""

    return '\n'.join([f"Profile: {p.full_name}, email: {p.email}, phone number: {p.phone_number},"
                      f" orders: {p.orders.count()}" for p in match_profiles])


def get_loyal_profiles():
    loyal_profiles = Profile.objects.get_regular_customers()

    if loyal_profiles is None:
        return ""

    return '\n'.join([f"Profile: {p.full_name}, orders: {p.orders_count}" for p in loyal_profiles])


def get_last_sold_products():
    last_order = Order.objects.last()

    if last_order is None:
        return ""

    products = [p.name for p in last_order.products.order_by('name')]

    if len(products) == 0:
        return ""

    return f"Last sold products: {', '.join(products)}"


def get_top_products():
    top_products = (Product.objects.annotate(order_count=Count('many_orders')).filter(order_count__gt=0)
                    .order_by('-order_count', 'name'))

    if top_products is None or Order.objects.all() is None:
        return ""

    if len(top_products) > 5:
        top_products = top_products[:5]

    return "Top products:\n" + '\n'.join([f"{p.name}, sold {p.order_count} times" for p in top_products])


def apply_discounts():
    not_completed_orders = (Order.objects.annotate(products_count=Count('products')).
                            filter(is_completed=False, products_count__gt=2).all())

    if not_completed_orders is None:
        return "Discount applied to 0 orders."

    count_of_discounts = 0

    for order in not_completed_orders:
        new_price = order.total_price * Decimal(0.9)
        Order.objects.filter(pk=order.pk).update(total_price=new_price)
        count_of_discounts += 1

    return f"Discount applied to {count_of_discounts} orders."



def complete_order():
    uncomplete_order = Order.objects.filter(is_completed=False).first()

    if uncomplete_order is None:
        return ""

    Order.objects.filter(pk=uncomplete_order.pk).update(is_completed=True)

    for p in uncomplete_order.products.all():
        new_stock = p.in_stock - 1
        if new_stock == 0:
            Product.objects.filter(pk=p.pk).update(is_available=False)

        Product.objects.filter(pk=p.pk).update(in_stock=new_stock)

    return "Order has been completed!"


print(get_top_products())



