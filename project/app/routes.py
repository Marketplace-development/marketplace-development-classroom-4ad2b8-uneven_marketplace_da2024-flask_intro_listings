# app/routes.py
import datetime
import uuid
import json
from flask import Blueprint, request, redirect, url_for, render_template, session
from .models import db, Users, DigitalGoods, Gekocht, Favoriet, Feedback
from flask import flash
from werkzeug.utils import secure_filename
from .config import supabase
from supabase import Client
from flask import Response
import requests
from flask import jsonify

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
    user = Users.query.get(session['userid'])  # Huidige gebruiker ophalen
    if not user:
        return redirect(url_for('main.logout'))  # Uitloggen als de gebruiker niet bestaa
    
    error_message = None

    if request.method == 'POST':
        try:
            # Haal formuliergegevens op
            itinerary_name = request.form['titleofitinerary']
            price = float(request.form['price'])
            description_tekst = request.form['descriptionofitinerary']
            pdf_file = request.files['file']
            stad = request.form['start_city']
            image_files = request.files.getlist('images[]')

            # Valideer en upload PDF
            if pdf_file and pdf_file.filename.endswith('.pdf'):
                filename = secure_filename(pdf_file.filename)
                unique_filename = f"{uuid.uuid4()}_{filename}"
                pdf_data = pdf_file.read()
                supabase.storage.from_("pdf_files").upload(f"pdfs/{unique_filename}", pdf_data)
                public_url = supabase.storage.from_("pdf_files").get_public_url(f"pdfs/{unique_filename}")
            else:
                raise ValueError("Ongeldig bestandstype. Upload een PDF-bestand.")

            # Haal coördinaten op voor de startstad
            api_url = f"https://nominatim.openstreetmap.org/search"
            params = {
                'q': stad,
                'format': 'json',
                'limit': 1,
                'accept-language': 'nl'
            }
            headers = {'User-Agent': 'MyApp/1.0 (vermeulen.anna@outlook.be)'}
            try:
                response = requests.get(api_url, params=params, headers=headers)
                response.raise_for_status()
                data = response.json()
                if data and len(data) > 0:
                    latitude = str(data[0]['lat'])
                    longitude = str(data[0]['lon'])
                else:
                    latitude = None
                    longitude = None
            except requests.RequestException as e:
                print(f"Fout bij het ophalen van coördinaten: {e}")
                latitude = None
                longitude = None

            # Valideer en upload afbeeldingen
            image_urls = []
            for image_file in image_files:
                if image_file.filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                    image_filename = secure_filename(image_file.filename)
                    unique_image_filename = f"{uuid.uuid4()}_{image_filename}"
                    image_data = image_file.read()
                    supabase.storage.from_("travel_images").upload(f"images/{unique_image_filename}", image_data)
                    image_public_url = supabase.storage.from_("travel_images").get_public_url(f"images/{unique_image_filename}")
                    image_urls.append(image_public_url)

            # Voeg toe aan database
            new_itinerary = DigitalGoods(
                goodid=str(uuid.uuid4()),
                titleofitinerary=itinerary_name,
                descriptionofitinerary=description_tekst,
                userid=session['userid'],
                price=price,
                pdf_url=public_url,
                image_urls=json.dumps(image_urls),  # Opslaan als JSON string
                start_city=stad,
                latitude=latitude,
                longitude=longitude
            )
            db.session.add(new_itinerary)
            db.session.commit()

            return redirect(url_for('main.reistoegevoegd'))

        except ValueError as ve:
            error_message = str(ve)
        except Exception as e:
            print(f"Error: {e}")
            db.session.rollback()
            error_message = "Er ging iets mis bij het opslaan van de reis."

    return render_template('post.html', error_message=error_message, user = user)

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

    # Geposte reizen van de ingelogde gebruiker ophalen, gesorteerd op nieuwste eerst
    geposte_reizen = DigitalGoods.query.filter_by(userid=user.userid).order_by(DigitalGoods.createdat.desc()).all()

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

