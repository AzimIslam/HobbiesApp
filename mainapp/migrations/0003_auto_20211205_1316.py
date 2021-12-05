# Generated by Django 3.2.7 on 2021-12-05 13:16

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_alter_hobby_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='friends',
            field=models.ManyToManyField(blank=True, related_name='_mainapp_user_friends_+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='country',
            name='name',
            field=models.CharField(max_length=150, unique=True),
        ),
    ]
