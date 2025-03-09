import os
import django



# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Astronaut, Mission, Spacecraft
from django.db.models import Q, F, Count


# Create queries within functions


def get_astronauts(search_string=None):
    if search_string is None:
        return ""
    correct_astronauts = Astronaut.objects.filter(
        Q(name__icontains=search_string) | Q(phone_number__icontains=search_string)
    ).order_by('name')

    if correct_astronauts is None:
        return ""

    result = ''
    for a in correct_astronauts:
        status = ''
        if a.is_active:
            status = 'Active'

        else:
            status = 'Inactive'

        result += f"Astronaut: {a.name}, phone number: {a.phone_number}, status: {status}\n"

    return result[:-1]


def get_top_astronaut():
    top_astro = Astronaut.objects.annotate(missions_count=Count('missions')).order_by('-missions_count', 'phone_number').first()
    if top_astro is None:
        return "No data."

    return f"Top Astronaut: {top_astro.name} with {top_astro.missions_count} missions."


def get_top_commander():
    top_comm = Astronaut.objects.annotate(commander_count=Count('commander')).order_by('-commander_count', 'phone_number').first()
    if top_comm is None:
        return "No data."

    return f"Top Commander: {top_comm.name} with {top_comm.commander_count} commanded missions."


def get_last_completed_mission():
    completed_missions = Mission.objects.filter(status='Completed').order_by('launch_date').first()
    if completed_missions is None:
        return "No data."

    commander_name = ''
    if completed_missions.commander is None:
        commander_name = "TBA"

    else:
        commander_name = completed_missions.commander.name

    return completed_missions.astronauts

    return (f"The last completed mission is: {completed_missions.name}. Commander: {commander_name}. "
            f" Spacecraft: {completed_missions.spacecraft.name}")


def get_most_used_spacecraft():
    most_used = (Spacecraft.objects.
                 annotate(mission_count=Count('missions_of_spacecrafts')).
                 annotate(astronauts_count=Count('missions_of_spacecrafts__astronauts'))
                 .order_by('-mission_count', 'name').first())

    if most_used is None:
        return "No data."

    return (f"The most used spacecraft is: {most_used.name}, manufactured by {most_used.manufacturer},"
            f" used in {most_used.mission_count}"
            f" missions, astronauts on missions: {most_used.astronauts_count}.")




