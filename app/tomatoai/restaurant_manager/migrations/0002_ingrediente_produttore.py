# Generated by Django 5.0.3 on 2024-03-24 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant_manager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingrediente',
            name='produttore',
            field=models.CharField(default='Produttore Locale', max_length=100),
            preserve_default=False,
        ),
    ]
