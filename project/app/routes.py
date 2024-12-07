# app/routes.py
import datetime
import uuid
from flask import Blueprint, request, redirect, url_for, render_template, session
from .models import db, Users, DigitalGoods
from flask import flash
from werkzeug.utils import secure_filename
from .config import supabase
from supabase import Client
from flask import Response


main = Blueprint('main', __name__)

@main.route('/')
def index():
    if 'userid' in session:
        user = Users.query.get(session['userid'])
        return render_template('index.html', username=user.firstname)
    return render_template('index.html', username=None)

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Haal gegevens op uit het formulier
        email = request.form.get('email')
        password = request.form.get('password')  # Zorg dat je wachtwoord veilig opslaat!
        first_name = request.form.get('firstname')
        last_name = request.form.get('lastname')
        address = request.form.get('address')
        city = request.form.get('city')
        postal_code = request.form.get('postalcode')
        country = request.form.get('country')
        phone = request.form.get('phone')
        nationality = request.form.get('nationality')

        # Controleer of de gebruiker al bestaat op basis van email of username
        if Users.query.filter((Users.email == email)).first():
            return "Email or Username already registered", 400

        # Maak een nieuwe gebruiker aan
        new_user = Users(
            userid=str(uuid.uuid4()),  # Genereer een unieke ID
            email=email,
            password=password,  # Hash het wachtwoord
            firstname=first_name,
            lastname=last_name,
            address=address,
            city=city,
            postalcode=postal_code,
            country=country,
            phone=phone,
            nationality=nationality
        )

        # Voeg de gebruiker toe aan de database
        db.session.add(new_user)
        db.session.commit()

        # Sla de userid op in de sessie
        session['userid'] = new_user.userid

        return redirect(url_for('main.index'))

    # Bij een GET-verzoek toon het registratieformulier
    return render_template('register.html')


@main.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']  # Zorg dat het wachtwoord ook wordt opgehaald

        # Zoek de gebruiker op basis van het e-mailadres
        user = Users.query.filter_by(email=email).first()

        # Controleer of de gebruiker bestaat
        if user and user.password == password:  # Controleer of het wachtwoord correct is
            session['userid'] = user.userid  # Gebruik de `userid` van de specifieke gebruiker
            return redirect(url_for('main.index'))
        
        # Toon een foutbericht als de gebruiker niet wordt gevonden of het wachtwoord onjuist is
        flash('Ongeldige inloggegevens. Controleer je e-mailadres en wachtwoord.', 'error')
        return redirect(url_for('main.login'))
    
    return render_template('login.html')


@main.route('/logout', methods=['POST', 'GET'])
def logout():
    session.pop('userid', None)
    return redirect(url_for('main.index'))


