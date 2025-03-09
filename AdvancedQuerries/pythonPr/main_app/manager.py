from decimal import Decimal

from django.db.models import Count, Avg, Max, Min

from django.db import models


class RealEstateListingManager(models.Manager):

    def by_property_type(self, property_type):
        return self.filter(property_type=property_type)

    def in_price_range(self, min_price: Decimal, max_price: Decimal):
        return self.filter(price__gte=min_price, price__lte=max_price)

    def with_bedrooms(self, bedroom_count):
        return self.filter(bedrooms=bedroom_count)

    def popular_locations(self):
        return self.values('location').annotate(location_count=Count('location')).order_by('-location_count', 'location')[:2]


class VideoGameManager(models.Manager):
    def games_by_genre(self, genre):
        return self.filter(genre=genre)

    def recently_released_games(self, year):
        return self.filter(release_year__gte=year)

    def highest_rated_game(self):
        return self.annotate(max_rating=Max('rating')).order_by('-max_rating').first()

    def lowest_rated_game(self):
        return self.annotate(min_rating=Min('rating')).order_by('min_rating').first()

    def average_rating(self):
        avg_value = self.values('rating').aggregate(avg=Avg('rating'))['avg']
        return f"{avg_value:.1f}"
