# Generated by Django 3.2.9 on 2023-03-25 23:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('libraryhelper', '0008_reservee_datecreated'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matric', models.CharField(max_length=100, unique=True)),
                ('totalloanbook', models.IntegerField()),
                ('totalretbook', models.CharField(max_length=100)),
                ('lstreturndate', models.DateTimeField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matric', models.CharField(max_length=100)),
                ('firstname', models.CharField(max_length=100)),
                ('department', models.CharField(max_length=100)),
                ('school', models.CharField(max_length=100)),
                ('dateloaned', models.DateTimeField(auto_now_add=True)),
                ('returndate', models.DateTimeField(blank=True)),
                ('copy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='libraryhelper.copy')),
            ],
        ),
    ]
