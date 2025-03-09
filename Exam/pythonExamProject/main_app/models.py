from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxValueValidator, MinValueValidator
from django.db import models

from main_app.managers import AstronautManager


# Create your models here.


def int_check(value):
    if not value.isdigit():
        raise ValidationError('')

    return value


class UpdatedApp(models.Model):
    class Meta:
        abstract = True

    updated_at = models.DateTimeField(auto_now=True)


class Astronaut(UpdatedApp):
    name = models.CharField(
        max_length=120,
        validators=[MinLengthValidator(2)],
    )
    phone_number = models.CharField(
        max_length=15,
        validators=[int_check],
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    date_of_birth = models.DateField(null=True, blank=True)
    spacewalks = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(100)],
    )

    objects = AstronautManager()


class Spacecraft(UpdatedApp):
    name = models.CharField(
        max_length=120,
        validators=[MinLengthValidator(2)],
    )
    manufacturer = models.CharField(max_length=100)
    capacity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    weight = models.FloatField(validators=[MinValueValidator(0.0)])
    launch_date = models.DateField()


class Mission(UpdatedApp):
    class StatusChoices(models.TextChoices):
        PLANNED = 'Planned', 'Planned'
        ONGOING = 'Ongoing', 'Ongoing'
        COMPLETED = 'Completed', 'Completed'

    name = models.CharField(
        max_length=120,
        validators=[MinLengthValidator(2)],
    )
    description = models.TextField(null=True, blank=True)
    status = models.CharField(
        choices=StatusChoices.choices,
        default=StatusChoices.PLANNED,
        max_length=9
    )
    launch_date = models.DateField()
    spacecraft = models.ForeignKey(
        to=Spacecraft,
        on_delete=models.CASCADE,
        related_name='missions_of_spacecrafts',
    )
    astronauts = models.ManyToManyField(
        to=Astronaut,
        related_name='missions',
    )
    commander = models.ForeignKey(
        to=Astronaut,
        on_delete=models.SET_NULL,
        related_name='commander',
        null=True,
        blank=True,
    )

