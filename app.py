from flask import Flask, render_template
from cs50 import SQL
# Conexion a la base de datos
db = SQL('sqlite:///masita.db') 

# Motor del servidor
app = Flask(__name__)

# Ruta principal, crear base html donde se pondran los estilos generales, 
# tener nombres de rutas con respecto a las vistas, usar bootstrap para maquetado 
# https://getbootstrap.com/docs/4.0/components/carousel/

@app.route("/")
def index():
    return render_template("index.html")
    