# Generated by Django 3.2.9 on 2023-03-31 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraryhelper', '0019_auto_20230331_0428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='pdf_available',
            field=models.BooleanField(blank=True, default=True),
        ),
    ]
