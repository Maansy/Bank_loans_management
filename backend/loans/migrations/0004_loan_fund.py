# Generated by Django 4.2.4 on 2023-11-12 16:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('funds', '0001_initial'),
        ('loans', '0003_alter_loan_interest_type_alter_loan_loan_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='fund',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='funds.fund'),
            preserve_default=False,
        ),
    ]
