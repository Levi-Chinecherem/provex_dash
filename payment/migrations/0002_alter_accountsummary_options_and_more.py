# Generated by Django 5.0.2 on 2024-02-10 22:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='accountsummary',
            options={'verbose_name': 'Account Summary', 'verbose_name_plural': 'Account Summaries'},
        ),
        migrations.AlterField(
            model_name='accountsummary',
            name='account_type',
            field=models.CharField(choices=[('USDT_TRC20', 'USDT TRC20'), ('USDT_ERC20', 'USDT ERC20'), ('BTC', 'BTC')], max_length=20, unique=True),
        ),
        migrations.CreateModel(
            name='InvestmentPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan_type', models.CharField(choices=[('BASIC', 'Basic'), ('STANDARD', 'Standard'), ('PLATINUM', 'Platinum'), ('PREMIUM', 'Premium')], max_length=20, unique=True)),
                ('roi_percentage', models.DecimalField(decimal_places=2, max_digits=5)),
                ('affine_space_duration', models.CharField(max_length=10)),
                ('investment_duration', models.CharField(max_length=15)),
                ('is_active', models.BooleanField(default=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Investment Plan',
                'verbose_name_plural': 'Investment Plans',
            },
        ),
        migrations.CreateModel(
            name='Interest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('percentage_return', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('monetary_return', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('total_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('investment_plan', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='payment.investmentplan')),
            ],
        ),
    ]
