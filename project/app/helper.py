from . import db
from .models import Meldingen  # Zorg ervoor dat je het juiste model importeert

def create_notification(recipient_id, sender_id=None, good_id=None, message=""):
    new_notification = Meldingen(  # Gebruik de correcte modelnaam
        recipient_id=recipient_id,
        sender_id=sender_id,
        good_id=good_id,
        message=message
    )
    db.session.add(new_notification)
    db.session.commit()
