from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models

from main_app.manager import LabelManager


# Create your models here.


class Creation(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)


class Label(Creation):
    name = models.CharField(
        max_length=140,
        validators=[MinLengthValidator(2)],
    )

    headquarters = models.CharField(
        max_length=150,
        default='Not specified'
    )

    market_share = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        default=0.1
    )

    objects = LabelManager()


class Artist(Creation):
    name = models.CharField(
        max_length=140,
        validators=[MinLengthValidator(2)]
    )

    nationality = models.CharField(
        max_length=3,
        validators=[MinLengthValidator(3)]
    )

    awards = models.PositiveSmallIntegerField(
        default=0
    )


class Album(Creation):

    class AlbumType(models.TextChoices):
        SINGLE = 'Single', 'Single'
        SOUNDTRACK = 'Soundtrack', 'Soundtrack'
        REMIX = 'Remix', 'Remix'
        OTHER = 'Other', 'Other'

    title = models.CharField(
        max_length=150,
        validators=[MinLengthValidator(1)]
    )

    release_date = models.DateField(
        null=True,
        blank=True,
    )

    description = models.TextField(
        null=True,
        blank=True,
    )

    type = models.CharField(
        max_length=10,
        choices=AlbumType.choices,
        default=AlbumType.OTHER,

    )

    is_hit = models.BooleanField(
        default=False,
    )

    label = models.ForeignKey(
        to=Label,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    artists = models.ManyToManyField(
        to=Artist
    )
