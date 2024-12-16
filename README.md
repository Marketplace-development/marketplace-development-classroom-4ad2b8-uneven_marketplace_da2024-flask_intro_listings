
# TravelTales
TravelTales is een website voor het uploaden en zoeken van reizen. Het is bedoeld als een alternatief voor dure reisbureaus, waarbij je bij TravelTales een heel groot aanbod hebt van verschillende soorten reizen over bijna alle landen van de wereld voor een zeer betaalbare prijs. Door eenvoudigweg een pdf te uploaden waarin al je tips en tricks staan van je reisbestemming, kan je mensen over de hele werd inspireren. 
“Share your journey, inspire others” 


## Functionaliteiten
Plaatsen van reizen: plaats een pdf van je reis en verdien er zelfs geld aan!
Zoeken van reizen: Vind reizen die bij je passen en start een transactie. Je kan deze reis dan kopen.
Reviews schrijven en beheren: Geef feedback over je gekochte reis en draag zo mee aan een meer transparante website!
Gebruikers zoeken: Zoek andere spelers op gebruikersnaam en bekijk hun profiel en reizen.

## Kaart-integratie
Je kan reizen zoeken op basis van een kaart, daarbij kan je ook bijhouden waar je allemaal op reis bent geweest na het uploaden van je reizen op de kaart.

## Installatie
Volg deze stappen om TravelTales lokaal te installeren en ervoor te zorgen dat het correct werkt met Flask:

### Vereisten
Python 3.9+
Pip (Python Package Installer)
Virtualenv (optioneel, voor een virtuele omgeving)
Instructies
Clone de repository
Clone de repository vanuit GitHub naar je lokale machine:

git clone https://github.com/Marketplace-development/uneven-marketplace-da2024-group21.git
Ga naar de projectmap

cd uneven-marketplace-da2024-group21
Maak een virtuele omgeving aan (optioneel)

python -m venv venv
source venv/bin/activate  # Voor Mac/Linux
venv\Scripts\activate     # Voor Windows
Installeer de vereisten
Installeer de benodigde Python-pakketten:

pip install flask flask-sqlalchemy flask-migrate sqlalchemy python-ics
Start de applicatie

flask run
Indien foutmelding ("Port in use")
Start de applicatie op een andere poort:

flask run --port=5001

## Links
### Figma
Bekijk hier onze [Figma](https://www.figma.com/design/h13wQmiQYUlBzGYlLRwLwC/Flux---Figma-Build-Tutorial-(Starter)-(Community)?node-id=0-1&p=f) om ons conceptuele design te zien.


