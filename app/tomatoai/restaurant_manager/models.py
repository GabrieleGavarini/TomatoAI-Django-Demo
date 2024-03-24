from django.db import models


    
class Ingrediente(models.Model):
    """
    Un ingrediente 
    """
    nome = models.CharField(max_length=100,
                            primary_key=True)
    
    produttore = models.CharField(max_length=100)
    
    # Utils
    def __str__(self) -> str:
        return self.nome 
    

class Ricetta(models.Model):
    """
    Un ricetta che contiene una lista di ingredienti 
    """
    # Nome della ricetta
    nome = models.CharField(max_length=100, primary_key=True)

    # Ricette che usano l-ingrediente
    ingredienti = models.ManyToManyField(Ingrediente, 
                                         blank=True,
                                         related_name='ricette')

    # Utils
    def __str__(self) -> str:
        return self.nome 
    
class Ristorante(models.Model):
    """
    Un ristorante che contiene una listsa di ricette
    """
    # Nome del ristorante
    nome = models.CharField(max_length=100,
                            primary_key=True)
    indirizzo = models.CharField(max_length=100)

    # Ricette associate al ristorante
    ricette = models.ManyToManyField(Ricetta, 
                                     blank=True,
                                     related_name='ristoranti')

    # Utils
    def __str__(self) -> str:
        return self.nome 

