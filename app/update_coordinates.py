from app import db
from app.models import Listing

# Voeg standaard latitude en longitude toe aan alle listings die deze missen
listings = Listing.query.filter((Listing.latitude == None) | (Listing.longitude == None)).all()
for listing in listings:
    listing.latitude = 51.05  # Voeg een standaardbreedtegraad toe (bijvoorbeeld Gent)
    listing.longitude = 3.716  # Voeg een standaardlengtegraad toe (bijvoorbeeld Gent)

# Opslaan in de database
db.session.commit()
print(f"{len(listings)} listings zijn bijgewerkt met standaardlocaties.")
