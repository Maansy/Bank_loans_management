# Generated by Django 4.2.7 on 2023-11-14 10:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_bankpersonnel_is_active_and_more'),
        ('loans', '0005_loanrequest_loanpayment_generalinfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loanrequest',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.loancustomer'),
        ),
    ]