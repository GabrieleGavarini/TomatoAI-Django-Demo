import sys

from django.urls import reverse

from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.test import APITestCase

from ..models import Ristorante, Ricetta, Ingrediente

class RistoranteTestCase(APITestCase):

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
        i dati. Questo metodo crea ingredienti, ricette e ristoranti di esempio per testare
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
        
        # Creazione ristoranti
        Ristorante.objects.create(nome='Da Mario', indirizzo='Via Roma 1').ricette.add(ricetta1)
        Ristorante.objects.create(nome='La Pergola', indirizzo='Via Milano 2').ricette.add(ricetta2)

    def test_list_ristoranti(self):
        """
        Testa la funzionalità di elenco dei ristoranti per verificare che la richiesta GET
        all'endpoint 'ristorante-list' ritorni un successo HTTP 200 OK e che l'elenco dei ristoranti
        restituito sia di lunghezza 2, corrispondente al numero di ristoranti predefiniti
        nel database di test.
        """
        # Call
        url = reverse('ristorante-list') 
        response = self.client.get(url)

        # Check
        self.print_results(test_case_name=sys._getframe().f_code.co_name, response=response)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_by_nome_ristorante(self):
        """
        Testa il filtro dei ristoranti per nome attraverso l'endpoint 'ristorante-list'.
        Verifica che, passando il nome 'Da Mario' come parametro di query, la risposta sia HTTP 200 OK,
        che la lunghezza dei dati restituiti sia 1, e che il nome del ristorante nei dati
        corrisponda a 'Da Mario'.
        """
        # Call
        url = reverse('ristorante-list') + '?nome_ristorante=Da Mario'
        response = self.client.get(url)

        # Check
        self.print_results(test_case_name=sys._getframe().f_code.co_name, response=response)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['nome'], 'Da Mario')

    def test_filter_by_nome_ricetta(self):
        """
        Testa il filtro dei ristoranti per nome ricetta tramite l'endpoint 'ristorante-list'.
        Controlla che, fornendo 'Pizza Margherita' come parametro di query, si riceva una risposta
        HTTP 200 OK, che la lunghezza dei dati restituiti sia 1, e che il nome del ristorante
        nei dati sia 'Da Mario'.
        """
        # Call
        url = reverse('ristorante-list') + '?nome_ricetta=Pizza Margherita'
        response = self.client.get(url)

        # Check
        self.print_results(test_case_name=sys._getframe().f_code.co_name, response=response)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['nome'], 'Da Mario')

    def test_create_ristorante(self):
        """
        Testa la creazione di un nuovo ristorante tramite POST all'endpoint 'ristorante-list'.
        Verifica che inviando i dati di un nuovo ristorante, la risposta sia HTTP 201 Created,
        e che il conteggio totale dei ristoranti nel database aumenti a 3.
        """
        # Call
        url = reverse('ristorante-list')
        data = {'nome': 'Nuovo Ristorante', 'indirizzo': 'Via Nuova 3'}
        response = self.client.post(url, data)

        # Check
        self.print_results(test_case_name=sys._getframe().f_code.co_name, response=response)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(Ristorante.objects.count(), 3) 

    def test_update_ristorante_put(self):
        """
        Testa l'aggiornamento completo di un ristorante esistente usando il metodo PUT.
        Verifica che l'indirizzo del ristorante venga aggiornato correttamente e che la risposta
        sia HTTP 200 OK. Controlla inoltre che il database rifletta l'aggiornamento.
        """
        # Call
        ristorante_to_update = Ristorante.objects.first()
        url = reverse('ristorante-detail', kwargs={'pk': ristorante_to_update.nome}) 
        data = {'nome': ristorante_to_update.nome, 'indirizzo': 'Via Aggiornata 123'}
        response = self.client.put(url, data)

        # Check
        self.print_results(test_case_name=sys._getframe().f_code.co_name, response=response)
        self.assertEqual(response.status_code, HTTP_200_OK)
        ristorante_to_update.refresh_from_db()
        self.assertEqual(ristorante_to_update.indirizzo, 'Via Aggiornata 123')

    def test_partial_update_ristorante_patch(self):
        """
        Testa l'aggiornamento parziale (PATCH) di un ristorante, focalizzandosi sull'indirizzo.
        Verifica che dopo l'invio della richiesta PATCH, la risposta sia HTTP 200 OK e che
        l'indirizzo del ristorante nel database sia stato aggiornato come specificato.
        """
        # Call
        ristorante_to_update = Ristorante.objects.first()
        url = reverse('ristorante-detail', kwargs={'pk': ristorante_to_update.nome})
        data = {'indirizzo': 'Via Parzialmente Aggiornata 456'}
        response = self.client.patch(url, data)

        # Check
        self.print_results(test_case_name=sys._getframe().f_code.co_name, response=response)
        self.assertEqual(response.status_code, HTTP_200_OK)
        ristorante_to_update.refresh_from_db()
        self.assertEqual(ristorante_to_update.indirizzo, 'Via Parzialmente Aggiornata 456')

    def test_delete_ristorante(self):
        """
        Testa la cancellazione di un ristorante dall'endpoint 'ristorante-detail'.
        Verifica che dopo la richiesta DELETE, la risposta sia HTTP 204 No Content e che
        il conteggio dei ristoranti nel database sia ridotto a 1.
        """
        # Call
        ristorante_to_delete = Ristorante.objects.first()
        url = reverse('ristorante-detail', kwargs={'pk': ristorante_to_delete.nome})
        response = self.client.delete(url)

        # Check
        self.print_results(test_case_name=sys._getframe().f_code.co_name, response=response)
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
        self.assertEqual(Ristorante.objects.count(), 1) 
