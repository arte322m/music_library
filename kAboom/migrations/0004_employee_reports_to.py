# Generated by Django 4.1.2 on 2022-10-22 09:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kAboom', '0003_customer_support_rep_id_employee_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='reports_to',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='kAboom.employee'),
            preserve_default=False,
        ),
    ]
