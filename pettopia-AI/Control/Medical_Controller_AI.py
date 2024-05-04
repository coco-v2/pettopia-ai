from ..AI.pet_disease.Pet_Disease_Model import Pet_Disease_Model
from ..AI.pet_disease.Entity.Pet_Disease_Data import Pet_Disease_Data
from ..AI.pet_disease.Preprocessing.Pet_Data_Decoding import Pet_Data_Decoding

class Medical_Controller_AI():

    def get_pet_disease(self, breed, age, pet_class, sex, weight, exercise, environment, defecation, food_count, food_amount, snack_amount, food_kind):
        test = Pet_Disease_Model()
        test.preprocess_pet_data(data)
        recommended_abn_pet_df = test.pet_disease_recommend()
        decoder = Pet_Data_Decoding()
        result = decoder.data_decoding(recommended_abn_pet_df)

        return result


    def get_pet_skin_disease(self, img):
        return 0

# test = Medical_Controller_AI()
# data = Pet_Disease_Data("강아지","BEA",2,"SH","IM",10.4,"LOW","IN_DOOR","NORMAL",4,3,1,"FEED")
# test.get_pet_disease(data)