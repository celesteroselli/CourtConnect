# Generated by Django 3.2.5 on 2023-06-17 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('juryapp', '0005_message_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jury',
            name='id',
            field=models.BigIntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='panel',
            name='id',
            field=models.BigIntegerField(primary_key=True, serialize=False),
        ),
    ]
