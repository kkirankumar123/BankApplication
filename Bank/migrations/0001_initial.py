# Generated by Django 3.2 on 2022-04-20 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bank_Details',
            fields=[
                ('Name', models.CharField(max_length=100, null=True)),
                ('Father_Name', models.CharField(max_length=100, null=True)),
                ('Account_Number', models.CharField(max_length=14, primary_key=True, serialize=False)),
                ('Amount', models.BigIntegerField(null=True)),
                ('Mobile', models.BigIntegerField(null=True)),
                ('Gender', models.CharField(max_length=6, null=True)),
                ('DOB', models.BigIntegerField(null=True)),
                ('Address', models.CharField(max_length=300, null=True)),
                ('City', models.CharField(max_length=50, null=True)),
                ('State', models.CharField(max_length=50, null=True)),
                ('Pin', models.IntegerField(null=True)),
                ('Religion', models.CharField(max_length=50, null=True)),
            ],
        ),
    ]