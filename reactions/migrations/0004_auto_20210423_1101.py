# Generated by Django 3.2 on 2021-04-23 11:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reactions', '0003_alter_reactions_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reactions',
            name='reaction',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='reactions',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
