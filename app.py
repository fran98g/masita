from flask import Flask, render_template, request, session
from cs50 import SQL
from helpers import login_required
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
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

@app.route("/")
def index():
    return render_template("index.html")

# REPETIR LO QUE SE HIZO EN OPERACIONES EN LAS OTRAS DOS RUTAS BASES Y CLASIFICACION, CREAR LAS PLANTILLAS HTML PARA LAS TRES OPCIONES

@login_required
@app.route("/bases")
def bases():
    if not session.get("user_id"):
        return render_template("login.html")
    return "Estas en la base"

@app.route("/operaciones")
def operaciones():
    if not session.get("user_id"):
        return render_template("login.html")
    return "Operaciones unitarias"

@login_required
@app.route("/clasificacion")
def clasificacion():
    if not session.get("user_id"):
        return render_template("login.html")
    return "Clasificacion operaciones"

# LOS ID DE LAS IMAGENES DEBERAN TENER EL MISMO NOMBRE DE RUTAS~


# LOGIN

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

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

        # Submit a username
        username = request.form.get("username")
        if not username:
            return apology("must provide username", 400)

        # Submit password  HASH
        password = request.form.get("password")
        if not password:
            return apology("must provide password",)
        # Verify password
        ver_password = request.form.get("confirmation")

        # Query database for username
        if password == ver_password:
            try:
                rows = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)",
                                  username=username, hash=generate_password_hash(password, salt_length=8))
                session["user_id"] = rows
            except:
                return apology("¡El usuario ya existe!", 400)
            # Redirect user to home page
            return redirect("/")

        else:
            return apology("your password doesn't match", 400)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

