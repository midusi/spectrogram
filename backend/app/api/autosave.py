from email import message
from flask import jsonify, Blueprint, request, current_app as app
import json
import os
from app.helpers.DictPersistJSON import DictPersistJSON

autosave_api = Blueprint("autosave", __name__, url_prefix="/api/autosave")

@autosave_api.put("/")
# Receives the information of an image and saves it in a local file
def save():
    # params
    body = request.get_json()
    img_name = body["name"]
    img_data = body["data"]
    
    # Valid the information received
    # Por ahora no realiza ninguna verificacion
    
    # Save image data in .json files
    full_path = os.path.join(app.static_folder, 'cache')
    if not os.path.exists(full_path):
        os.mkdir(full_path)
    save_path = os.path.join(full_path, img_name+".json")
    db = DictPersistJSON(save_path)
    db["body"] = body
    
    # API response messaje
    message = {
        'message': "success"
    }
    resp = jsonify(message)
    resp.status_code = 200
    return resp