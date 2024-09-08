from flask import Flask, render_template, redirect, url_for, request, flash, session
from werkzeug.security import check_password_hash as checkph
from werkzeug.security import generate_password_hash as genph

import db

app = Flask(__name__)
app.secret_key = 'clave-secreta'

@app.before_request
def antes_de_todo():
    ruta = request.path
    if not 'usuario' in session and ruta!= '/entrar' and ruta!= '/login' and ruta!= '/salir' and ruta!= '/registro':
        flash('Necesitas iniciar sesión para acceder a esta página', 'error')
        return redirect('/entrar')

@app.route('/dentro')
def dentro():
    return render_template('index.html')

@app.route('/')
@app.route('/entrar')
def entrar():
    return render_template('entrar.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    contraseña = request.form['contraseña']
    try:
        usuario = db.obtener_usuario(email)
    except Exception as e:
        flash('Error al iniciar sesión', 'error')
    if usuario:
        if (checkph(usuario[1], contraseña)):
            session['usuario'] = email
            return redirect('/dentro')
        else:
            flash('Acceso denegado', 'error')
            return redirect('/entrar')
    return redirect('/entrar')
        
@app.route('/salir')
def salir():
    session.pop('usuario', None)
    flash('Sesión cerrada','success')
    return redirect('/entrar')

@app.route("/registro")
def registro():
    return render_template("registro.html")

@app.route("/registrar", methods=['POST'])
def registrar():
    email = request.form['email']
    contraseña = request.form['contraseña']
    contraseña = genph(contraseña)
    try: 
        db.alta_usuario(email, contraseña)
        flash('Usuario registrado correctamente','success')
    except Exception as e:
        flash('Error al registrar usuario', 'error')
    finally:
        return redirect("/entrar")

if __name__ == '__main__':
    app.run(debug=True)