@main.route('/download_aankoop_pdf/<gekochtid>', methods=['GET'])
def download_aankoop_pdf(gekochtid):
    # Haal de aankoop op uit de database
    aankoop = Gekocht.query.filter_by(gekochtid=gekochtid).first()

    if aankoop:
        # Verkrijg de gekoppelde `DigitalGoods` via de foreign key `goodid`
        reis = DigitalGoods.query.filter_by(goodid=aankoop.goodid).first()
        if reis and reis.pdf_url:
            # Extract het pad naar de PDF uit de URL
            pdf_path = reis.pdf_url.split('pdfs/')[1]  # Pad achter "pdfs/" verkrijgen
            response = supabase.storage.from_("pdf_files").download(f"pdfs/{pdf_path}")

            if response:
                # Retourneer de PDF met de juiste headers
                return Response(
                    response,
                    mimetype="application/pdf",
                    headers={
                        "Content-Disposition": f"inline; filename={pdf_path}",
                        "Content-Type": "application/pdf"
                    }
                )
        else:
            return "PDF niet gevonden of niet gekoppeld aan deze aankoop.", 404
    else:
        return "Aankoop niet gevonden.", 404

@main.route('/gekocht', methods=['GET'])
def gekocht():
    if 'userid' not in session:
        return redirect(url_for('main.login'))

    user = Users.query.get(session['userid'])
    if not user:
        return redirect(url_for('main.logout'))

    # Haal alle gekochte reizen van de gebruiker op
    gekochte_reizen = Gekocht.query.filter_by(userid=user.userid).all()

    # Voeg eigenaarinformatie toe aan elk gekocht object
    for aankoop in gekochte_reizen:
        aankoop.eigenaar = Users.query.get(aankoop.good.userid)

    return render_template('gekocht.html', user=user, gekochte_reizen=gekochte_reizen)

@main.route('/algekocht')
def algekocht():
    if 'userid' not in session:
        return redirect(url_for('main.login'))  # Verwijs naar login als gebruiker niet is ingelogd
    
    user = Users.query.get(session['userid'])  # Huidige gebruiker ophalen
    if not user:
        return redirect(url_for('main.logout'))  # Uitloggen als de gebruiker niet bestaat

    return render_template('algekocht.html', user=user)

@main.route('/favoriet', methods=['GET'])
def favoriet():
    if 'userid' not in session:
        return redirect(url_for('main.login'))

    user = Users.query.get(session['userid'])
    if not user:
        return redirect(url_for('main.logout'))

    # Haal favorieten op voor de huidige gebruiker
    favorieten = Favoriet.query.filter_by(userid=user.userid).all()

    # Voeg eigenaarinformatie toe aan elk favoriet object
    for favoriet in favorieten:
        favoriet.eigenaar = Users.query.get(favoriet.good.userid)

    return render_template('favoriet.html', user=user, favorieten=favorieten)

@main.route('/search', methods=['GET'])
def search():
    if 'userid' not in session:
        return redirect(url_for('main.login'))

    user = Users.query.get(session['userid'])
    if not user:
        return redirect(url_for('main.logout'))

    zoekterm = request.args.get('zoekterm', '').strip()
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)

    # Haal reizen op en sorteer op createdat (nieuwste eerst)
    reizen = DigitalGoods.query.order_by(DigitalGoods.createdat.desc()).all()

    for reis in reizen:
        reis.user = Users.query.filter_by(userid=reis.userid).first()
        try:
            reis.image_urls = json.loads(reis.image_urls) if reis.image_urls else []
        except json.JSONDecodeError:
            reis.image_urls = []
        
        reis.review_count = Feedback.query.filter_by(targetgoodid=reis.goodid).count()

    # Filter op zoekterm en prijs
    if zoekterm:
        reizen = [reis for reis in reizen if zoekterm.lower() in reis.titleofitinerary.lower()]
    if min_price is not None:
        reizen = [reis for reis in reizen if reis.price >= min_price]
    if max_price is not None:
        reizen = [reis for reis in reizen if reis.price <= max_price]

    favorieten = [favoriet.goodid for favoriet in Favoriet.query.filter_by(userid=session['userid']).all()]

    return render_template(
        'search.html',
        user=user,
        reizen=reizen,
        favorieten=favorieten,
        zoekterm=zoekterm,
        min_price=min_price,
        max_price=max_price
    )


