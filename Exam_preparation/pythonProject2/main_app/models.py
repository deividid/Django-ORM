from datetime import date

from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models

from main_app.manager import HouseManager


def validate_code(text):
    for l in text:
        if l.isalpha() or l == '#':
            continue

        raise ValidationError('Must contain alphabet characters or hash symbol')


class Modify(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(
        max_length=80,
        unique=True,
        validators=[MinLengthValidator(5)],
    )
    modified_at = models.DateTimeField(auto_now=True)


class House(Modify):
    motto = models.TextField(
        null=True,
        blank=True,
    )

    is_ruling = models.BooleanField(default=False)

    castle = models.CharField(
        max_length=80,
        null=True,
        blank=True,
    )

    wins = models.PositiveSmallIntegerField(
        default=0,
    )

    objects = HouseManager()


class Dragon(Modify):

    class BreathChoices(models.TextChoices):
        FIRE = 'Fire', 'Fire'
        ICE = 'Ice', 'Ice'
        LIGHTNING = 'Lightning', 'Lightning'
        UNKNOWN = 'Unknown', 'Unknown'


    power = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=1.0,
        validators=[MinValueValidator(1.0), MaxValueValidator(10.0)],
    )

    breath = models.CharField(
        max_length=9,
        choices=BreathChoices.choices,
        default=BreathChoices.UNKNOWN,
    )

    is_healthy = models.BooleanField(default=True)

    birth_date = models.DateField(
        default=date.today,
    )

    wins = models.PositiveSmallIntegerField(
        default=0,
    )

    house = models.ForeignKey(
        to=House,
        on_delete=models.CASCADE,
    )


class Quest(Modify):
    code = models.CharField(
        unique=True,
        max_length=4,
        validators=[validate_code],
    )

    reward = models.FloatField(
        default=100.0,
    )

    start_time = models.DateTimeField()

    dragons = models.ManyToManyField(
        to=Dragon,

    )

    host = models.ForeignKey(
        to=House,
        on_delete=models.CASCADE,
    )
