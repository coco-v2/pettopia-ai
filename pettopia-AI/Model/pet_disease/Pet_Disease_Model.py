import numpy as np
import pandas as pd
import os
from sklearn.metrics.pairwise import cosine_similarity

from .Entity import Pet_Disease_Data as pet
from .Preprocessing import Pet_Data_Encoding as enco
from .Preprocessing import Pet_Data_Decoding as deco
from .Preprocessing import Pet_Disease_Data_Parsing as pet_data

class Pet_Disease_Model():

    def __init__(self):
        self.pet_encoding_data = {}
        self.pet_disease_data_parsing =  pet_data.Pet_Disease_Data_Parsing()
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

        pet_features = np.array([breed, age, pet_class, sex, weight, exercise, environment,
                                defecation, food_count, food_amount, snack_amount, food_kind])
        pet_features_weight = pet_features * np.array([weight_breed, weight_age, weight_pet_class, weight_sex, weight_weight, weight_exercise, weight_environment, weight_defecation, weight_food_count, weight_food_amount, weight_snack_amount, weight_food_kind])

        anonymous_data = ""

        #10:dog, 20:cat
        try:
            if species == "10":
                anonymous_data = pd.read_csv('C:/Users/jooho/Documents/GitHub/ettopia-ai/pettopia-AI/Model/pet_disease/data/dog_data_encoding.csv')
            elif species == "20":
                anonymous_data = pd.read_csv('C:/Users/jooho/Documents/GitHub/ettopia-ai/pettopia-AI/Model/pet_disease/data/cat_data_encoding.csv')
        except Exception as e:
            print(f"Failed to load data: {e}")
            anonymous_data = None

        print(type(anonymous_data))
        print(anonymous_data.head())  # DataFrame의 첫 5행을 출력

        similarity_scores = cosine_similarity([pet_features_weight], anonymous_data[[
        'species', 'breed', 'age', 'pet_class', 'sex', 'weight', 'exercise', 'environment', 'defecation', 'food_count', 'food_amount', 'snack_amount', 'food_kind']])
        most_similar_pet_index = np.argmax(similarity_scores)

        print(similarity_scores)
        print(most_similar_pet_index)

    def process_directory(self, directory):
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                pet_data.Pet_Disease_Data_Parsing.data_paring(file_path, root[-3:])

    def preprocess_pet_data(self, data):
        self.pet_encoding_data = self.pet_data_encoder.data_encoding(data)
        print(self.pet_encoding_data)

#데이터 타입 확인
test = Pet_Disease_Model()
data = pet.Pet_Disease_Data("강아지","BEA",2,"SH","IM",10.4,"LOW","IN_DOOR","NORMAL",4,3,1,"FEED")
a = test.preprocess_pet_data(data)
test.pet_disease_recommend()



