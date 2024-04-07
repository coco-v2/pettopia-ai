import csv
import Pet_Data_Encoding as enco

class Pet_Data_Decoding():

    def __init__(self):
        encoder = enco.Pet_Data_Encoding()

        self.dog_breed = {v:k for k,v in encoder.dog_breed.items()}
        self.cat_breed = {v:k for k,v in encoder.cat_breed.items()}
        self.pet_class = {v:k for k,v in encoder.pet_class.items()}
        self.sex = {v:k for k,v in encoder.sex.items()}

    def dog_data_decoding(self, breed, pet_class, sex):

        deco_breed = self.dog_breed.get(str(breed))
        deco_pet_class = self.pet_class.get(str(pet_class))
        deco_sex = self.sex.get(str(sex))

        return deco_breed, deco_pet_class, deco_sex

    def cat_data_decoding(self, breed, pet_class, sex):

        deco_breed = self.cat_breed.get(str(breed))
        deco_pet_class = self.pet_class.get(str(pet_class))
        deco_sex = self.sex.get(str(sex))

        return deco_breed, deco_pet_class, deco_sex



test = Pet_Data_Decoding()

t=test.dog_data_decoding(2, 1, 1)
print(t)
