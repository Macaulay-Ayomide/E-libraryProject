# Generated by Django 3.2.9 on 2023-04-01 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraryhelper', '0022_alter_book_approve'),
    ]

    operations = [
        migrations.AlterField(
            model_name='copy',
            name='approve',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='copy',
            name='available',
            field=models.BooleanField(default=False),
        ),
    ]
