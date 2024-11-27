from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def login():
    return '''
    <!DOCTYPE html>
    <html lang="nl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Inloggen</title>
        <style>
            body {
                font-family: 'Georgia', serif;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), 
                            url('/static/images/forest_background.jpg') no-repeat center center;
                background-size: cover;
                color: #ffffff;
            }
            .container {
                text-align: center;
                max-width: 400px;
                width: 100%;
            }
            h1 {
                font-size: 46px;
                font-weight: bold;
                margin-bottom: 10px;
            }
            p.welcome-text {
                font-size: 16px;
                margin-bottom: 30px;
                line-height: 1.5;
            }
            form {
                text-align: left;
            }
            label {
                display: block;
                margin-top: 17px;
                font-size: 14px;
                font-weight: bold;
                color: #ffffff;
            }
            input {
                display: block;
                width: 100%;
                padding: 10px;
                margin-top: 5px;
                border: none;
                border-bottom: 2px solid #ffffff;
                background: transparent;
                color: #ffffff;
                font-size: 16px;
            }
            input:focus {
                outline: none;
                border-bottom: 2px solid #4caf50;
            }
            button {
                margin-top: 30px;
                width: 100%;
                padding: 15px;
                border: none;
                border-radius: 25px;
                background-color: #ffffff;
                color: #1f3d2b;
                font-size: 18px;
                font-weight: bold;
                cursor: pointer;
                transition: transform 0.2s ease, background-color 0.2s ease;
            }
            button:hover {
                transform: scale(1.02);
                background-color: #e0e0e0;
            }
            .footer {
                margin-top: 20px;
                font-size: 14px;
                color: #ffffff;
            }
            .footer a {
                color: #ffffff;
                text-decoration: underline;
            }
            .footer a:hover {
                color: #4caf50;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Inloggen</h1>
            <p class="welcome-text">Welkom bij Travel Tales! Log in om je reisverhalen te delen en inspiratie op te doen!</p>
            <form method="post" action="/login">
                <label for="username">Gebruikersnaam</label>
                <input type="text" id="username" name="username" placeholder="Voer je gebruikersnaam in" required>

                <label for="password">Wachtwoord</label>
                <input type="password" id="password" name="password" placeholder="Voer je wachtwoord in" required>

                <button type="submit">Inloggen</button>
            </form>
            <div class="footer">
                <p>Wachtwoord vergeten? <a href="/forgot-password">Klik hier</a></p>
                <p>Nog geen account? <a href="/register">Registreer hier</a></p>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/register')
def register():
    return '''
    <h1>Registreer Pagina</h1>
    <p>Hier komt de registreer functionaliteit!</p>
    '''

@app.route('/login', methods=['POST'])
def handle_login():
    username = request.form.get('username')
    password = request.form.get('password')
    # Voeg logica toe voor het controleren van gebruikers
    if username == "admin" and password == "password":  # Dummy validatie
        return f"Welkom, {username}!"
    else:
        return "Onjuiste inloggegevens, probeer het opnieuw."

@app.route('/forgot-password')
def forgot_password():
    return '''
    <h1>Wachtwoord Vergeten</h1>
    <p>Hier kun je je wachtwoord herstellen!</p>
    '''

if __name__ == '__main__':
    app.run(debug=True)
