# Generated by Django 3.2.9 on 2023-04-01 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraryhelper', '0031_alter_liberian_dob'),
    ]

    operations = [
        migrations.AlterField(
            model_name='liberian',
            name='dob',
            field=models.DateField(),
        ),
    ]
