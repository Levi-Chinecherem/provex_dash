# Generated by Django 5.0.2 on 2024-02-11 00:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_alter_accountsummary_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interest',
            name='investment_plan',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='interest', to='payment.investmentplan'),
        ),
    ]