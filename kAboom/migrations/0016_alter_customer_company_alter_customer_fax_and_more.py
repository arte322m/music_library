# Generated by Django 4.1.2 on 2022-10-23 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kAboom', '0015_rename_county_customer_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='company',
            field=models.CharField(max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='fax',
            field=models.CharField(max_length=24, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='postal_code',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='state',
            field=models.CharField(max_length=40, null=True),
        ),
    ]
