from rest_framework.viewsets import ModelViewSet

from .models import Ristorante, Ricetta, Ingrediente
from .serializers import RistoranteSerializer, RicettaSerializer, IngredienteSerializer

class RistoranteViewSet(ModelViewSet):
    queryset = Ristorante.objects.all()
    serializer_class = RistoranteSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        nome_ristorante = self.request.query_params.get('nome_ristorante', None)
        nome_ricetta = self.request.query_params.get('nome_ricetta', None)

        filter_dict = {}

        if nome_ristorante:
            filter_dict['nome'] = nome_ristorante
        if nome_ricetta:
            filter_dict['ricette__nome'] = nome_ricetta

        queryset = queryset.filter(**filter_dict)

        return queryset
    

class RicettaViewSet(ModelViewSet):
    serializer_class = RicettaSerializer
    queryset = Ricetta.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        nome_ristorante = self.request.query_params.get('nome_ristorante', None)
        nome_ricetta = self.request.query_params.get('nome_ricetta', None)
        nome_ingrediente = self.request.query_params.get('nome_ingrediente', None)

        filter_dict = {}

        if nome_ricetta:
            filter_dict['nome'] = nome_ricetta
        if nome_ristorante:
            filter_dict['ristoranti__nome'] = nome_ristorante
        if nome_ingrediente:
            filter_dict['ingredienti__nome'] = nome_ingrediente

        queryset = queryset.filter(**filter_dict)

        return queryset

class IngredienteViewSet(ModelViewSet):
    serializer_class = IngredienteSerializer
    queryset = Ingrediente.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        nome_ristorante = self.request.query_params.get('nome_ristorante', None)
        nome_ricetta = self.request.query_params.get('nome_ricetta', None)
        nome_ingrediente = self.request.query_params.get('nome_ingrediente', None)

        filter_dict = {}

        if nome_ingrediente:
            filter_dict['nome'] = nome_ingrediente
        if nome_ricetta:
            nome_ricetta['ricette__nome'] = nome_ricetta
        if nome_ristorante:
            filter_dict['ricette__ristoranti__nome'] = nome_ristorante

        queryset = queryset.filter(**filter_dict)

        return queryset