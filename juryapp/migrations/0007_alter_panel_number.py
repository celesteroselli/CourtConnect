# Generated by Django 3.2.5 on 2023-06-17 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('juryapp', '0006_auto_20230617_2053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='panel',
            name='number',
            field=models.IntegerField(max_length=10),
        ),
    ]