@main.route('/reis/<goodid>', methods=['GET'])
def reisdetail(goodid):
    if 'userid' not in session:
        return redirect(url_for('main.login'))  # Verwijzen naar login als gebruiker niet is ingelogd

    user = Users.query.get(session['userid'])  # Huidige gebruiker ophalen
    if not user:
        return redirect(url_for('main.logout'))  # Uitloggen als de gebruiker niet bestaat

    # Haal de specifieke reis op uit de database
    reis = DigitalGoods.query.filter_by(goodid=goodid).first()

    if not reis:
        flash('Reis niet gevonden.', 'error')
        return redirect(url_for('main.search'))

    # Haal de eigenaar van de reis op
    eigenaar = Users.query.filter_by(userid=reis.userid).first()

    # Controleer of deze reis een favoriet is van de gebruiker
    is_favoriet = Favoriet.query.filter_by(userid=user.userid, goodid=goodid).first() is not None

    # Haal alle reviews voor deze reis op
    reviews = Feedback.query.filter_by(targetgoodid=goodid).all()

    # Voeg het aantal reviews toe
    review_count = len(reviews)

    # Render de template met reisgegevens, reviews, favorietstatus en eigenaar
    return render_template(
        'reisdetail.html',
        reis=reis,
        user=user,
        eigenaar=eigenaar,
        is_favoriet=is_favoriet,
        reviews=reviews,
        review_count=review_count
    )


@main.route('/koop/<goodid>', methods=['POST'])
def koop(goodid):
    if 'userid' not in session:
        return redirect(url_for('main.login'))  # Verwijs naar login als gebruiker niet is ingelogd

    user = Users.query.get(session['userid'])  # Huidige gebruiker ophalen
    if not user:
        return redirect(url_for('main.logout'))  # Uitloggen als de gebruiker niet bestaat

    # Haal de specifieke reis op uit de database
    reis = DigitalGoods.query.filter_by(goodid=goodid).first()
    if not reis:
        flash('Reis niet gevonden.', 'error')
        return redirect(url_for('main.search'))  # Verwijs terug naar de zoekpagina

    # Controleer of deze reis al gekocht is door de gebruiker
    bestaande_aankoop = Gekocht.query.filter_by(userid=user.userid, goodid=goodid).first()
    if bestaande_aankoop:
        flash('Je hebt deze reis al gekocht.', 'info')
        return redirect(url_for('main.algekocht'))  # Verwijs naar de pagina met gekochte reizen

    # Voeg de aankoop toe aan de database
    nieuwe_aankoop = Gekocht(
    gekochtid=str(uuid.uuid4()),  # Unieke ID voor gekochtid
    userid=user.userid,
    goodid=reis.goodid,
    createdat=datetime.datetime.utcnow()  # Dit wordt standaard gebruikt
    )
    db.session.add(nieuwe_aankoop)
    db.session.commit()

    return redirect(url_for('main.koopbevestiging'))

@main.route('/koopbevestiging', methods=['GET'])
def koopbevestiging():
    if 'userid' not in session:
        return redirect(url_for('main.login'))  # Verwijs naar login als gebruiker niet is ingelogd
    
    user = Users.query.get(session['userid'])  # Huidige gebruiker ophalen
    if not user:
        return redirect(url_for('main.logout'))  # Uitloggen als de gebruiker niet bestaat

    return render_template('koopbevestiging.html', user=user)

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

