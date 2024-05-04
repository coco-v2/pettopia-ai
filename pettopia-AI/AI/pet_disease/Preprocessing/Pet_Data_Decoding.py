import re

class Pet_Data_Decoding():

    def data_decoding(self, abn_data):

        species = int(abn_data['pet_species'])
        breed = int(abn_data['breed'])

        if species == 10:
            breed = self.dog_breed_decoding(breed)
        else:
            breed = self.cat_breed_decoding(breed)

        age = int(abn_data['age'])
        pet_class = self.pet_class_decoding(int(abn_data['pet_class']))
        sex = self.sex_decoding(int(abn_data['sex']))
        weight = int(abn_data['weight'])
        exercise = self.exercise_decoding(int(abn_data['exercise']))
        environment = self.environment_decoding(int(abn_data['environment']))
        defecation = self.defecation_decoding(int(abn_data['defecation']))
        food_count = self.food_count_decoding(int(abn_data['food_count']))
        food_amount = float(abn_data['food_amount'])
        snack_amount = float(abn_data['snack_amount'])
        food_kind = self.food_kind_decoding(int(abn_data['food_kind']))

        abn_disease_name = abn_data['disease_name']
        abn_CRP = float(abn_data['CRP'])
        abn_IgG = float(abn_data['IgG'])
        abn_AFP = float(abn_data['AFP'])
        abn_stress = float(abn_data['stress'])

        pattern = r'\b[A-Z]+'
        matches = re.findall(pattern, str(abn_disease_name))

        if matches[-1] == 'N':
            matches.pop(-1)

        decoded_diseases = []

        for code in matches:
            decoded_diseases.append(self.abn_disease_name_decoding(code))
        results = {
            'breed': breed,
            'age': age,
            'pet_class': pet_class,
            'sex': sex,
            'weight': weight,
            'exercise': exercise,
            'environment': environment,
            'defecation': defecation,
            'food_count': food_count,
            'food_amount': food_amount,
            'snack_amount': snack_amount,
            'food_kind': food_kind,
            'disease_name': decoded_diseases,
            'CRP': abn_CRP,
            'IgG': abn_IgG,
            'AFP': abn_AFP,
            'stress': abn_stress
        }

        return results

    def abn_disease_name_decoding(self, name):
        if name == "DER":
            return "피부"
        elif name == "MUS":
            return "근골격계"
        elif name == "NEU":
            return "신경계"
        elif name == "OCU":
            return "안과"
        elif name == "RES":
            return "호흡계통"
        elif name == "CAR":
            return "심혈계통"
        elif name == "HEM":
            return "혈액"
        elif name == "GAS":
            return "소화계통"
        elif name == "URI":
            return "비뇨계통"
        elif name == "REP":
            return "생식계통"
        elif name == "END":
            return "내분비계통"
        elif name == "INF":
            return "감염성 및 기생충성"
        elif name == "ETC":
            return "기타"
        else:
            return "Unknown Disease"

    def dog_breed_decoding(self, breed):
        if breed == 1:
            return "그레이트피레니즈"
        elif breed == 2:
            return "닥스훈트 장모"
        elif breed == 3:
            return "닥스훈트 단모"
        elif breed == 4:
            return "도베르만 핀셔"
        elif breed == 5:
            return "골드 리트리버"
        elif breed == 6:
            return "래브라도 리트리버"
        elif breed == 7:
            return "몰티즈"
        elif breed == 8:
            return "불독"
        elif breed == 9:
            return "비글"
        elif breed == 10:
            return "비숑 프리제"
        elif breed == 11:
            return "쉽독"
        elif breed == 12:
            return "슈나우저"
        elif breed == 13:
            return "시추"
        elif breed == 14:
            return "웰시코기"
        elif breed == 15:
            return "저먼셰퍼드"
        elif breed == 16:
            return "진도"
        elif breed == 17:
            return "치와와 장모"
        elif breed == 18:
            return "치와와 단모"
        elif breed == 19:
            return "코커스패니엘"
        elif breed == 20:
            return "테리어"
        elif breed == 21:
            return "포메라니안"
        elif breed == 22:
            return "푸들"
        elif breed == 23:
            return "하우드"
        elif breed == 24:
            return "허스키"
        elif breed == 25:
            return "말라뮤트"
        elif breed == 26:
            return "믹스 장모"
        elif breed == 27:
            return "믹스 단모"
        elif breed == 28:
            return "기타"
        else:
            return "Unknown Breed"
    def cat_breed_decoding(self, breed):
        if breed == 1:
            return "코리안숏헤어"
        elif breed == 2:
            return "러시안 블루"
        elif breed == 3:
            return "페르시안"
        elif breed == 4:
            return "샴"
        elif breed == 5:
            return "터키시알고라"
        elif breed == 6:
            return "스코티시폴드"
        elif breed == 7:
            return "믹스묘"
        elif breed == 8:
            return "기타"
        else:
            return "Unknown Breed"

    def pet_class_decoding(self, pet_class):
        if pet_class == 1:
            return "장모종"
        elif pet_class == 2:
            return "단모종"
        else:
            return "Unknown pet_class"

    def sex_decoding(self, sex):
        if sex == 1:
            return "수컷"
        elif sex == 2:
            return "암컷"
        elif sex == 3:
            return "중성화 수컷"
        elif sex == 4:
            return "중성화 암컷"
        else:
            return "Unknown sex"

    def exercise_decoding(self, exercise):
        if exercise == 1:
            return "1주일에 1시간 이하"
        elif exercise == 2:
            return "매일 30분 이하"
        elif exercise == 3:
            return "매일 1시간 이상"
        else:
            return "Unknown exercise"

    def environment_decoding(self, environment):
        if environment == 1:
            return "실내 생활"
        elif environment == 2:
            return "야외 생활"
        else:
            return "Unknown environment"

    def defecation_decoding(self, defecation):
        if defecation == 1:
            return "정상 배변"
        elif defecation == 2:
            return "이상 배변"
        else:
            return "Unknown defecation"


    def food_count_decoding(self, food_count):
        if food_count == 1:
            return "하루 1회"
        elif food_count == 2:
            return "하루 2회"
        elif food_count == 3:
            return "하루 3회"
        elif food_count == 4:
            return "자유 급식"
        else:
            return "Unknown food_count"


    def food_kind_decoding(self, food_kind):
        if food_kind == 1:
            return "반료 동물 전용 사료만 제공"
        elif food_kind == 2:
            return "전용 사료와 사람 음식 혼용하여 제공"
        elif food_kind == 3:
            return "사람 음식 위주로 제공"
        else:
            return "Unknown food_kind"
