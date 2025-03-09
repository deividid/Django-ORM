import os


import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Customer, Product, DiscountedProduct
from django.core.exceptions import ValidationError
from decimal import Decimal
# Create queries within functions



