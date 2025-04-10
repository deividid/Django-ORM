import os
import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
import math
from main_app.models import Label, Artist, Album
from main_app.helping import populate_model_with_data
from django.db.models import Count, F


# Create queries within functions


def populate_db():
    populate_model_with_data(Label, 2)
    a1 = Artist(name='Snop Dog', nationality='USA', awards=3)
    a2 = Artist(name='Azis', nationality='BUL')
    a1.save()
    a2.save()
    populate_model_with_data(Album, 2)


def get_labels(string=None):
    if string is None:
        return 'No search.'

    labels = Label.objects.filter(name__icontains=string).order_by('-market_share', 'name')

    if not labels.exists():
        return "No labels match this search."

    return '\n'.join(f"Label: {l.name}, headquarters: {l.headquarters}, "
                     f"market share: {math.floor(l.market_share)}%"for l in labels)


def get_best_label():
    top_label = Label.objects.get_labels_by_albums_count().first()
    if top_label is None:
        return "No data."

    return f"The best label is {top_label.name} with {top_label.album_count} albums."


def get_artists_by_albums_count():
    artists = Artist.objects.annotate(
        album_count=Count('album')
    ).order_by('-album_count', 'name')[:3]

    if not artists.exists():
        return 'No data.'

    return '\n'.join(f"{a.name}: {a.album_count} album/s." for a in artists)


def get_most_productive_artist():
    top_artist = Artist.objects.annotate(
        album_count=Count('album')
    ).order_by('-album_count', 'name').first()
    if top_artist is None:
        return "No data."

    albums = Album.objects.filter(artists__name=top_artist.name).order_by('title')

    if not albums.exists():
        return 'No data.'

    return (f"The most productive artist is {top_artist.name} "
            f"with album titles: {', '.join(a.title for a in albums)}.")


def get_latest_hit_album():
    album = Album.objects.filter(is_hit=True).order_by('-release_date', 'title').first()
    if album is None:
        return 'No data.'

    artists = Artist.objects.filter(album__id=album.id).order_by('name')

    if not artists.exists():
        result = 'TBA'
        return (f"The latest hit album is {album.title}, type: {album.type}, "
                f"artists: {result}.")

    return (f"The latest hit album is {album.title}, type: {album.type}, "
            f"artists: {', '.join(a.name for a in artists)}.")


def award_album(album_title):
    artists = Artist.objects.filter(album__title=album_title).update(
        awards=F('awards') + 1
    )

    if artists > 0:
        return f"Updated awards for {artists} artist/s."

    return "Updates not applicable."

