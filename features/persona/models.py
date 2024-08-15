from flask_wtf import FlaskForm
from sqlalchemy import Column, Date, Integer, String
from wtforms import DateField, FileField, HiddenField, SelectField, StringField, TextAreaField
from wtforms.validators import DataRequired, Length
from features.core.bd import db

class PersonaForm(FlaskForm):
    id = HiddenField("Id", [], description="")
    nombrecompleto = StringField("*Nombre completo", 
                                [DataRequired(), 
                                 Length(max=100, message="El valor máx. es %(max)d")
                                 ], description= "El nombre es requerido :(")
    fechanacimiento = DateField("*Fecha nac.")
    sexo = SelectField("Sexo",validators=[DataRequired()],
             choices=[("Hombre"), ("Mujer"), ("indefinido")],
             description="Hombre o Mujer o indefinido",
             render_kw={})
    capacidaddiferente = SelectField("Capacidad diferente",validators=[DataRequired()],
            choices=[("No"), ("Si")], render_kw={})
    observaciones = TextAreaField ("Datos de contacto (Tel., cel., correo, domicilio, otros)", validators=[Length(max=250)], description="Long.Max.:250")
    user_id = SelectField("Cuenta de usuario", 
                          choices=[("Elija una opción")],
            validate_choice=False, description=('Seleccione una opcion'), render_kw={})


class PersonaFileForm(FlaskForm):
    id = HiddenField("Id", [DataRequired()], description="")
    file = FileField("*Frente")


class Persona (db.Model):
    """Clase model que se mapea con la tabla de BD correspondiente"""
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombrecompleto = Column(String(100), nullable=False)
    fechanacimiento = Column(Date, nullable=False)
    sexo = Column(String(10), nullable=False)
    capacidaddiferente = Column(String(10), nullable=True)
    observaciones = Column(String(250), nullable=True)
    credencialfrente = Column(String(100), nullable=True)
    credencialreverso = Column(String(100), nullable=True)
    user_id = Column(Integer, index=True, nullable=True)

      # def __init__(self, nombrecompleto, fechanacimiento, sexo, capacidaddiferente, observaciones) -> None:
    #     self.nombrecompleto = nombrecompleto
    #     self.fechanacimiento = fechanacimiento
    #     self.sexo = sexo
    #     self.capacidaddiferente = capacidaddiferente
    #     self.observaciones = observaciones

    def get_data(self):
        return {'id':self.id, 
                'nombrecompleto': self.nombrecompleto, 
                'fechanacimiento': self.fechanacimiento,
                'sexo': self.sexo,
                'capacidaddiferente': self.capacidaddiferente,
                'observaciones': self.observaciones,
                'user_id': self.user_id,
                'credencialfrente': self.credencialfrente,
                'credencialreverso': self.credencialreverso,
                }