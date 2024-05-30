from flask import Flask, request, jsonify, send_file, Response
import numpy as np
import io, sys, json, cv2

sys.path.append('pettopia-AI')
from Control import Medical_Controller_AI as med
from Control import Life_Controller_AI as life
from Control import Beauty_Controller_AI as beauty

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def test():
    return '펫토피아'

@app.route('/pet_color', methods=['POST'])
def api_pet_color():
    try:
        img_file = request.files['petImage']

        img_np = np.frombuffer(img_file.read(), np.uint8)
        img_cv = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

        model = beauty.Beauty_Controller_AI()

        response = model.get_pet_color(img_cv)

        response_dict = {'response': response}

        return Response(response=json.dumps(response_dict, ensure_ascii=False).encode('utf-8'),
                    content_type='application/json; charset=utf-8')

    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/pet_filter', methods=['POST'])
def api_pet_filter():
    try:
        img_file = request.files['petImage']
        species = request.form['species']
        filter_nose = request.form['petFilterNose']
        filter_horns = request.form['petFilterHorns']
        cat_filter = request.form['petFilterCat']

        img_np = np.frombuffer(img_file.read(), np.uint8)
        img_cv = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

        response = None
        model = life.Life_Controller_AI()

        if species == "강이지":
            filter_horns = "AI/pet_filter/dog/image/horns_img" + filter_horns + ".png"
            filter_nose = "AI/pet_filter/dog/image/nose_img" + filter_nose + ".png"
            response = model.get_dog_filter(img_cv, filter_horns, filter_nose)
        elif species == "고양이":
            filter_img = "AI/pet_filter/cat/image/filter_img" + cat_filter + ".png"
            response = model.get_cat_filter(img_cv, filter_img)

        retval, buffer = cv2.imencode('.jpg', response)
        response_bytes = buffer.tobytes()

        return send_file(io.BytesIO(response_bytes), mimetype='image/jpeg')

    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/PetDiseaseRecommend', methods=['POST'])
def api_sentence_generation():
    try:
        data = request.get_json()
        species = data.get('species')
        breed = data.get('breed')
        age = data.get('age')
        pet_class = data.get('pet_class')
        sex = data.get('sex')
        weight = data.get('weight')
        exercise = data.get('exercise')
        environment = data.get('environment')
        defecation = data.get('defecation')
        food_count = data.get('food_count')
        food_amount = data.get('food_amount')
        snack_amount = data.get('snack_amount')
        food_kind = data.get('food_kind')

        model = med.Medical_Controller_AI()

        response_array = model.get_pet_disease(species, breed, age, pet_class, sex, weight, exercise, environment, defecation, food_count, food_amount, snack_amount, food_kind)
        response_dict = {'response': response_array}
        return Response(response=json.dumps(response_dict, ensure_ascii=False).encode('utf-8'),
                        content_type='application/json; charset=utf-8')
    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)