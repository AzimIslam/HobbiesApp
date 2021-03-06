# Generated by Django 3.2.7 on 2021-12-05 17:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_alter_user_hobbies'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='city',
            name='country',
        ),
        migrations.AlterField(
            model_name='user',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users', to='mainapp.city'),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_pic',
            field=models.ImageField(blank=True, upload_to=''),
        ),
        migrations.DeleteModel(
            name='Country',
        ),
    ]