@main.route('/verwijder_aankoop', methods=['POST'])
def verwijder_aankoop():
    if 'userid' not in session:
        return redirect(url_for('main.login'))
    
    user = Users.query.get(session['userid'])  # Haal de huidige gebruiker op
    if not user:
        return redirect(url_for('main.logout'))

    gekochtid = request.form.get('gekochtid')
    aankoop = Gekocht.query.filter_by(gekochtid=gekochtid).first()

    if aankoop and aankoop.userid == session['userid']:
        db.session.delete(aankoop)
        db.session.commit()
        flash('Aankoop succesvol verwijderd.', 'success')
    else:
        flash('Er is iets misgegaan bij het verwijderen.', 'error')

    return render_template('aankoopverwijderd.html')

@main.route('/toggle_favoriet', methods=['POST'])
def toggle_favoriet():
    if 'userid' not in session:
        flash("Je moet ingelogd zijn om een reis als favoriet te markeren of verwijderen.", "error")
        return redirect(url_for('main.login'))

    user_id = session['userid']
    goodid = request.form.get('goodid')
    referer_page = request.form.get('referer')  # Haal de referentiepagina op

    if not goodid:
        flash("Geen geldige reis geselecteerd.", "error")
        return redirect(url_for('main.search'))

    # Controleer of de reis al in de favorieten staat
    favoriet = Favoriet.query.filter_by(userid=user_id, goodid=goodid).first()
    if favoriet:
        # Verwijder de favoriet
        db.session.delete(favoriet)
        db.session.commit()
        flash("Reis verwijderd uit je favorieten.", "info")
    else:
        # Voeg de favoriet toe
        nieuwe_favoriet = Favoriet(
            favorietid=str(uuid.uuid4()),
            userid=user_id,
            goodid=goodid
        )
        db.session.add(nieuwe_favoriet)
        db.session.commit()
        flash("Reis toegevoegd aan je favorieten!", "success")

    # Verwijs terug naar de juiste pagina
    if referer_page == 'search':
        return redirect(url_for('main.search'))
    elif referer_page == 'reisdetail':
        return redirect(url_for('main.reisdetail', goodid=goodid))
    elif referer_page == 'favoriet':
        return redirect(url_for('main.favoriet'))
    else:
        return redirect(url_for('main.search'))  # Fallback naar search

@main.route('/review/<goodid>', methods=['GET'])
def review_page(goodid):
    # Haal de digitale goederen op die overeenkomen met het opgegeven goodid
    reis = DigitalGoods.query.filter_by(goodid=goodid).first()

    # Controleer of de reis bestaat
    if not reis:
        flash('De geselecteerde reis bestaat niet.', 'error')
        return redirect(url_for('main.gekocht'))  # Stuur terug naar de gekocht-pagina
    if 'userid' not in session:
        return redirect(url_for('main.login'))
    
    user = Users.query.get(session['userid'])  # Zorg ervoor dat userid in de sessie zit
    if not user:
        return redirect(url_for('main.login'))
    # Render de review-pagina met de reisdetails
    return render_template('review.html', reis=reis)

@main.route('/submit_review', methods=['POST'])
def submit_review():
    if 'userid' not in session:
        flash("Je moet ingelogd zijn om een reis als favoriet te markeren of verwijderen.", "error")
        return redirect(url_for('main.login'))

    userid = session['userid']
    goodid = request.form.get('goodid')
    review_text = request.form.get('review_text')
    rating = request.form.get('rating')

    # Controleer of alle velden correct zijn ingevuld
    if not (goodid and review_text and rating):
        flash('Alle velden zijn verplicht.', 'danger')
        return redirect(request.referrer)

    # Controleer of de gebruiker deze reis heeft gekocht
    aankoop = Gekocht.query.filter_by(userid=userid, goodid=goodid).first()
    if not aankoop:
        flash('Je kunt alleen een review schrijven voor een gekochte reis.', 'danger')
        return redirect(url_for('main.gekocht'))

    # Controleer of er al een review bestaat voor deze gebruiker en reis
    bestaande_review = Feedback.query.filter_by(userid=userid, targetgoodid=goodid).first()
    if bestaande_review:
        flash('Je hebt al een review geschreven voor deze reis.', 'warning')
        return redirect(url_for('main.gekocht'))

    # Voeg een nieuwe review toe aan de database
    new_feedback = Feedback(
        feedbackid=str(uuid.uuid4()),  # Genereer een unieke ID
        userid=userid,
        targetgoodid=goodid,
        rating=int(rating),
        comment=review_text,
        createdat=datetime.datetime.utcnow()
    )
    db.session.add(new_feedback)
    db.session.commit()

    flash('Review succesvol ingediend!', 'success')
    return redirect(url_for('main.review_bedanking'))

