# Generated by Django 2.2 on 2020-06-15 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_auto_20200615_1425'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='promotion',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=5),
        ),
    ]
