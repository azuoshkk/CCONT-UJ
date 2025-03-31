from flask import Flask, render_template, request
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
        print(f"Email recebido: '{email}'")
        print(f"Senha recebida: '{password}'")

        return "Sucefful login"
    else:
        print(f"Email recebido: '{email}'")
        print(f"Senha recebida: '{password}'")

        return "wrong email or password"
    
if __name__ == '__main__':
    app.run(debug=True)