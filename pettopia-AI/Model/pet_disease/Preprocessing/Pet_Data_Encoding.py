import csv
from ..Entity import Pet_Disease_Data
from ..Enum import Dog_Breed, Cat_Breed, Pet_Class, Sex

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

    def data_encoding(self, data:Pet_Disease_Data):
        result={}

        species = 0
        breed = self.__
        pet_class = 0
        sex = 0
        exercise = 0
        environment = 0
        defecation = 0

        if data.get_species() == "반려견":
            species = 10
        elif data.get_species() == "반려묘":
            species = 20

        breed =

    def species_encoding(self, data):
        species = 0

        if(data == "강아지"):
            species = 10
        elif(data == "고양이"):
            species = 20
        else:
            species = 10

        return species

    #Todo 각 데이터 인코딩
    def breed_encoding(self, data, species):
        breed = 0

        if

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