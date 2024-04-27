from flask import Flask, request, jsonify, send_file
import cv2
import numpy as np
import io

from Control import Life_Controller_AI as life

app = Flask(__name__)

@app.route('/pet_filter', methods=['POST'])
def api_pet_filter():
    try:
        img_file = request.files['petImage']
        species = request.form['species']
        filter_nose = request.form['petFilterNose']
        filter_horns = request.form['petFilterHorns']

        img_np = np.frombuffer(img_file.read(), np.uint8)
        img_cv = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

        response = None
        model = life.Life_Controller_AI()

        filter_horns = "/AI/pet_filter/image" + filter_horns
        filter_nose = "/AI/pet_filter/image" + filter_nose

        if species == "강이지":
            response = model.get_dog_filter(img_cv, filter_horns, filter_nose)
        elif species == "고양이":
            response = model.get_cat_filter(img_cv, filter_horns, filter_nose)

        retval, buffer = cv2.imencode('.jpg', response)
        response_bytes = buffer.tobytes()

        return send_file(io.BytesIO(response_bytes), mimetype='image/jpeg')

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
