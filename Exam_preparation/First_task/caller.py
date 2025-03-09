import os

import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Movie, Actor, Director
from django.db.models import Count
from decimal import Decimal
# Create queries within functions


def get_directors(search_name=None, search_nationality=None):
    directors = 0
    if search_name is None and search_nationality is None:
        return ""

    elif search_name is None and search_nationality is not None:
        directors = Director.objects.filter(nationality__icontains=search_nationality).order_by('full_name')

    elif search_name is not None and search_nationality is None:
        directors = Director.objects.filter(full_name__icontains=search_name).order_by('full_name')

    else:
        directors = (Director.objects.filter(full_name__icontains=search_name, nationality__icontains=search_nationality)
                     .order_by('full_name'))

    if directors is None:
        return ""

    result = ""
    for director in directors:
        result += (f"Director: {director.full_name}, nationality: {director.nationality}, "
                   f"experience: {director.years_of_experience}\n")

    return result[:-1]


def get_top_director():
    top_director = (Director.objects.annotate(movies_count=Count('directors'))
                    .order_by('-movies_count', 'full_name').first())

    if top_director is None:
        return ""

    return f"Top Director: {top_director.full_name}, movies: {top_director.movies_count}."


def get_top_actor():
    top_actor = (Actor.objects.annotate(movies_count=Count('starring_actors'))
                    .order_by('-movies_count', 'full_name').first())
    if top_actor is None:
        return ""

    all_movies = Movie.objects.filter(starring_actor=top_actor.id)

    if len(all_movies) == 0:
        return ""
    average_rating = sum([m.rating for m in all_movies]) / len(all_movies)

    return (f"Top Actor: {top_actor.full_name}, "
            f"starring in movies: {', '.join([m.title for m in all_movies])}, "
            f"movies average rating: {average_rating:.1f}")


def get_actors_by_movies_count():
    actors = Actor.objects.annotate(movies_count=Count('actors')).order_by('-movies_count', 'full_name')

    if actors is None:
        return ""

    if len(actors) > 3:
        actors = actors[:3]

    result = ""
    for actor in actors:
        if actor.movies_count > 0:
            result += f"{actor.full_name}, participated in {actor.movies_count} movies\n"

    if result == "":
        return ""

    return result[:-1]


def get_top_rated_awarded_movie():
    top_movie = Movie.objects.filter(is_awarded=True).order_by('-rating', 'title').first()
    if top_movie is None:
        return ""

    starring_actor = ""
    if top_movie.starring_actor is None:
        starring_actor = "N/A"

    else:
        starring_actor = top_movie.starring_actor.full_name

    cast = ", ".join([a.full_name for a in top_movie.actors.order_by("full_name").all()])

    return (f"Top rated awarded movie: {top_movie.title}, rating: {top_movie.rating:.1f}. "
            f"Starring actor: {starring_actor}. Cast: {cast}.")


def increase_rating():
    classic_movies = Movie.objects.filter(is_classic=True).all()
    if classic_movies is None:
        return "No ratings increased."
    count_of_increased_ratings = 0

    for movie in classic_movies:
        if movie.rating <= 9.9:
            new_rating = movie.rating + Decimal(0.1)
            Movie.objects.filter(title=movie.title).update(rating=new_rating)
            count_of_increased_ratings += 1

        elif 9.9 < movie.rating < 10.0:
            Movie.objects.filter(title=movie.title).update(rating=10.0)
            count_of_increased_ratings += 1

    if count_of_increased_ratings == 0:
        return "No ratings increased."

    return f"Rating increased for {count_of_increased_ratings} movies."


