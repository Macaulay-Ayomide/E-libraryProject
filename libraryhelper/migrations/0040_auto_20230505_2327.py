# Generated by Django 3.2.9 on 2023-05-05 23:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('libraryhelper', '0039_alter_book_popular'),
    ]

    operations = [
        migrations.AddField(
            model_name='liberian',
            name='dateadded',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='liberian',
            name='last_log',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]