# Generated by Django 4.1.2 on 2022-10-23 15:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kAboom', '0012_employee_birth_date_employee_hire_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='support_rep_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kAboom.employee'),
        ),
    ]
