from django.db import models


class Employees(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    photo = models.URLField()
    birth_date = models.DateField()
    works_full_time = models.BooleanField()
    created_on = models.DateTimeField()


class Department(models.Model):
    cities = [
        ("Sofia", "Sofia"),
        ("Plovdiv", "Plovdiv"),
        ("Burgas", "Burgas"),
        ("Varna", "Varna")
    ]
    code = models.CharField(max_length=4, primary_key=True, unique=True)
    name = models.CharField(max_length=50, unique=True)
    employee_count = models.PositiveIntegerField(default=1, verbose_name="Employee Count")
    location = models.CharField(max_length=20, choices=cities)
    last_edited_on = models.DateTimeField(auto_now=True, editable=False)
