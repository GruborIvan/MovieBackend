# Generated by Django 3.2 on 2021-04-20 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0003_auto_20210419_0824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='genre',
            field=models.ManyToManyField(related_name='genres', to='myapi.MovieGenre'),
        ),
    ]