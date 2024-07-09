import sys, os, uuid
import cv2

sys.path.append('pettopia-AI')
from AI.pet_skin_disease.model.Pet_Skin_Disease_Model import Pet_Skin_Disease_Model
from AI.pet_disease.Pet_Disease_Model import Pet_Disease_Model
from AI.pet_disease.Entity.Pet_Disease_Data import Pet_Disease_Data
from AI.pet_disease.Preprocessing.Pet_Data_Decoding import Pet_Data_Decoding

class Medical_Controller_AI():

    def get_pet_disease(self, species, breed, age, pet_class, sex, weight, exercise, environment, defecation, food_count, food_amount, snack_amount, food_kind):
        test = Pet_Disease_Model()
        data = Pet_Disease_Data(species, breed, age, pet_class, sex, weight, exercise, environment, defecation, food_count, food_amount, snack_amount, food_kind)
        test.preprocess_pet_data(data)
        recommended_abn_pet_df = test.pet_disease_recommend()
        decoder = Pet_Data_Decoding()
        result = decoder.data_decoding(recommended_abn_pet_df)

        return result


    def get_pet_skin_disease(self, img):
        img_filename = f"uploaded_{uuid.uuid4()}.jpg"
        print("5")
        path = 'AI/pet_skin_disease/data/image'
        img_path = os.path.join(path, img_filename)
        print("6")
        try:

            cv2.imwrite(img_path, img)
            print("Save success")
        except Exception as e:
            # 예외가 발생할 경우
            print("Error during image save:", e)
        print("7")
        result = Pet_Skin_Disease_Model().model_test(img_filename)
        print("8")
        return result


#test = Medical_Controller_AI()
# #data = Pet_Disease_Data("강아지","GRE",2,"LH","IF",3.0,"LOW","IN_DOOR","NORMAL",3,4,2,"FEED")
#
# test.get_pet_disease("강아지","GRE",2,"LH","IF",3.0,"LOW","IN_DOOR","NORMAL",3,4,2,"FEED")
# print(test)
#test.get_pet_skin_disease('test3.jpg')