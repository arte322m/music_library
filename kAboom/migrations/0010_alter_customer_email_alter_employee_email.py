# Generated by Django 4.1.2 on 2022-10-23 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kAboom', '0009_alter_track_composer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.EmailField(max_length=60),
        ),
        migrations.AlterField(
            model_name='employee',
            name='email',
            field=models.EmailField(default=None, max_length=60),
        ),
    ]
