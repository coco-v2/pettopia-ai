import re
import pandas as pd

class Pet_Data_Decoding():

    def data_decoding(self, abn_data):
        abn_data['pet_species'] = pd.to_numeric(abn_data['pet_species'], errors='coerce').astype('Int64')
        abn_data['breed'] = pd.to_numeric(abn_data['breed'], errors='coerce').astype('Int64')

        results = []

        for index, row in abn_data.iterrows():
            species = row['pet_species']
            breed = row['breed']

            print(type(species))

            if species == 10:
                breed = self.dog_breed_decoding(breed)
            else:
                breed = self.cat_breed_decoding(breed)

            age = int(row['age'])
            pet_class = self.pet_class_decoding(int(row['pet_class']))
            sex = self.sex_decoding(int(row['sex']))
            weight = float(row['weight'])  # weight should be float
            exercise = self.exercise_decoding(int(row['exercise']))
            environment = self.environment_decoding(int(row['environment']))
            defecation = self.defecation_decoding(int(row['defecation']))
            food_count = self.food_count_decoding(int(row['food_count']))
            food_amount = float(row['food_amount'])
            snack_amount = float(row['snack_amount'])
            food_kind = self.food_kind_decoding(int(row['food_kind']))

            abn_disease_name = row['disease_name']
            abn_CRP = float(row['CRP'])
            abn_IgG = float(row['IgG'])
            abn_AFP = float(row['AFP'])
            abn_stress = float(row['stress'])

            pattern = r'\b[A-Z]+'
            matches = re.findall(pattern, str(abn_disease_name))

            if matches and matches[-1] == 'N':
                matches.pop(-1)

            decoded_diseases = []

            for code in matches:
                decoded_diseases.append(self.abn_disease_name_decoding(code))

            result = {
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

            results.append(result)

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
        breeds = {
            1: "그레이트피레니즈",
            2: "닥스훈트 장모",
            3: "닥스훈트 단모",
            4: "도베르만 핀셔",
            5: "골드 리트리버",
            6: "래브라도 리트리버",
            7: "몰티즈",
            8: "불독",
            9: "비글",
            10: "비숑 프리제",
            11: "쉽독",
            12: "슈나우저",
            13: "시추",
            14: "웰시코기",
            15: "저먼셰퍼드",
            16: "진도",
            17: "치와와 장모",
            18: "치와와 단모",
            19: "코커스패니엘",
            20: "테리어",
            21: "포메라니안",
            22: "푸들",
            23: "하우드",
            24: "허스키",
            25: "말라뮤트",
            26: "믹스 장모",
            27: "믹스 단모",
            28: "기타"
        }
        return breeds.get(breed, "Unknown Breed")

    def cat_breed_decoding(self, breed):
        breeds = {
            1: "코리안숏헤어",
            2: "러시안 블루",
            3: "페르시안",
            4: "샴",
            5: "터키시알고라",
            6: "스코티시폴드",
            7: "믹스묘",
            8: "기타"
        }
        return breeds.get(breed, "Unknown Breed")

    def pet_class_decoding(self, pet_class):
        pet_classes = {
            1: "장모종",
            2: "단모종"
        }
        return pet_classes.get(pet_class, "Unknown pet_class")

    def sex_decoding(self, sex):
        sexes = {
            1: "수컷",
            2: "암컷",
            3: "중성화 수컷",
            4: "중성화 암컷"
        }
        return sexes.get(sex, "Unknown sex")

    def exercise_decoding(self, exercise):
        exercises = {
            1: "1주일에 1시간 이하",
            2: "매일 30분 이하",
            3: "매일 1시간 이상"
        }
        return exercises.get(exercise, "Unknown exercise")

    def environment_decoding(self, environment):
        environments = {
            1: "실내 생활",
            2: "야외 생활"
        }
        return environments.get(environment, "Unknown environment")

    def defecation_decoding(self, defecation):
        defecations = {
            1: "정상 배변",
            2: "이상 배변"
        }
        return defecations.get(defecation, "Unknown defecation")

    def food_count_decoding(self, food_count):
        food_counts = {
            1: "하루 1회",
            2: "하루 2회",
            3: "하루 3회",
            4: "자유 급식"
        }
        return food_counts.get(food_count, "Unknown food_count")

    def food_kind_decoding(self, food_kind):
        food_kinds = {
            1: "반려 동물 전용 사료만 제공",
            2: "전용 사료와 사람 음식 혼용하여 제공",
            3: "사람 음식 위주로 제공"
        }
        return food_kinds.get(food_kind, "Unknown food_kind")
