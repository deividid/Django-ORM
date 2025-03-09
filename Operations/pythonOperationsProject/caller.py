import os
import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()


# Import your models here
from main_app.models import Pet, Artifact, Location, Car, Task, HotelRoom


def create_pet(name: str, species: str):
    pet = Pet.objects.create(name=name, species=species)

    return f"{pet.name} is a very cute {pet.species}!"


def create_artifact(name, origin, age, description, is_magical):
    new_artifact = Artifact.objects.create(
        name=name,
        origin=origin,
        age=age,
        description=description,
        is_magical=is_magical
    )

    return f"The artifact {new_artifact.name} is {new_artifact.age} years old!"


def rename_artifact(artifact: Artifact, new_name: str):
    if artifact.is_magical == True and artifact.age > 250:
        artifact.name = new_name
        artifact.save()


def delete_all_artifacts():
    Artifact.objects.all().delete()


def show_all_locations():
    result = ''
    locations = Location.objects.all().order_by('-id')
    for location in locations:
        result += f"{location.name} has a population of {location.population}!\n"

    return result[:-1]


def new_capital():
    location = Location.objects.get(id=1)
    location.is_capital = True
    location.save()


def get_capitals():
    return Location.objects.filter(is_capital=True).values('name')


def delete_first_location():
    Location.objects.first().delete()


def apply_discount():
    cars = Car.objects.all()
    for car in cars:
        discount = sum([int(numb) for numb in str(car.year)])
        car.price_with_discount = car.price / 100 * (100 - discount)
        car.save()


def get_recent_cars():
    return Car.objects.filter(year__gt=2020).values('model', 'price_with_discount')


def delete_last_car():
   Car.objects.last().delete()


def show_unfinished_tasks():
    unfinished = Task.objects.filter(is_finished=False)
    result = ''
    for task in unfinished:
        result += f"Task - {task.title} needs to be done until {task.due_date}!\n"

    return result[:-1]


def complete_odd_tasks():
    tasks = Task.objects.all()

    for task in tasks:
        if task.id % 2 != 0:
            task.is_finished = True
            task.save()


def encode_and_replace(text, task_title):
    encoded_text = ''
    for char in text:
        encoded_text += chr(ord(char)-3)

    tasks = Task.objects.all()

    for task in tasks:
        if task.title == task_title:
            task.description = encoded_text
            task.save()


def get_deluxe_rooms():
    rooms = HotelRoom.objects.all()
    result = ''

    for room in rooms:
        if room.room_type == "Deluxe" and room.id % 2 == 0:
            result += f"Deluxe room with number {room.room_number} costs {room.price_per_night}$ per night!\n"

    return result[:-1]


def increase_room_capacity():
    rooms = HotelRoom.objects.all().order_by('id')

    previous_room_capacity = None

    for room in rooms:
        if room.is_reserved:
            if previous_room_capacity is None:
                room.capacity += room.id


            else:
                room.capacity += previous_room_capacity

            room.save()

        previous_room_capacity = room.capacity



def reserve_first_room():
    first_room = HotelRoom.objects.first()
    first_room.is_reserved = True
    first_room.save()


def delete_last_room():
    last_room = HotelRoom.objects.last()
    if last_room.is_reserved == False:
        last_room.delete()
