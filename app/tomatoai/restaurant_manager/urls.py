from django.urls import path, include

from .views import RistoranteViewSet, RicettaViewSet, IngredienteViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'ristoranti', RistoranteViewSet)
router.register(r'ricette', RicettaViewSet)
router.register(r'ingredienti', IngredienteViewSet)

urlpatterns = [
    path(r'', include(router.get_urls())),
]