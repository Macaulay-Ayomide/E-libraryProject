# Generated by Django 3.2.9 on 2023-03-30 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraryhelper', '0013_liberian'),
    ]

    operations = [
        migrations.AddField(
            model_name='liberian',
            name='bio',
            field=models.TextField(default='There is nothing to know', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='liberian',
            name='gender',
            field=models.CharField(default='Male', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='liberian',
            name='nin',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='liberian',
            name='profileimg',
            field=models.ImageField(default='./blank-profile-picture-circle-hd.png', upload_to='libraryhelper/images'),
        ),
    ]
