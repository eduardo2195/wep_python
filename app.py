import os
import uuid
from dotenv import load_dotenv
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
import pymysql

from features.persona.models import Persona
pymysql.install_as_MySQLdb()

app = Flask(__name__)

from features.core.auth.model import LoginForm, User
from features.persona.routes_backend import app as app_persona
app.register_blueprint(app_persona)


basedir = os.path.abspath( os.path.dirname(__file__) )
load_dotenv( os.path.join(basedir, ".env") )
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
# db = SQLAlchemy(app)
from features.core.bd import db
db.init_app(app)
csrf = CSRFProtect(app)

@app.route("/nombre", methods=["POST"])
def get_nombre():
    return "Armando"

@app.route("/")
def get_index():
    return render_template("index.html")

# @app.route("/personas")
# def get_personas():
#     return render_template("personas.html")

def create_user(username_given, email, full_name, passwd, public_id, tipo):
    user: User = db.session.query(User).filter_by(username=username_given).first()
    if user == None:
        user = User(username_given, email, full_name, passwd, public_id, tipo)
        user.encrypt_password()
        db.session.add(user)
        db.session.commit()
    per: Persona = db.session.query(Persona).filter_by(nombrecompleto=username_given).first()
    if per == None:
        objPersona = Persona(username_given, "1990-01-01", "Mujer", "No", "")
        db.session.add(objPersona)
        db.session.commit()

with app.app_context():
    try:
        db.create_all()
        create_user("admin", "admin@gmail.com", "Armando", "123456", str(uuid.uuid4()), "2" ) # 2 = Admin
    except (BaseException) as err:
        print(err.__dict__)

if __name__ == "__main__":
    app.run(debug=True)

