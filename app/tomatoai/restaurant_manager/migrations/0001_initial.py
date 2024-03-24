# Generated by Django 5.0.3 on 2024-03-24 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingrediente',
            fields=[
                ('nome', models.CharField(max_length=100, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Ricetta',
            fields=[
                ('nome', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('ingredienti', models.ManyToManyField(blank=True, related_name='ricette', to='restaurant_manager.ingrediente')),
            ],
        ),
        migrations.CreateModel(
            name='Ristorante',
            fields=[
                ('nome', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('indirizzo', models.CharField(max_length=100)),
                ('ricette', models.ManyToManyField(blank=True, related_name='ristoranti', to='restaurant_manager.ricetta')),
            ],
        ),
    ]