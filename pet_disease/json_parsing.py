import json
import os
import csv

def data_paring(path, pet):
    # 파일 열기
    with open(path, encoding='UTF8') as file:
        # JSON 데이터 로드
        data = json.load(file)
        meta = data['metadata']

        # 각 데이터 파싱
        type = meta['type']

        species, mission_id, breed, age, pet_class, sex = id_data_paring(meta)
        disease, disease_name, CRP, IgG, IL_6, AFP = medical_data_paring(meta)
        weight = -1
        exercise = -1
        environment = -1
        defecation = -1
        food_count = -1
        food_amount = -1
        snack_amount = -1
        food_kind = -1
        stress = -1

        if(type == 'B'):
            weight = physical_data_paring(meta)
            exercise, environment, defecation, food_count, food_amount, snack_amount, food_kind = breeding_data_paring(meta)
            stress = vital_data_paring(meta)

        # CSV에 쓸 데이터 리스트로 구성
        pet_data = [species, mission_id, breed, age, pet_class, sex, weight, exercise,
                    environment, defecation, food_count, food_amount, snack_amount, food_kind,
                    disease, disease_name, CRP, IgG, AFP, stress]

        print(path)
        print(pet_data)

        if pet == "반려견":
            with open('data/dog_data.csv', 'a', newline='', encoding='UTF8') as f:
                csv_writer = csv.writer(f)
                csv_writer.writerow(pet_data)
        elif pet == "반려묘":
            with open('data/cat_data.csv', 'a', newline='', encoding='UTF8') as f:
                csv_writer = csv.writer(f)
                csv_writer.writerow(pet_data)

def id_data_paring(meta):
    # 기본 정보 파싱
    id = meta['id']
    species = id["species"]
    mission_id = id["mission-id"]
    breed = id["breed"]
    age = id["age"]
    pet_class = id['class']
    sex = id['sex']
    return species, mission_id, breed, age, pet_class, sex

def physical_data_paring(meta):
    # 신체 데이터 파싱
    physical = meta['physical']
    weight = physical['weight']
    return weight

def breeding_data_paring(meta):
    # 사육 데이터 파싱
    breeding = meta['breeding']
    exercise = breeding['exercise']
    environment = breeding['environment']
    defecation = breeding['defecation']
    food_count = breeding['food-count']
    food_amount = breeding['food-amount']
    snack_amount = breeding['snack-amount']
    food_kind = breeding['food-kind']
    return exercise, environment, defecation, food_count, food_amount, snack_amount, food_kind

def medical_data_paring(meta):
    # 의학 정보 파싱
    medical = meta['medical']
    disease = medical['disease']
    disease_name = None

    if disease == 'ABN':
        disease_name = medical['diseaseName']

    CRP = medical['CRP']
    IgG = medical['lgG']
    IL_6 = medical['IL-6']
    AFP = medical['AFP']

    return disease, disease_name, CRP, IgG, IL_6, AFP

def vital_data_paring(meta):
    vital = meta['vital']
    stress = vital['stress']

    return stress

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            data_paring(file_path, root[-3:])

directory_path = 'C:/Users/jooho/Desktop/petpoia/data/disease_notice/Training/TL_B_반려견'
process_directory(directory_path)

directory_path = 'C:/Users/jooho/Desktop/petpoia/data/disease_notice/Training/TL_B_반려묘'
process_directory(directory_path)

directory_path = 'C:/Users/jooho/Desktop/petpoia/data/disease_notice/Training/02.참조데이터_C_반려견'
process_directory(directory_path)