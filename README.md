# Eindopdracht Python Enterprise

## Automatisatie voor de Brella CEO
Een paraplufabrikant en verkoper Brella houdt nu nog handmatig bij hoeveel paraplu's zij in voorraad hebben. De CEO wil daarom een slag maken in de automatisatie voor de administratie van de voorraad. Hiervoor willen ze dat jullie een applicatie ontwikkelen waarin een verkoper kan inloggen en zijn of haar transacties kan invoeren zodat ze in een database worden opgeslagen. Hiervoor zijn de volgende onderdelen nodig:

### SQLite Database met de volgende tabellen:
* Inloggegevens tabel
  * Naam
  * Wachtwoord
  * Mailadres
  * Functie

* Transactie tabel
  * Aantal paraplu's
  * Naam (van uitvoering transactie)
  * Datum 
  * Verkoopprijs
  * Inkoopprijs

### GUI met de volgende functionaliteiten:

* Inloggen

* Paraplu transactie invoeren

## Klachten van de manager

Na het invoeren van de nieuwe applicaties zijn de verkopers en producenten erg blij met de efficiëntie winst. Alleen een van de managers begint te klagen dat hij het overzicht van de huidige voorraad kwijt is. Hij wil daarom hij een aantal extra functionaliteiten:

* Een extra knop in de GUI die een mail naar hem stuurt met de volgende inhoud:

* Een overzicht van de huidige voorraad

* Weersvoorspelling voor de komende vijf dagen (met nadruk op regenval)

### Bonus: rapportagefunctie die overige informatie over de verkoop van paraplu’s door de verschillende verkopers

## Extra wensen van de ICT afdeling

Nu de manager ook tevreden is met zijn nieuwe informatie, vraagt een ict’er van het team wat er gebeurt als de database per ongeluk wordt verwijderd. Het lijkt hem handig als er ook een mogelijkheid is om een backup te maken in een CSV file.

* Voeg een knop toe om een CSV export te maken:

* Zorg dat de backup in een unieke folder komt met de datum als naam

### Bonus: maak een script om met een backup de database opnieuw te vullen, eventueel kun je een speciaal venster maken waarin de backup geselecteerd kan worden.

## Nieuwe storm paraplu

Brella draait door de nieuwe applicatie steeds hogere winsten en wil investeren in een nieuw soort paraplu. Helaas is het met de huidige applicatie is niet mogelijk om onderscheid te maken tussen verschillende soorten paraplu’s.

* Voeg een dropdown toe om bij de transacties ook de type paraplu mee te geven, maak hiervoor wijzigingen die nodig zijn aan de data structuur. 

* Bonus: zorg ook dat de rapportages aangepast en uitgebreid worden.

## Bonus ideeën

### Zorg dat er een rollen en rechten systeem is, bijvoorbeeld:
* Rollen: admin, verkoper, manager
  * Rechten admin: beheren gebruikers view + alles wat verkoper mag
  * Rechten manager: inzien alle verkopen + genereren rapportages + alles wat verkoper mag
  * Rechten verkoper: toevoegen, inzien en wijzigen van eigen transacties

### Breid het login systeem uit:

* Wachtwoord vergeten functionaliteit
* Zorg dat wachtwoorden secure opgeslagen worden

### Automatische rapportage:

* Mail de rapportages dagelijks automatisch naar de managers 
* Stel de admin op de hoogte via mail bij nieuw wachtwoord aanvragen en ongewone login patronen

### Automatische backups ieder uur (CSV)

### Voeg unit tests voor het project toe

### Voorraad voorspelling: implementeer een basis machine learning model om de behoefte aan voorraad te voorspellen gebaseerd op het weer en historische verkoopcijfers.