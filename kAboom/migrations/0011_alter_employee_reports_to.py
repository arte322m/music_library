# Generated by Django 4.1.2 on 2022-10-23 14:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kAboom', '0010_alter_customer_email_alter_employee_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='reports_to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='kAboom.employee'),
        ),
    ]
