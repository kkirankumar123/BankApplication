# Generated by Django 3.2 on 2022-05-13 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bank', '0003_transact_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transact_details',
            name='Pin',
            field=models.IntegerField(null=True),
        ),
    ]