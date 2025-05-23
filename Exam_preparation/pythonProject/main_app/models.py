from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models

from main_app.manager import ProfileManager


# Create your models here.


class DateAndTime(models.Model):
    class Meta:
        abstract = True

    creation_date = models.DateTimeField(
        auto_now_add=True,
    )


class Profile(DateAndTime):
    full_name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(2)]
    )

    email = models.EmailField()

    phone_number = models.CharField(
        max_length=15,
    )

    address = models.TextField()

    is_active = models.BooleanField(default=True)

    objects = ProfileManager()


class Product(DateAndTime):
    name = models.CharField(
        max_length=100,
    )

    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )

    in_stock = models.PositiveIntegerField()

    is_available = models.BooleanField(default=True)


class Order(DateAndTime):
    profile = models.ForeignKey(
        to=Profile,
        on_delete=models.CASCADE,
    )

    products = models.ManyToManyField(
        to=Product,
    )

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )

    is_completed = models.BooleanField(default=False)
