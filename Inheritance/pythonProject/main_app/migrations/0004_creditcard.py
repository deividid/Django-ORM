# Generated by Django 5.0.4 on 2024-08-02 15:26

import main_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_student'),
    ]

    operations = [
        migrations.CreateModel(
            name='CreditCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_owner', models.CharField(max_length=100)),
                ('card_number', main_app.models.MaskedCreditCardField(max_length=20)),
            ],
        ),
    ]
