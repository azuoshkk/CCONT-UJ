from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
#inicializa a aplicação Flask //  Start the Flask aplication
app = Flask(__name__)# Instancia da framework para saber o modulo atual // Framework instance to know the current module
# Define a chave secreta do app(usada para assinar cookies e proteger seções) // Sets the app's secret key(used to sign cookies and secure sessions)
app.secret_key = 'salamemingue' # Em produção, use uma váriavel de ambiente para proteger essa chave // In producion, use an environment variable to secure this key


# Função para conectar ao banco de dados(db) // Functiopn to connect to the database(db)
def connect_db():
    conn = sqlite3.connect("studenty.db")
    return conn
# Função para criar um db caso n exista // Function to creat an db if not exists
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

# Define rota principal do app // Define the main route of the app 
# Quando o usuario acessar a rota base ('/'), a função será chamada //  When the user access the basic route ('/'), the function will be called
@app.route('/')
def index():
    # renderiza e retorna o "index.html"(pagina principal) //  renders and return the "index.html"(main page)
    return render_template('index.html')

# Define a rota para o endpoint de login //  Sets the route to the login endpoint
# Esse endpoint aceita apenas requisições do tipo "POST", que normalmente é utilizada para envio de dados de login // This endpoint only accepted "POST" type request, which are typically used to send login data
@app.route('/login', methods=['POST'])
def login():
    # Define o valor da variavel email e password usando uma função para pegar um input do usuario. // Sets the value of email and pasword variables using using an fuction to get the user input
    # Procura o input pela definição de name em cada um //  Search the input by the name definition in each
    email = request.form.get('email')
    password = request.form.get('password')
     

    # Conecta ao db e cria um cursor //  Connect to the db and create a cursor
    conn = sqlite3.connect('studenty.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM studenty where email = ? AND password = ?", (email, password)) # Procura no db uma linha que possua um email e uma senha igual ao input //  Search in the db for an line that has an email and password equal to the input
    user = cursor.fetchone() # Função usando cursor para obter a linha que foi pesquisada //  Function using the cursor to get the line that was searched

    conn.close() # Fecha a conexão com o db // Close the db connection

    if user: # Verifica se a variável user não está vazia ou é None // Verify if the user variable is not empty or is none
        # Armazena os dados de usuarios na sessão Flask // Stores the user data in the Flask session
        # isso permite manter o usuario autenticado durante a navegação do site // This allow the user to remain authenticated while browsing the site
        session['user'] = {
            # Formata como um dicionario para facilitar o trabalho // Formatted like a dictionary to make the work easier
            # Nome para o dicionario : Numero da tabela que deve ser procurada
            'id': user[0],           # ID único do usuário no banco de dados // Unique user ID in the db
            'name': user[1],         # Nome do usuário // User name
            'semester': user[2],     # Semestre atual do usuário // User's corrent semester
            'email': user[3],        # E-mail do usuário // User email
            'registration': user[4]  # Número de matrícula // Number registration
        }
        print(f"Email recebido: '{email}'")
        print(f"Senha recebida: '{password}'")
        return jsonify({'redirect': url_for('dashboard')})  # Retorna um JSON com o link da página
    else:
        print(f"Email recebido: '{email}'")
        print(f"Senha recebida: '{password}'")
        return jsonify({'error': 'Wrong email or password'}), 401

@app.route('/dashboard') # Define a rota '/dashboard' // Sets the "/dashboard" route
def dashboard():
    user = session.get('user') # Obtém os dados do usuário armazenados na sessão // Gets the user data stored in the section
    if not user: # Se não estiver logado, volta para a página inicial // If you are not logged in, returno to the main page
        return redirect(url_for('index')) # Redireciona para a página principal // Redirect to the main page 
    return render_template('dashboard.html', **user) # Renderiza a dashboard, passando os dados de "user" // Render the dashboard, passing the "user" data

@app.route('/logout') # Define a rota "logout" // Sets the "logout" route
def logout():
    session.pop('user', None)  # Remove os dados do usuario(se existir) // Delete the user data(if exists) 
    return redirect(url_for('index')) # Redireciona para a pagina inicial // Redirect to the main page

# Esse bloco garante que o servidor Flask só será iniciado se o script for executado diretamente // This block ensures that the serve will only turn on if the script is triggered directly 
if __name__ == '__main__':
    app.run(debug=True) # Inicia o servidor Flask no modo dubg