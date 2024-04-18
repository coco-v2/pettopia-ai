import csv
from ..Enum import Dog_Breed, Cat_Breed, Pet_Class, Sex, Exercise, Environment, Defecation, Food_Count
from ..Entity import Pet_Disease_Data

class Pet_Data_Encoding():

    def __init__(self):
        self.__cat_data_file = "../data/cat_data.csv"
        self.__dog_data_file = '../data/dog_data.csv'

        self.__dog_encoding_file = '../data/dog_data_encoding.csv'
        self.__cat_encoding_file = '../data/cat_data_encoding.csv'


        self.__dog_breed_dictionary = Dog_Breed.Dog_Breed
        self.__cat_breed_dictionary = Cat_Breed.Cat_Breed
        self.__pet_class_dictionary = Pet_Class.Pet_Class
        self.__sex_dictionary = Sex.Sex
        self.__exercise_dictionary = Exercise.Exercise
        self.__environment_dictionary = Environment.Environment
        self.__defecation_dictionary = Defecation.Defecation
        self.__food_count_dictionary = Food_Count.Food_Count

    def data_encoding(self, data:Pet_Disease_Data.Pet_Disease_Data):
        result={}

        species = self.species_encoding(data.get_species())
        breed = self.breed_encoding(data.get_breed(), species)
        pet_class = self.pet_class_encoding(data.get_pet_class())
        sex = self.pet_class_encoding(data.get_pet_class())
        exercise = self.exercise_encoding(data.get_exercise())
        environment = self.environment_encoding(data.get_environment())
        defecation = self.defecation_encoding(data.get_defecation())
        food_count = self.food_count_encoding(data.get_food_count())
        

    def species_encoding(self, data):
        species = 0

        if(data == "강아지"):
            species = 10
        elif(data == "고양이"):
            species = 20
        else:
            species = -1

        return species

    #Todo 각 데이터 인코딩
    def breed_encoding(self, data, species):
        breed = 0
        print(data)
        print(species)

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

        return  environment

    def defecation_encoding(self, data):
        defecation = self.__defecation_dictionary.__getitem__(data).value

        return defecation

    def food_count_encoding(self, data):
        food_count = 0

        if data >= 4 :
            food_count = self.__food_count_dictionary.__getitem__("FREE").value
        else:
            food_count = self.__food_count_dictionary.__getitem__(data).value

        return food_count

    def dog_data_encoding_file(self):
        file = open(self.__dog_data_file, 'r')
        data = csv.reader(file)

        for line in data:
            breed = line[2]
            pet_class = line[4]
            sex = line[5]

            line[2] = self.__dog_breed_dictionary.get(breed)
            line[4] = self.__pet_class_dictionary.get(pet_class)
            line[5] = self.__sex_dictionary.get(sex)

            with open(self.__dog_encoding_file, 'a', newline='', encoding='UTF8') as f:
                csv_writer = csv.writer(f)
                csv_writer.writerow(line)

    def cat_data_encoding_file(self):
        file = open(self.__cat_data_file, 'r')
        data = csv.reader(file)

        for line in data:
            breed = line[2]
            pet_class = line[4]
            sex = line[5]

            line[2] = self.__cat_breed_dictionary.get(breed)
            line[4] = self.__pet_class_dictionary.get(pet_class)
            line[5] = self.__sex_dictionary.get(sex)

            with open(self.__cat_encoding_file, 'a', newline='', encoding='UTF8') as f:
                csv_writer = csv.writer(f)
                csv_writer.writerow(line)

test = Pet_Data_Encoding()
t = test.breed_encoding("BEA", 10)
print(t)