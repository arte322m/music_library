# Generated by Django 4.1.3 on 2023-02-14 10:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kAboom', '0038_auto_20230130_1204'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Genre',
            new_name='GenresTags',
        ),
        migrations.RenameField(
            model_name='track',
            old_name='genre',
            new_name='genre_tags',
        ),
    ]