from flask import request, jsonify, current_app as app
import os
import base64
import cv2
from app.helpers.DictPersistJSON import DictPersistJSON

def api_get_img():

    dir_path = request.values["dir_path"]
    img_name = request.values["img_name"]
    
    # It checks if there is information saved for that image and 
    # if it exists, it returns its data
    cache_path = os.path.join(app.static_folder, 'cache', img_name+".json")
    
    if (os.path.isfile(cache_path)):
        data = {}
        data = DictPersistJSON(cache_path)["body"]["data"]
        
        # API response messaje
        resp = jsonify(data)
        resp.status_code = 200
    
    # In case there is no saved information of that image
    else:
        filename = os.path.join(dir_path, img_name)
        img_info = cv2.imread(filename, -1)
        img = cv2.imread(filename)

        original_dtype = img_info.dtype
        original_height, original_width, _ = img.shape

        if not (img_name.split(sep='.')[-1] == 'png'):
            if((original_width < original_height)):
                img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
            original_height, original_width, _ = img.shape 
            filename = os.path.join(dir_path, app.config['PNG_FOLDER'], img_name+'.jpg')
            if not os.path.exists(os.path.join(dir_path, app.config['PNG_FOLDER'])):
                os.mkdir(os.path.join(dir_path, app.config['PNG_FOLDER']))
            cv2.imwrite(filename, img, [cv2.IMWRITE_JPEG_QUALITY, 50])    
        
        with open(filename, "rb") as f:
            image_binary = f.read()
        
        image = base64.b64encode(image_binary).decode("utf-8")
        # API response messaje
        data = {
            'status': True,
            'image': image,
            'info': {
                'width': original_width,
                'heigth': original_height,
                "name": img_name.split(sep=".")[0],
                "ext": img_name.split(sep=".")[-1],
                "path":os.path.join(dir_path, img_name),
                "dtype": str(original_dtype)
            }
        }
        resp = jsonify(data)
        resp.status_code = 200
    
    return resp