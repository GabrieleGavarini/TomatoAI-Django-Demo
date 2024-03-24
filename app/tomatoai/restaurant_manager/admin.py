from django.contrib import admin

from .models import Ristorante, Ricetta, Ingrediente

# Register your models here.
admin.site.register([Ristorante, Ricetta, Ingrediente])