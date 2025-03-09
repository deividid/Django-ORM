import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import *
# Create queries within functions

house1 = House.objects.create(
    name="something",
    wins=10
)

dragon1 = Dragon.objects.create(
    name="Nemo",
    power=5.3,
    breath='Fire',
    wins=5,
    house=house1
)

quest1 = Quest.objects.create(
    code="Code",
    reward=36,
    start_time='2000-12-8 11:45:12',
    host=house1
)

