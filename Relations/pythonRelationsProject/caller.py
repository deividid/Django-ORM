import os
from datetime import timedelta, date

import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Author, Book, Song, Artist, Product, Review, DrivingLicense, Driver, Owner, Registration, \
    Car


# Create queries within functions


def show_all_authors_with_their_books():
    result = ''
    authors = Author.objects.all()
    books = Book.objects.all()
    for author in authors:
        works = []

        for book in books:
            if book.author_id == author.id:
                works.append(book.title)

        if len(works) > 0:
            result += f"{author.name} has written - {', '.join(works)}!\n"

    return result[:-1]


def delete_all_authors_without_books():
    have_books = False
    authors = Author.objects.all()
    for author in authors:
        books = Book.objects.all()
        for book in books:
            if book.author_id == author.id:
                have_books = True

        if have_books == False:
            author.delete()

        else:
            have_books = False


def add_song_to_artist(artist_name, song_title):
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)

    artist.songs.add(song)


def get_songs_by_artist(artist_name):
    return Artist.objects.filter(name=artist_name).order_by('-id').songs.all()


def remove_song_from_artist(artist_name, song_title):
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)

    artist.songs.remove(song)


def calculate_average_rating_for_product_by_name(product_name: str):
    product = Product.objects.get(name=product_name)
    reviews = product.reviews.all()
    average_rating = sum([r.rating for r in reviews]) / len(reviews)
    return average_rating


def get_reviews_with_high_ratings(threshold: int):
    return Review.objects.filter(rating__gte=threshold)


def get_products_with_no_reviews():
    return Product.objects.filter(reviews__isnull=True).order_by('-name')


def delete_products_without_reviews():
    get_products_with_no_reviews().delete()


def calculate_licenses_expiration_dates():
    expiration_date = {}
    licenses = DrivingLicense.objects.all().order_by('-license_number')
    for l in licenses:
        expiration_date[l.license_number] = l.issue_date + timedelta(days=365)

    result = ''

    for key, value in expiration_date.items():
        result += f"License with number: {key} expires on {value}!\n"

    return result[:-1]


def get_drivers_with_expired_licenses(due_date):
    valid_date = due_date - timedelta(days=365)

    drivers_with_expired_licenses = Driver.objects.filter(license__issue_date__gt=valid_date)
    return drivers_with_expired_licenses


def register_car_by_owner(owner: Owner):
    registration = Registration.objects.filter(car__isnull=True).first()
    car = Car.objects.filter(registration__isnull=True).first()

    car.owner = owner

    car.save()

    registration.registration_date = date.today()
    registration.car = car
    registration.save()

    return (f"Successfully registered {car.model} to {owner.name}"
            f" with registration number {registration.registration_number}.")


