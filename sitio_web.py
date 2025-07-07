from flask import Flask, request, jsonify
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('usuarios.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return "Bienvenido al sitio web del Examen Transversal"

@app.route('/registrar', methods=['POST'])
def registrar():
    nombre = request.form.get('nombre')
    password = request.form.get('password')
    if not nombre or not password:
        return jsonify({"error": "Faltan datos"}), 400
    hashed_password = generate_password_hash(password)
    conn = sqlite3.connect('usuarios.db')
    c = conn.cursor()
    c.execute('INSERT INTO usuarios (nombre, password) VALUES (?, ?)', (nombre, hashed_password))
    conn.commit()
    conn.close()
    return jsonify({"mensaje": f"Usuario {nombre} registrado correctamente"})

@app.route('/validar', methods=['POST'])
def validar():
    nombre = request.form.get('nombre')
    password = request.form.get('password')
    conn = sqlite3.connect('usuarios.db')
    c = conn.cursor()
    c.execute('SELECT password FROM usuarios WHERE nombre = ?', (nombre,))
    resultado = c.fetchone()
    conn.close()
    if resultado and check_password_hash(resultado[0], password):
        return jsonify({"mensaje": "Usuario validado correctamente"})
    else:
        return jsonify({"mensaje": "Credenciales incorrectas"}), 401

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5800, debug=True)