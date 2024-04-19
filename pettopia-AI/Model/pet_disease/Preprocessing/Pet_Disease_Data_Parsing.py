import json
import pandas as pd
import csv

class Pet_Disease_Data_Parsing():

    def data_paring(self, path, species):
        # 파일 열기
        with open(path, encoding='UTF8') as file:
            # JSON 데이터 로드
            data = json.load(file)
            meta = data['metadata']

            # 각 데이터 파싱
            type = meta['type']

            pet_species, mission_id, breed, age, pet_class, sex = self.id_data_paring(meta)
            disease, disease_name, CRP, IgG, IL_6, AFP = self.medical_data_paring(meta)
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
                weight = self.physical_data_paring(meta)
                exercise, environment, defecation, food_count, food_amount, snack_amount, food_kind = self.breeding_data_paring(meta)
                stress = self.vital_data_paring(meta)

            pet_data = [pet_species, mission_id, breed, age, pet_class, sex, weight, exercise,
                        environment, defecation, food_count, food_amount, snack_amount, food_kind,
                        disease, disease_name, CRP, IgG, AFP, stress]

            df = pd.DataFrame([pet_data],
                              columns=['pet_species', 'mission_id', 'breed', 'age', 'pet_class', 'sex', 'weight', 'exercise',
                                       'environment', 'defecation', 'food_count', 'food_amount', 'snack_amount', 'food_kind',
                                       'disease', 'disease_name', 'CRP', 'IgG', 'AFP', 'stress'])

            if species == "반려견":
                df.to_csv('pet_disease/data/dog_data.csv', mode='a', header=False, index=False, encoding='UTF8')
            elif species == "반려묘":
                df.to_csv('pet_disease/data/cat_data.csv', mode='a', header=False, index=False, encoding='UTF8')

    def id_data_paring(self, meta):
        # 기본 정보 파싱
        id = meta['id']
        species = id["species"]
        mission_id = id["mission-id"]
        breed = id["breed"]
        age = id["age"]
        pet_class = id['class']
        sex = id['sex']
        return species, mission_id, breed, age, pet_class, sex

    def physical_data_paring(self, meta):
        # 신체 데이터 파싱
        physical = meta['physical']
        weight = physical['weight']
        return weight

    def breeding_data_paring(self, meta):
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

    def medical_data_paring(self, meta):
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

    def vital_data_paring(self, meta):
        vital = meta['vital']
        stress = vital['stress']

        return stress

