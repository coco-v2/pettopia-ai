from ..Enum import Dog_Breed, Cat_Breed, Pet_Class, Sex, Exercise, Environment, Defecation, Food_Count, Food_Kind
from ..Entity import Pet_Disease_Data

import pandas as pd

class Pet_Data_Encoding():

    def __init__(self):
        self.__cat_data_file = "pet_disease/data/cat_data.csv"
        self.__dog_data_file = "pet_disease/data/dog_data.csv"

        self.__dog_encoding_file = "pet_disease/data/dog_data_encoding.csv"
        self.__cat_encoding_file = "pet_disease/data/cat_data_encoding.csv"


        self.__dog_breed_dictionary = Dog_Breed.Dog_Breed
        self.__cat_breed_dictionary = Cat_Breed.Cat_Breed
        self.__pet_class_dictionary = Pet_Class.Pet_Class
        self.__sex_dictionary = Sex.Sex
        self.__exercise_dictionary = Exercise.Exercise
        self.__environment_dictionary = Environment.Environment
        self.__defecation_dictionary = Defecation.Defecation
        self.__food_count_dictionary = Food_Count.Food_Count
        self.__food_kind_dictionary = Food_Kind.Food_Kind

    def data_encoding(self, data: Pet_Disease_Data.Pet_Disease_Data):

        species = int(self.species_encoding(data.get_species()))
        breed = int(self.breed_encoding(data.get_breed(), species))
        age = int(data.get_age())
        pet_class = int(self.pet_class_encoding(data.get_pet_class()))
        sex = int(self.pet_class_encoding(data.get_pet_class()))
        weight = int(data.get_weight())
        exercise = int(self.exercise_encoding(data.get_exercise()))
        environment = int(self.environment_encoding(data.get_environment()))
        defecation = int(self.defecation_encoding(data.get_defecation()))
        food_count = int(data.get_food_count())
        food_amount = float(data.get_food_amount())
        snack_amount = float(data.get_snack_amount())
        food_kind = int(self.food_kind_encoding(data.get_food_kind()))

        result = {"species":species, "breed":breed, "age":age, "pet_class":pet_class,
                  "sex":sex, "weight":weight, "exercise":exercise, "environment":environment,
                  "defecation":defecation, "food_count":food_count, "food_amount":food_amount,
                  "snack_amount":snack_amount, "food_kind":food_kind}

        return result

    def species_encoding(self, data):
        species = 0

        if(data == "강아지"):
            species = 10
        elif(data == "고양이"):
            species = 20
        else:
            species = -1

        return species

    def breed_encoding(self, data, species):
        breed = 0

        if species == 10:
            breed = self.__dog_breed_dictionary.__getitem__(data).value
        elif species == 20:
            breed = self.__cat_breed_dictionary.__getitem__(data).value
        else:
            breed = -1

        return breed

    def pet_class_encoding(self, data):
        pet_class = self.__pet_class_dictionary.__getitem__(data).value;

        return pet_class

    def sex_encoding(self, data):
        sex = self.__sex_dictionary.__getitem__(data).value

        return sex

    def exercise_encoding(self, data):
        exercise = self.__exercise_dictionary.__getitem__(data).value

        return exercise

    def environment_encoding(self, data):
        environment = self.__environment_dictionary.__getitem__(data).value

        return environment

    def defecation_encoding(self, data):
        defecation = self.__defecation_dictionary.__getitem__(data).value

        return defecation

    def food_count_encoding(self, data):
        food_count = 0

        if data >= 4 :
            food_count = self.__food_count_dictionary.__getitem__("FREE").value
        else:
            print(data)
            food_count = self.__food_count_dictionary.__getitem__(data).value

        return food_count

    def food_kind_encoding(self,data):
        food_kind = self.__food_kind_dictionary.__getitem__(data).value

        return food_kind

    def dog_data_encoding_file(self):
        df = pd.read_csv(self.__dog_data_file, encoding='UTF8', header=None)

        # 데이터 매핑
        df[2] = df[2].map(self.__dog_breed_dictionary)  # 열 번호를 사용하여 열을 참조
        df[4] = df[4].map(self.__pet_class_dictionary)
        df[5] = df[5].map(self.__sex_dictionary)

        # 인코딩된 데이터 저장
        df.to_csv(self.__dog_encoding_file, mode='a', index=False, header=False, encoding='UTF8')

    def cat_data_encoding_file(self):
        df = pd.read_csv(self.__cat_data_file, encoding='UTF8', header=None)  # 헤더가 없는 경우

        # 데이터 매핑
        df[2] = df[2].map(self.__cat_breed_dictionary)
        df[4] = df[4].map(self.__pet_class_dictionary)
        df[5] = df[5].map(self.__sex_dictionary)

        # 인코딩된 데이터 저장
        df.to_csv(self.__cat_encoding_file, mode='a', index=False, header=False, encoding='UTF8')

# test = Pet_Data_Encoding()
# t = test.breed_encoding("BEA", 10)
# print(t)

# test.dog_data_encoding_file()
# test.cat_data_encoding_file()