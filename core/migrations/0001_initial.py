# Generated by Django 4.2 on 2023-05-15 05:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CashOut',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('pay_to', models.CharField(max_length=128)),
                ('remarks', models.CharField(max_length=128)),
                ('date', models.DateField()),
                ('mode', models.CharField(choices=[('phone_pay', 'Phone Pay'), ('cash', 'Cash'), ('card_pay', 'Card Pay'), ('cheque_pay', 'Cheque Pay'), ('others', 'Others')], default='phone_pay', max_length=10)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CashIn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('type', models.CharField(choices=[('salary', 'Salary'), ('loan', 'Loan'), ('rent', 'Rent'), ('others', 'Others')], default='salary', max_length=6)),
                ('mode', models.CharField(choices=[('bank_deposit', 'Bank Deposit'), ('cash', 'Cash'), ('phone_pay', 'Phone Pay'), ('other', 'Other')], default='bank_deposite', max_length=15)),
                ('note', models.CharField(max_length=256)),
                ('date', models.DateField()),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
