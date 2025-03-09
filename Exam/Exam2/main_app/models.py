from django.core.validators import (MinLengthValidator, MaxLengthValidator, MinValueValidator,
                                    MaxValueValidator, RegexValidator)
from django.db import models

# Create your models here.


class Modified(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(
        max_length=80,
        validators=[MinLengthValidator(5)],
        unique=True
    )
    modified_at = models.DateTimeField(auto_now=True)


class House(Modified):
    moto = models.TextField(null=True, blank=True)
    is_ruling = models.BooleanField(default=False)
    castle = models.CharField(max_length=80, null=True, blank=True)
    wins = models.SmallIntegerField(default=0)


class Dragon(Modified):
    class BreathChoices(models.TextChoices):
        FIRE = 'Fire', 'Fire'
        ICE = 'Ice', 'Ice'
        LIGHTNING = 'Lightning', 'Lightning'
        UNKNOWN = 'Unknown', 'Unknown'

    power = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(1.0), MaxValueValidator(10.0)],
        default=1.0
    )
    breath = models.CharField(
        choices=BreathChoices.choices,
        max_length=9,
        default=BreathChoices.UNKNOWN,
    )
    is_healthy = models.BooleanField(default=True)
    birth_date = models.DateField()
    wins = models.SmallIntegerField(default=0)
    house = models.ForeignKey(
        to=House,
        on_delete=models.CASCADE,
        related_name='dragons',
    )


class Quest(Modified):
    code = models.CharField(
        validators=[MinLengthValidator(4),
                    MaxLengthValidator(4),
                    RegexValidator(regex=r'^([a-zA-Z#]+)$')],
        unique=True,
    )
    reward = models.FloatField(default=100)
    start_time = models.DateTimeField()
    dragons = models.ManyToManyField(
        to=Dragon,
        related_name='quests',
    )
    host = models.ForeignKey(
        to=House,
        on_delete=models.CASCADE,
        related_name='host_quests',
    )
