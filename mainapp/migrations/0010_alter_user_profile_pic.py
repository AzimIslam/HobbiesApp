# Generated by Django 3.2.7 on 2021-12-09 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0009_alter_hobby_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_pic',
            field=models.ImageField(blank=True, default='default.png', null=True, upload_to=''),
        ),
    ]
