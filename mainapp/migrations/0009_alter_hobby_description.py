# Generated by Django 3.2.7 on 2021-12-08 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0008_alter_user_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hobby',
            name='description',
            field=models.TextField(),
        ),
    ]