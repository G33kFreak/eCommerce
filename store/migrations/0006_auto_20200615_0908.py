# Generated by Django 2.2 on 2020-06-15 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='phoneNum',
            field=models.CharField(max_length=15),
        ),
    ]