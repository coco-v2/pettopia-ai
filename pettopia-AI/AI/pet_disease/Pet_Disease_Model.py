import numpy as np
import pandas as pd
import os, ast
from sklearn.metrics.pairwise import cosine_similarity

import sys

sys.path.append('pettopia-AI')
from AI.pet_disease.Entity import Pet_Disease_Data as pet
from AI.pet_disease.Preprocessing import Pet_Data_Encoding as enco
from AI.pet_disease.Preprocessing import Pet_Data_Decoding as deco
from AI.pet_disease.Preprocessing import Pet_Disease_Data_Parsing as pet_data
# from .Entity import Pet_Disease_Data as pet
# from .Preprocessing import Pet_Data_Encoding as enco
# from .Preprocessing import Pet_Data_Decoding as deco
# from .Preprocessing import Pet_Disease_Data_Parsing as pet_data

class Pet_Disease_Model():

    def __init__(self):
        self.pet_encoding_data = {}
        self.pet_disease_data_parsing = pet_data.Pet_Disease_Data_Parsing()
        self.pet_data_encoder = enco.Pet_Data_Encoding()
        self.pet_data_decoder = deco.Pet_Data_Decoding()


    def pet_disease_recommend(self):
        #1~10
        weight_breed = 8
        weight_age = 7
        weight_pet_class = 7
        weight_sex = 7
        weight_weight = 3
        weight_exercise = 8
        weight_environment = 7
        weight_defecation = 9
        weight_food_count = 3
        weight_food_amount = 3
        weight_snack_amount = 5
        weight_food_kind = 5

        species = self.pet_encoding_data.get("species")
        breed = self.pet_encoding_data.get("breed")
        age = self.pet_encoding_data.get("age")
        pet_class = self.pet_encoding_data.get("pet_class")
        sex = self.pet_encoding_data.get("sex")
        weight = self.pet_encoding_data.get("weight")
        exercise = self.pet_encoding_data.get("exercise")
        environment = self.pet_encoding_data.get("environment")
        defecation = self.pet_encoding_data.get("defecation")
        food_count = self.pet_encoding_data.get("food_count")
        food_amount = self.pet_encoding_data.get("food_amount")
        snack_amount = self.pet_encoding_data.get("snack_amount")
        food_kind = self.pet_encoding_data.get("food_kind")

        pet_features = np.array([breed, age, pet_class, sex, weight, exercise, environment, defecation, food_count, food_amount, snack_amount, food_kind])
        pet_features_weight = pet_features * np.array([weight_breed, weight_age, weight_pet_class, weight_sex, weight_weight, weight_exercise, weight_environment, weight_defecation, weight_food_count, weight_food_amount, weight_snack_amount, weight_food_kind])

        anonymous_data = ""

        #10:dog, 20:cat
        try:
            if species == 10:
                anonymous_data_original = pd.read_csv('AI/pet_disease/data/dog_data_encoding.csv', index_col=False)
            elif species == 20:
                anonymous_data_original = pd.read_csv('AI/pet_disease/data/dog_data_encoding.csv', index_col=False)
        except Exception as e:
            print(f"Failed to load data: {e}")
            anonymous_data = None

        if anonymous_data is not None:
            pet_features_weight = pet_features_weight.reshape(1, -1)

            anonymous_data = anonymous_data_original[[
                'breed', 'age', 'pet_class', 'sex', 'weight', 'exercise', 'environment', 'defecation', 'food_count',
                 'food_amount', 'snack_amount', 'food_kind']]

            similarity_scores = cosine_similarity(pet_features_weight, anonymous_data)

            abn_pet_indices = [i for i, pet in enumerate(anonymous_data_original['disease']) if pet == 'ABN']
            abn_similarity_scores = similarity_scores[0][abn_pet_indices]
            most_similar_abn_pet_index = abn_pet_indices[np.argmax(abn_similarity_scores)]

            recommended_abn_pet_df = anonymous_data_original.iloc[most_similar_abn_pet_index].to_frame().transpose()

            return recommended_abn_pet_df

    def process_directory(self, directory):
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                test = pet_data.Pet_Disease_Data_Parsing()
                test.data_paring(file_path, root[-3:])

    def preprocess_pet_data(self, data):
        self.pet_encoding_data = self.pet_data_encoder.data_encoding(data)

#데이터 타입 확인
#test = Pet_Disease_Model()
#data = pet.Pet_Disease_Data("강아지","BEA",2,"SH","IM",10.4,"LOW","IN_DOOR","NORMAL",4,3,1,"FEED")
#a = test.preprocess_pet_data(data)
#est.pet_disease_recommend()



# directory_path = 'C:/Users/jooho/Desktop/petpoia/data/disease_notice/Training/TL_B_반려견'
# test.process_directory(directory_path)
#
# directory_path = 'C:/Users/jooho/Desktop/petpoia/data/disease_notice/Training/TL_B_반려묘'
# test.process_directory(directory_path)
#
# directory_path = 'C:/Users/jooho/Desktop/petpoia/data/disease_notice/Training/02.참조데이터_C_반려견'
# test.process_directory(directory_path)