@main.route('/post', methods=['GET', 'POST'])
def post():
    if 'userid' not in session:
        return redirect(url_for('main.login'))
    
    if request.method == 'POST':

        itinerary_name = request.form['titleofitinerary']  # Ophalen uit HTML
        price = float(request.form['price'])
        description_tekst = request.form['descriptionofitinerary']
        pdf_file = request.files['file']
        if pdf_file and pdf_file.filename.endswith('.pdf'):
            # Beveilig de bestandsnaam
            filename = secure_filename(pdf_file.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"  # Maak een unieke bestandsnaam

            # Upload bestand naar Supabase Storage
            file_data = pdf_file.read()  # Lees de PDF als binary data
            result = supabase.storage.from_("pdf_files").upload(f"pdfs/{unique_filename}", file_data)


            # Haal de publieke URL van het geüploade bestand op
            public_url = supabase.storage.from_("pdf_files").get_public_url(f"pdfs/{unique_filename}")
        else:
            return "Ongeldig bestandstype. Upload een PDF-bestand.", 400

        # Maak een nieuw record in de database
        new_itinerary = DigitalGoods(
            goodid=str(uuid.uuid4()),
            titleofitinerary=itinerary_name,    # Eerste waarde is de naam van je database & de 2e komt van HTML
            descriptionofitinerary=description_tekst,
            userid=session['userid'],
            price=price,
            pdf_url=public_url
        )
        db.session.add(new_itinerary)
        db.session.commit()
        return redirect(url_for('main.reistoegevoegd'))

    return render_template('post.html')

@main.route('/userpage', methods=['GET', 'POST'])
def userpage():
    if 'userid' not in session:
        return redirect(url_for('main.login'))  # Stuur gebruiker naar login als deze niet is ingelogd
    
    user = Users.query.get(session['userid'])  # Haal de huidige gebruiker op
    if not user:
        return redirect(url_for('main.logout'))  # Log gebruiker uit als de gebruiker niet bestaat

    if request.method == 'POST':
        # Haal gegevens uit het formulier
        user.firstname = request.form.get('firstname')
        user.lastname = request.form.get('lastname')
        user.email = request.form.get('email')
        user.phone = request.form.get('phone')
        user.address = request.form.get('address')
        user.city = request.form.get('city')
        user.postalcode = request.form.get('postalcode')
        user.country = request.form.get('country')

        # Sla wijzigingen op in de database
        db.session.commit()

        return redirect(url_for('main.userpage'))  # Refresh de pagina met de nieuwe gegevens

    return render_template('userpage.html', user=user)

@main.route('/change_password', methods=['POST'])
def change_password():
    user = Users.query.filter_by(userid=session['userid']).first()
    
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')

    if not user or not user.check_password(current_password):
        flash('Huidig wachtwoord is onjuist.', 'error')
        return redirect(url_for('main.userpage'))
    
    if new_password != confirm_password:
        flash('Nieuwe wachtwoorden komen niet overeen.', 'error')
        return redirect(url_for('main.userpage'))

    user.set_password(new_password)  # Zorg dat je een methode `set_password` hebt in je User-model
    db.session.commit()
    flash('Wachtwoord succesvol gewijzigd!', 'success')
    return redirect(url_for('main.userpage'))

from flask import Response

@main.route('/download_pdf/<goodid>', methods=['GET'])
def download_pdf(goodid):
    # Haal de reis op uit de database
    reis = DigitalGoods.query.filter_by(goodid=goodid).first()

    if reis:
        # Controleer of een geldige PDF-URL aanwezig is
        if reis.pdf_url:
            pdf_path = reis.pdf_url.split('pdfs/')[1]  # Haal het pad naar de PDF uit de URL
            response = supabase.storage.from_("pdf_files").download(f"pdfs/{pdf_path}")

            if response:
                # Stuur de PDF terug met juiste headers
                return Response(
                    response,
                    mimetype="application/pdf",
                    headers={
                        "Content-Disposition": f"inline; filename={pdf_path}",
                        "Content-Type": "application/pdf"
                    }
                )
        else:
            return "PDF niet gevonden of niet gekoppeld aan deze reis.", 404
    else:
        return "Reis niet gevonden.", 404


@main.route('/gepost', methods=['GET', 'POST'])
def gepost():
    if 'userid' not in session:
        return redirect(url_for('main.login'))  # Verwijzen naar login als gebruiker niet is ingelogd

    user = Users.query.get(session['userid'])  # Huidige gebruiker ophalen
    if not user:
        return redirect(url_for('main.logout'))  # Uitloggen als de gebruiker niet bestaat

    # Geposte reizen van de ingelogde gebruiker ophalen
    geposte_reizen = DigitalGoods.query.filter_by(userid=user.userid).all()

    if request.method == 'POST':
        # Update een specifieke reis
        goodid = request.form.get('goodid')  # ID van het item dat wordt bewerkt
        reis = DigitalGoods.query.filter_by(goodid=goodid, userid=user.userid).first()

        if reis:
            # Gegevens updaten vanuit het formulier
            reis.titleofitinerary = request.form.get('titleofitinerary')
            reis.descriptionofitinerary = request.form.get('descriptionofitinerary')
            reis.price = request.form.get('price')

            db.session.commit()  # Wijzigingen opslaan

            return redirect(url_for('main.gepost'))

    return render_template('gepost.html', user=user, geposte_reizen=geposte_reizen)


@main.route('/gekocht', methods=['GET', 'POST'])
def gekocht():
    if 'userid' not in session:
        return redirect(url_for('main.login'))  # Stuur gebruiker naar login als deze niet is ingelogd
    
    user = Users.query.get(session['userid'])  # Haal de huidige gebruiker op
    if not user:
        return redirect(url_for('main.logout'))  # Log gebruiker uit als de gebruiker niet bestaat

    return render_template('gekocht.html', user=user)

@main.route('/favoriet', methods=['GET', 'POST'])
def favoriet():
    if 'userid' not in session:
        return redirect(url_for('main.login'))  # Stuur gebruiker naar login als deze niet is ingelogd
    
    user = Users.query.get(session['userid'])  # Haal de huidige gebruiker op
    if not user:
        return redirect(url_for('main.logout'))  # Log gebruiker uit als de gebruiker niet bestaat

    return render_template('favoriet.html', user=user)

@main.route('/search', methods=['GET', 'POST'])
def search():
    if 'userid' not in session:
        return redirect(url_for('main.login'))  # Verwijzen naar login als gebruiker niet is ingelogd

    user = Users.query.get(session['userid'])  # Huidige gebruiker ophalen
    if not user:
        return redirect(url_for('main.logout'))
    return render_template('search.html')


@main.route('/verwijder_reis', methods=['POST'])
def verwijder_reis():
    if 'userid' not in session:
        return redirect(url_for('main.login'))

    goodid = request.form.get('goodid')
    reis = DigitalGoods.query.filter_by(goodid=goodid, userid=session['userid']).first()

    if reis:
        db.session.delete(reis)
        db.session.commit()
        return redirect(url_for('main.reisverwijderd'))

    flash('Reis kon niet worden gevonden of verwijderd.', 'error')
    return redirect(url_for('main.gepost'))


@main.route('/reisverwijderd', methods=['GET'])
def reisverwijderd():
    return render_template('reisverwijderd.html')


@main.route('/reistoegevoegd', methods=['GET'])
def reistoegevoegd():
    if 'userid' not in session:
        return redirect(url_for('main.login'))  # Verwijs naar login als gebruiker niet is ingelogd
    
    user = Users.query.get(session['userid'])  # Haal de huidige gebruiker op
    if not user:
        return redirect(url_for('main.logout'))  # Uitloggen als de gebruiker niet bestaat

    return render_template('reistoegevoegd.html', user=user)
