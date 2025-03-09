import os
import django



# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import CreditCard
# Create queries within functions
# Create CreditCard instances with card owner names and card numbers

