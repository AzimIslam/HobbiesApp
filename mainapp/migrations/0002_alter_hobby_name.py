# Generated by Django 3.2.7 on 2021-12-05 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hobby',
            name='name',
            field=models.CharField(max_length=150, unique=True),
        ),
    ]