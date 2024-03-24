import sys

from django.urls import reverse

from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.test import APITestCase

from ..models import Ristorante, Ricetta, Ingrediente

class IngredienteTestCase(APITestCase):

    @staticmethod
    def print_results(test_case_name, response):
        print('\n' + '*' * 50)
        print(test_case_name)
        print("Status:", response.status_code)
        print("Data:", response.data)
        print('*' * 50)

    
    @classmethod
    def setUpTestData(cls):
        """
        Configura il database di test con dati iniziali per eseguire test che non modificano
        i dati. Questo metodo crea ingredienti, ricette e ingredienti di esempio per testare
        le relazioni tra questi oggetti nel database.

        Ingredienti creati: Pomodoro, Mozzarella.
        Ricette create: Pizza Margherita (ingredienti: Pomodoro, Mozzarella),
                        Insalata Caprese (ingredienti: Pomodoro, Mozzarella).
        Ristoranti creati: Da Mario (ricette: Pizza Margherita),
                        La Pergola (ricette: Insalata Caprese).
        """
        # Creazione ingredienti
        ingrediente1 = Ingrediente.objects.create(nome='Pomodoro', produttore='Produttore Locale')
        ingrediente2 = Ingrediente.objects.create(nome='Mozzarella', produttore='Produttore Locale')
        
        # Creazione ricette
        ricetta1 = Ricetta.objects.create(nome='Pizza Margherita')
        ricetta1.ingredienti.add(ingrediente1, ingrediente2)
        ricetta2 = Ricetta.objects.create(nome='Insalata Caprese')
        ricetta2.ingredienti.add(ingrediente1, ingrediente2)
        
        # Creazione ingredienti
        Ristorante.objects.create(nome='Da Mario', indirizzo='Via Roma 1').ricette.add(ricetta1)
        Ristorante.objects.create(nome='La Pergola', indirizzo='Via Milano 2').ricette.add(ricetta2)

    def test_list_ingredienti(self):
        """
        Testa la funzionalità di elenco dei ingredienti per verificare che la richiesta GET
        all'endpoint 'ingrediente-list' ritorni un successo HTTP 200 OK e che l'elenco dei ingredienti
        restituito sia di lunghezza 2, corrispondente al numero di ingredienti predefiniti
        nel database di test.
        """
        # Call
        url = reverse('ingrediente-list') 
        response = self.client.get(url)

        # Check
        self.print_results(test_case_name=sys._getframe().f_code.co_name, response=response)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_by_nome_ristorante(self):
        """
        Testa il filtro dei ingredienti per nome attraverso l'endpoint 'ingrediente-list'.
        Verifica che, passando il nome 'Da Mario' come parametro di query, la risposta sia HTTP 200 OK,
        che la lunghezza dei dati restituiti sia 1, e che il nome del ingrediente nei dati
        corrisponda a 'Pomodoro'.
        """
        # Call
        url = reverse('ingrediente-list') + '?nome_ristorante=Da Mario'
        response = self.client.get(url)

        # Check
        self.print_results(test_case_name=sys._getframe().f_code.co_name, response=response)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['nome'], 'Mozzarella')
        self.assertEqual(response.data[1]['nome'], 'Pomodoro')

    def test_filter_by_nome_ricetta(self):
        """
        Testa il filtro dei ingredienti per nome ricetta tramite l'endpoint 'ingrediente-list'.
        Controlla che, fornendo 'Pizza Margherita' come parametro di query, si riceva una risposta
        HTTP 200 OK, che la lunghezza dei dati restituiti sia 1, e che il nome del ingrediente
        nei dati sia 'Pomodoro'.
        """
        # Call
        url = reverse('ingrediente-list') + '?nome_ricetta=Pizza Margherita'
        response = self.client.get(url)

        # Check
        self.print_results(test_case_name=sys._getframe().f_code.co_name, response=response)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['nome'], 'Mozzarella')
        self.assertEqual(response.data[1]['nome'], 'Pomodoro')

    def test_filter_by_nome_ingrediente(self):
        """
        Testa il filtro dei ingredienti per nome attraverso l'endpoint 'ingrediente-list'.
        Verifica che, passando il nome 'Pomodoro' come parametro di query, la risposta sia HTTP 200 OK,
        che la lunghezza dei dati restituiti sia 1, e che il nome del ingrediente nei dati
        corrisponda a 'Pomodoro'.
        """
        # Call
        url = reverse('ingrediente-list') + '?nome_ingrediente=Pomodoro'
        response = self.client.get(url)

        # Check
        self.print_results(test_case_name=sys._getframe().f_code.co_name, response=response)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['nome'], 'Pomodoro')

    def test_create_ingrediente(self):
        """
        Testa la creazione di un nuovo ingrediente tramite POST all'endpoint 'ingrediente-list'.
        Verifica che inviando i dati di un nuovo ingrediente, la risposta sia HTTP 201 Created,
        e che il conteggio totale dei ingredienti nel database aumenti a 3.
        """
        # Call
        url = reverse('ingrediente-list')
        data = {'nome': 'Basilico', 'ricette': ['Pizza Margherita'], 'produttore': 'Produttore Locale'}
        response = self.client.post(url, data)

        # Check
        self.print_results(test_case_name=sys._getframe().f_code.co_name, response=response)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(Ingrediente.objects.count(), 3) 

    def test_update_ingrediente_put(self):
        """
        Testa l'aggiornamento completo di un ingrediente esistente usando il metodo PUT.
        Verifica che il produttore del ingrediente venga aggiornato correttamente e che la risposta
        sia HTTP 200 OK. Controlla inoltre che il database rifletta l'aggiornamento.
        """
        # Call
        ingrediente_to_update = Ingrediente.objects.first()
        url = reverse('ingrediente-detail', kwargs={'pk': ingrediente_to_update.nome}) 
        data = {'nome': ingrediente_to_update.nome, 'produttore': 'Esselunga'}
        response = self.client.put(url, data)

        # Check
        self.print_results(test_case_name=sys._getframe().f_code.co_name, response=response)
        self.assertEqual(response.status_code, HTTP_200_OK)
        ingrediente_to_update.refresh_from_db()
        self.assertEqual(ingrediente_to_update.produttore, 'Esselunga')

    def test_partial_update_ingrediente_patch(self):
        """
        Testa l'aggiornamento parziale (PATCH) di un ingrediente, focalizzandosi sul produttore.
        Verifica che dopo l'invio della richiesta PATCH, la risposta sia HTTP 200 OK e che
        il produttore del ingrediente nel database sia stato aggiornato come specificato.
        """
        # Call
        ingrediente_to_update = Ingrediente.objects.first()
        url = reverse('ingrediente-detail', kwargs={'pk': ingrediente_to_update.nome})
        data = {'produttore': 'Esselunga'}
        response = self.client.patch(url, data)

        # Check
        self.print_results(test_case_name=sys._getframe().f_code.co_name, response=response)
        self.assertEqual(response.status_code, HTTP_200_OK)
        ingrediente_to_update.refresh_from_db()
        self.assertEqual(ingrediente_to_update.produttore, 'Esselunga')

    def test_delete_ingrediente(self):
        """
        Testa la cancellazione di un ingrediente dall'endpoint 'ingrediente-detail'.
        Verifica che dopo la richiesta DELETE, la risposta sia HTTP 204 No Content e che
        il conteggio dei ingredienti nel database sia ridotto a 1.
        """
        # Call
        ingrediente_to_delete = Ingrediente.objects.first()
        url = reverse('ingrediente-detail', kwargs={'pk': ingrediente_to_delete.nome})
        response = self.client.delete(url)

        # Check
        self.print_results(test_case_name=sys._getframe().f_code.co_name, response=response)
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
        self.assertEqual(Ingrediente.objects.count(), 1) 
