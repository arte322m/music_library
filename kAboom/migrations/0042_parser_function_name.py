# Generated by Django 4.1.3 on 2023-02-15 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kAboom', '0041_rename_genrestags_genretag_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='parser',
            name='function_name',
            field=models.CharField(default=None, max_length=40, null=True),
        ),
    ]