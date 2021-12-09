from flask import Flask, flash, render_template, request, session
from cs50 import SQL
from helpers import *
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
import json
# Conexion a la base de datos
db = SQL('sqlite:///masita.db')

# Motor del servidor
app = Flask(__name__)

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Ruta principal, crear base html donde se pondran los estilos generales,
# tener nombres de rutas con respecto a las vistas, usar bootstrap para maquetado
# https://getbootstrap.com/docs/4.0/components/carousel/
# BARRA DE PROGRESO (? https://codepen.io/jenning/pen/bQvqMm Y https://codepen.io/peruvianidol/pen/NLMvqO)
# BOTON DE ¿ESTAS LISTO? https://codepen.io/abdelrhmansaid/pen/OJRNOpQ | https://codepen.io/Unleashed-Design/pen/gOrEvMV | https://codepen.io/robsonvinicius/pen/bGpKQrw


@app.route("/")
def index():

    # https://codepen.io/jhancock532/pen/GRZrLwY

    # Query database for email
    rows = db.execute("SELECT * FROM users WHERE email = :email",
                      email=request.form.get("email"))

    # Ensure username exists and password is correct
    # if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
        # BLOQUEAR EL POST

    # Remember which has logged in
    # session["user_id"] = rows[0]["id"]
    return render_template("index.html")

@login_required
@app.route("/bases")
def bases():

    if not session.get("user_id"):
        return render_template("login.html"), 403
    return "Estas en las bases"

@app.route("/operaciones")
def operaciones():

    if not session.get("user_id"):
        return render_template("login.html"), 403
    return "Operaciones unitarias"

@login_required
@app.route("/clasificacion")
def clasificacion():

    if not session.get("user_id"):
        return render_template("login.html"), 403
    return "Clasificacion operaciones"

# LOGIN

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure email was submitted
        if not request.form.get("email"):
            return apology("must provide email", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for email
        rows = db.execute("SELECT * FROM users WHERE email = :email",
                          email=request.form.get("email"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("register.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return render_template("index.html")
        flash("¡Felicidades! Te has registrado")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

# LOGOUT

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

# CHANGE PASSWORD

@app.route("/changepassword", methods=["GET", "POST"])
def changepassword():
    if request.method == "POST":
        # La copia de aca es de register
        originalpassword = request.form.get("original")
        if not originalpassword:
            return apology("must provide actual password", 400)

        # Submit password  HASH
        newpassword = request.form.get("password")
        if not newpassword:
            return apology("must provide new password", 400)
        # Verify password
        confirm = request.form.get("confirmation")
        if not confirm:
            return apology("verify password", 400)

        if newpassword != confirm:
            return apology("wrong password", 400)

        # Se solicita la contraseña original a la base de datos
        hashes = db.execute("SELECT hash FROM users WHERE id=:y", y=session["user_id"])
        if not check_password_hash(hashes[0]["hash"], originalpassword):
            return apology("wrong password", 400)
        db.execute("UPDATE users SET hash=:contra WHERE id=:cosa",
                   contra=generate_password_hash(newpassword), cosa=session["user_id"])
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("changepassword.html")

# REGISTER

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Create

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Submit a name
        nameprueba = request.form.get("name")
        if not nameprueba:
            return apology("Ingrese su nombre", 400)
            flash("Ingrese su nombre")

        # Submit a last name
        apellidoprueba = request.form.get("apellido")
        if not apellidoprueba:
            return apology("Ingrese su nombre", 400)
            flash("Ingrese su apellido")

        # Submit a username
        usernameprueba = request.form.get("username")
        if not usernameprueba:
            return apology("Ingrese su nombre", 400)
            flash("Ingrese nombre de usuario")

        # Submit an email
        emailprueba = request.form.get("email")
        if not emailprueba:
            return apology("Ingrese su nombre", 400)
            flash("Ingrese email")

        # Submit password  HASH
        password = request.form.get("password")
        if not password:
            return apology("Ingrese su nombre", 400)
            flash("Ingrese contraseña")
        # Verify password
        ver_password = request.form.get("confirmation")

        # Query database for email
        if password == ver_password:
            try:
                rows = db.execute("INSERT INTO users (name, apellido, email, username, hash) VALUES (:name, :apellido, :email, :username, :hash)",
                                  name=nameprueba, apellido=apellidoprueba, email=emailprueba, username=usernameprueba, hash=generate_password_hash(password))
                print("Insercion lista")
            except:
                # return redirect(url_for('register'))
                return apology("Ingrese su nombre", 400)
                flash("¡El correo ya existe!")
            # Redirect user to home page
            session["user_id"] = rows
            return render_template("index.html")
            flash("¡Felicidades! Te has registrado")
        else:
            return apology("Ingrese su nombre", 400)
            flash("las contraseñas no coinciden")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")
        print("Hola")

@app.route("/prueba")
def prueba():
    return render_template("absorcion.html")

@app.route("/ejercicios")
def ejercicios():
    numero_ejercicio = request.args.get("no")
    ejercicio = db.execute("SELECT * FROM ejercicios WHERE id=:id_ejercicios", id_ejercicios=numero_ejercicio)[0]
    campos = ejercicio["seleccion"]
    campos = json.loads(campos)
    listado_campos = []
    for i in campos:
        temporal = campos[i]
        listado_campos.append(temporal)
    print(ejercicio)
    return render_template("ejercicios.html", dato=ejercicio, a=listado_campos[0], b=listado_campos[1], c=listado_campos[2])


# RESPETAR EL A, B, C PARA QUE NO SE ROMPA
# PARA ACCEDER A CADA EJERCICIO ejercicios?no=1