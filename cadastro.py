from flask import Blueprint, request, render_template, redirect, url_for, jsonify
import sqlite3

#criar um blueprint para separara o cadastro do resto do código
cadastro_bp = Blueprint('cadastro',__name__)

def connect_db():
    return sqlite3.connect("studenty.db")

def create_db():
    conn = sqlite3.connect("studenty.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS studenty (
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

create_db()

@cadastro_bp.route('/register', methods = ['GET'])
def register_page():
    return render_template('register.html')

@cadastro_bp.route('/register', methods=['POST'])
def registration():
    name = request.form.get('name')
    semester = request.form.get('semester')
    email = request.form.get('email')
    registration = request.form.get('registration')
    password = request.form.get('password')
    if not name or not email or not registration or not semester or not password:
        return jsonify({'error': 'Todos os campos são obrigatórios'}), 400
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO studenty (name, email, registration, semester, password) VALUES (?, ?, ?, ?, ?)",
                       (name, email, registration, semester, password))
        conn.commit()
        conn.close()
        return redirect(url_for('cadastro.register_page'))  # Redireciona para a página de cadastro
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Email ou matrícula já cadastrados!'}), 409