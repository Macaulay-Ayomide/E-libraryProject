# Generated by Django 3.2.9 on 2023-04-30 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraryhelper', '0035_alter_reservee_matric'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='expectedreturndate',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]