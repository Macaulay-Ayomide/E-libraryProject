# Generated by Django 3.2.9 on 2023-04-01 15:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraryhelper', '0029_auto_20230401_1542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='liberian',
            name='dob',
            field=models.DateField(default=datetime.datetime(2023, 4, 1, 15, 47, 12, 841632)),
            preserve_default=False,
        ),
    ]
