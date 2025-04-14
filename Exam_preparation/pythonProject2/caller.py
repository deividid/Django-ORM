import os
import django
from django.db.models import Q, F

from main_app.models import House, Dragon, Quest

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

# Create queries within functions


def get_houses(string):

    houses = House.objects.filter(
        Q(name__icontains=string)
        |
        Q(moto__icontains=string)

    ).order_by('-wins', 'name')

    if string is None or houses is None:
        return "No houses match your search."

    result = ''

    for h in houses:
        mot = 'N/A'
        if h.motto:
            mot = h.motto

        result += f'House: {h.name}, wins: {h.wins}, motto: {mot}"/n"'

    return result


def get_most_dangerous_houses():
    house = House.objects.get_houses_by_dragons_count().first()

    if house in None:
        return "No relevant data."

    rul = 'ruling'

    if not house.is_ruling:
        rul = 'not ruling'

    return f'The most dangerous house is the House of {house.name} with {house.dragon_count} dragons. Currently {rul} the kingdom.'


def get_the_most_powerful_dragon():
    dragon = Dragon.objects.filter(is_healthy=True).order_by('-wins')[0]

    if dragon in None:
        return "No relevant data."

    return (f"The most powerful healthy dragon is {dragon.name} with a power level of {dragon.power},"
            f" breath type {dragon.breath}, and {dragon.wins} wins, "
            f"coming from the house of {dragon.house__name}. "
            f"Currently participating in {dragon.quest_set.count()} quests.")


def update_dragons_data():
    injured_dragons = Dragon.objects.filter(power__gt=1.0, is_healthy=False).update(
        power=F('power') - 0.1,
        is_healthy=True
    )

    min_power = Dragon.objects.order_by('power').first().power

    return (f"The data for {injured_dragons} dragon/s has been changed. "
            f"The minimum power level among all dragons is {min_power}")


def get_earliest_quest():
    quest = Quest.objects.order_by('start_time').first()
    d = quest.start_time
    total_power = 0
    count = 0
    for d in quest.dragons:
        total_power += d.power
        count += 1
    return (f"The earliest quest is: {quest.name}, code: {quest.code}, "
            f"start date: {d.day}.{d.month}.{d.year}, host: {quest.host__name}. "
            f"Dragons: {'*'.join(d.name for d in quest.dragons)}. "
            f"Average dragons power level: {(total_power / count):.2f}")



