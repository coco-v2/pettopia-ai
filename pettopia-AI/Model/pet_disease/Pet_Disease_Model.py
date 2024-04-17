import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

import Preprocessing.Pet_Data_Encoding as enco
import Preprocessing.Pet_Disease_Data_Parsing as pet_data
import Preprocessing.Pet_Data_Decoding as deco

class Pet_Disease_Model():

    def __init__(self):
        self.pet_disease_data_parsing =  pet_data.Pet_Disease_Data_Parsing
        self.pet_data_encoder = enco.Pet_Data_Encoding
        self.pet_data_decoder = deco.Pet_Data_Decoding


    def pet_disease_recommend(self, ):
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

        pet_features = np.array([breed, age, pet_class, sex, weight, exercise, environment,
                                defecation, food_count, food_amount, snack_amount, food_kind])
        pet_features_weight = pet_features * np.array([weight_breed, weight_age, weight_pet_class, weight_sex, weight_weight, weight_exercise, weight_environment, weight_defecation, weight_food_count, weight_food_amount, weight_snack_amount, weight_food_kind])

        #10:dog, 20:cat
        if species == "10":
            anonymous_data = pd.read_csv('data/dog_data.csv')
        elif species == "20":
            anonymous_data = pd.read_csv('data/cat_data.csv')

        similarity_scores = cosine_similarity([pet_features_weight], anonymous_data['species', 'breed', 'age', 'pet_class', 'sex', 'weight', 'exercise', 'environment', 'defecation', 'food_count', 'food_amount', 'snack_amount', 'food_kind'])
        most_similar_pet_index = np.argmax(similarity_scores)

        print(similarity_scores)
        print(most_similar_pet_index)

    def process_directory(self, directory):


    def preprocess_pet_data(self, data):


#데이터 타입 확인
#pet_disease_recommend(10,"BEA",2,"SH","IM",10.4,1,2,1,1,4,0,1)



