class Pet_Disease_Data():

    def __init__(self, species, breed, age, pet_class, sex, weight, exercise,
                              environment, defecation, food_count, food_amount,snack_amount, food_kind):
        self.__species:str = species
        self.__breed:str = breed
        self.__age:int = age
        self.__pet_class:str = pet_class
        self.__sex:str = sex
        self.__weight:float = weight
        self.__exercise:str = exercise
        self.__environment:str = environment
        self.__defecation:str = defecation
        self.__food_count:int = food_count
        self.__food_amount:int = food_amount
        self.__snack_amount:int = snack_amount
        self.__food_kind:int = food_kind

    def get_species(self):
        return self.__species

    def get_breed(self):
        return self.__breed

    def get_age(self):
        return self.__age

    def get_pet_class(self):
        return self.__pet_class

    def get_sex(self):
        return self.__sex

    def get_weight(self):
        return self.__weight

    def get_exercise(self):
        return self.__exercise

    def get_environment(self):
        return self.__environment

    def get_defecation(self):
        return self.__defecation

    def get_food_count(self):
        return self.__food_count

    def get_food_amount(self):
        return self.__food_amount

    def get_snack_amount(self):
        return self.__snack_amount

    def get_food_kind(self):
        return self.__food_kind