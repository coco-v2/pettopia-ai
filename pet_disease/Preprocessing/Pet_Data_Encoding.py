import csv

class Pet_Data_Encoding():

    def __init__(self):
        self.cat_data_file = "../data/cat_data.csv"
        self.dog_data_file = '../data/dog_data.csv'

        self.dog_encoding_file = '../data/dog_data_encoding.csv'
        self.cat_encoding_file = '../data/cat_data_encoding.csv'


        self.dog_breed = {'GRE' : '1', 'DAL':'2', 'DAS':'3', 'DOB':'4','GOL':'5',
                        'LAB':'6', 'MAL':'7', 'BUL':'8', 'BEA':'9', 'BIC':'10',
                        'SHE':'11', 'SCH':'12', 'DRI':'13', 'WEL':'14', 'GER':'15', 'JIN':'16',
                        'CHL':'17', 'CHS':'18', 'COC':'19', 'TER':'20', 'POM':'21',
                        'POO':'22', 'HOU':'23', 'HUS':'24', 'MUT':'25', 'MIL':'26',
                        'MIS':'27', 'ETC':'28'}
        self.cat_breed = {'KOR':'1', 'RUS':'2', 'PER':'3', 'SIA':'4', 'TUR':'5',
                          'SCO':'6', 'MIX':'7', 'ETC':'8'}
        self.pet_class = {'LH':'1', 'SH':'2', 'UK':'3'}
        self.sex = {'IM':'1', 'IF':'2', 'CM':'3', 'SF':'4'}

    def dog_data_encoding(self):
        file = open(self.dog_data_file, 'r')
        data = csv.reader(file)

        for line in data:
            breed = line[2]
            pet_class = line[4]
            sex = line[5]

            line[2] = self.dog_breed.get(breed)
            line[4] = self.pet_class.get(pet_class)
            line[5] = self.sex.get(sex)

            with open(self.dog_encoding_file, 'a', newline='', encoding='UTF8') as f:
                csv_writer = csv.writer(f)
                csv_writer.writerow(line)

    def cat_data_encoding(self):
        file = open(self.cat_data_file, 'r')
        data = csv.reader(file)

        for line in data:
            breed = line[2]
            pet_class = line[4]
            sex = line[5]

            line[2] = self.cat_breed.get(breed)
            line[4] = self.pet_class.get(pet_class)
            line[5] = self.sex.get(sex)

            with open(self.cat_encoding_file, 'a', newline='', encoding='UTF8') as f:
                csv_writer = csv.writer(f)
                csv_writer.writerow(line)



test = Pet_Data_Encoding()
# test.dog_data_encoding()
#test.cat_data_encoding()