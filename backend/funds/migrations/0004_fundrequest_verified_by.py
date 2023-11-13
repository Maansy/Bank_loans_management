# Generated by Django 4.2.4 on 2023-11-12 21:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_bankpersonnel_is_active_and_more'),
        ('funds', '0003_fundpayment'),
    ]

    operations = [
        migrations.AddField(
            model_name='fundrequest',
            name='verified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.bankpersonnel'),
        ),
    ]
