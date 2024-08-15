import datetime
import os
from flask import Blueprint, redirect, render_template, url_for, Response, jsonify, request, send_from_directory
# from flask_jwt_extended import current_user, jwt_required
from features.core.projectdefs import getPageDataRequested, response_bad_request, getUploadsPathBase
from features.persona.models import PersonaFileForm, PersonaForm
#from features.persona.ucases_or_services import PersonaCU
from werkzeug.utils import secure_filename

from features.persona.ucases_or_services import PersonaCU

# Rutas o EndPoints compuestas con el prefijo referente a la feature actual (user)
app = Blueprint('PersonaAPIs', __name__, url_prefix='/personas')

@app.route("/")
def get_persona():
    obj_form = PersonaForm()
    context = {"obj_form": obj_form}
    return render_template("personas.html", **context)

@app.post('/api/add')
# @jwt_required()
def api_persona_add():
    try:
        # if current_user.tipo != "2":
        #     return {'errormsg': 'Acceso Restringido' }
        obj_form = PersonaForm()
        if obj_form.validate_on_submit():
            objCU = PersonaCU()
            resp = objCU.save(obj_form)
            if resp and resp['obj']:
                return jsonify( {'success': 'ok', 'data':resp['obj'] } )
            else:
                return {'errormsg': 'La persona ya se encuentra registrada' }
        else:
            return {'errors': obj_form.errors }
    except (BaseException) as err:
        return response_bad_request(err)

@app.get('/api/get')
# @jwt_required()
def personas_get():
    try:
        # if current_user.tipo != "2":
        #     return {'errormsg': 'Acceso Restringido' }
        personacu = PersonaCU()
        # Obtener el id
        data = dict(request.args)
        id = data.get("id")
        # Obtener los registros y retornarlos
        registros = personacu.get_registros(id)
        return jsonify ( {'data':registros} )
    except (BaseException) as err:
        return response_bad_request(err)

@app.delete('/api/delete')
# @jwt_required()
def persona_delete():
    try:
        # if current_user.tipo != "2":
        #     return {'errormsg': 'Acceso Restringido' }
        objcu = PersonaCU()
        obj_form = PersonaForm()
        print (obj_form)
        print (obj_form.id.data)
        return jsonify ( {'data': objcu.delete(obj_form.id.data)} )
    except (BaseException) as err:
        return response_bad_request(err)