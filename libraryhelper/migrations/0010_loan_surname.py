# Generated by Django 3.2.9 on 2023-03-25 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraryhelper', '0009_loan_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='surname',
            field=models.CharField(default='nulll', max_length=100),
            preserve_default=False,
        ),
    ]
