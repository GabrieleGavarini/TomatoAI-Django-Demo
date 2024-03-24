from rest_framework.serializers import ModelSerializer
from .models import Ricetta, Ristorante, Ingrediente

class IngredienteSerializer(ModelSerializer):

    class Meta:
        model = Ingrediente
        fields = '__all__'

class RicettaSerializer(ModelSerializer):
    ingrediente = IngredienteSerializer(many=True, read_only=True)

    class Meta:
        model = Ricetta
        fields = "__all__"

class RistoranteSerializer(ModelSerializer):
    ricetta = RicettaSerializer(many=True, read_only=True)

    class Meta:
        model = Ristorante
        fields = "__all__"
