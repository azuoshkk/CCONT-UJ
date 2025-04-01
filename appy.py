from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3

app = Flask(__name__)
app.secret_key = 'salamemingue'

def connect_db():
    conn = sqlite3.connect("studenty.db")
    return conn
def creat_db():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS studenty(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        semester INTEGER NOT NULL,
                        email TEXT NOT NULL UNIQUE,
                        registration INTEGER NOT NULL UNIQUE,
                        password TEXT NOT NULL
                   )
                   """)
    conn.commit()
    conn.close()

creat_db()

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    conn = sqlite3.connect('studenty.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM studenty where email = ? AND password = ?", (email, password))
    user = cursor.fetchone()

    conn.close()

    if user:
        session['user'] = {
            'id': user[0],
            'name': user[1],
            'email': user[3],
            'registration': user[4],
            'semester': user[2]
        }
        print(f"Email recebido: '{email}'")
        print(f"Senha recebida: '{password}'")
        return jsonify({'redirect': url_for('dashboard')})  # Retorna um JSON com o link da página
    else:
        print(f"Email recebido: '{email}'")
        print(f"Senha recebida: '{password}'")
        return jsonify({'error': 'Wrong email or password'}), 401

@app.route('/dashboard')
def dashboard():
    user = session.get('user')
    if not user:
        return redirect(url_for('index'))  # Se não estiver logado, volta para a página inicial
    return render_template('dashboard.html', **user)

@app.route('/logout')
def logout():
    session.pop('user', None)  # Remove o usuário da sessão
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)