@main.route('/review_bedanking', methods=['GET'])
def review_bedanking():
    return render_template('reviewbedanking.html')

@main.route('/api/travels', methods=['GET'])
def get_travels():
    travels = DigitalGoods.query.all()  # Haal alle reizen op
    travel_list = []

    for travel in travels:
        travel_list.append({
            'id': travel.goodid,
            'titleofitinerary': travel.titleofitinerary,
            'descriptionofitinerary': travel.descriptionofitinerary,
            'latitude': float(travel.latitude) if travel.latitude else None,
            'longitude': float(travel.longitude) if travel.longitude else None
        })

    return jsonify(travel_list)

@main.route('/profile', methods=['GET'])
def profile():
    if 'userid' not in session:
        return redirect(url_for('main.login'))  # Verwijs naar login als gebruiker niet is ingelogd

    # Haal de ingelogde gebruiker op
    user = Users.query.get(session['userid'])
    if not user:
        return redirect(url_for('main.logout'))  # Log uit als de gebruiker niet bestaat

    # Haal de geüploade reizen van de gebruiker op
    reizen = DigitalGoods.query.filter_by(userid=user.userid).all()

    # Render de profielpagina met de gebruiker en reizen
    return render_template('profile.html', user=user, reizen=reizen)

@main.route('/user/<userid>', methods=['GET'])
def user_profile(userid):
    # Zoek de gebruiker op basis van de opgegeven userid
    user = Users.query.get(userid)
    if not user:
        flash("Gebruiker niet gevonden.", "error")
        return redirect(url_for('main.index'))

    # Haal de geüploade reizen van deze gebruiker op
    reizen = DigitalGoods.query.filter_by(userid=user.userid).all()

    # Render de profielpagina met de gegevens van de gebruiker en zijn/haar reizen
    return render_template('profile.html', user=user, reizen=reizen)

@main.route('/boost_reis', methods=['POST'])
def boost_reis():
    if 'userid' not in session:
        return redirect(url_for('main.login'))

    goodid = request.form.get('goodid')
    reis = DigitalGoods.query.filter_by(goodid=goodid, userid=session['userid']).first()

    if reis:
        # Redirect naar de betaalpagina voor het boosten
        return redirect(url_for('main.boost_payment', goodid=goodid))
    else:
        flash('Reis niet gevonden of u heeft geen rechten om deze reis te boosten.', 'error')
        return redirect(url_for('main.gepost'))

@main.route('/boost_payment/<goodid>', methods=['GET', 'POST'])
def boost_payment(goodid):
    if 'userid' not in session:
        return redirect(url_for('main.login'))

    reis = DigitalGoods.query.filter_by(goodid=goodid, userid=session['userid']).first()

    if not reis:
        flash('Reis niet gevonden of u heeft geen rechten om deze reis te boosten.', 'error')
        return redirect(url_for('main.gepost'))

    if request.method == 'POST':
        # Simuleer een succesvolle betaling (voeg hier een echte betaalprovider-integratie toe)
        payment_success = True

        if payment_success:
            # Update de timestamp om de reis als geboost te markeren
            reis.createdat = datetime.datetime.utcnow()
            db.session.commit()
            flash(f'Reis "{reis.titleofitinerary}" is succesvol geboost!', 'success')
            return redirect(url_for('main.gepost'))
        else:
            flash('Betaling mislukt. Probeer het opnieuw.', 'error')
            return redirect(url_for('main.boost_payment', goodid=goodid))

    # Render de betaalpagina
    return render_template('boost_payment.html', reis=reis)


