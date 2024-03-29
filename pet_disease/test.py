import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def pet_disease_recommend(species, breed, age, pet_class, sex, weight, exercise,
                          environment, defecation, food_count, food_amount,snack_amount, food_kind,):
    #1~10
    weight_breed = 8
    weight_age = 7
    weight_pet_class = 7
    weight_sex = 7
    weight_weight = 3
    weight_exercise = 8
    weight_environment = 7
    weight_defecation = 9
    weight_food_count = 3
    weight_food_amount = 3
    weight_snack_amount = 5
    weight_food_kind = 5

    pet_features = np.array([breed, age, pet_class, sex, weight, exercise, environment,
                            defecation, food_count, food_amount, snack_amount, food_kind])
    pet_features_weight = pet_features * np.array([weight_breed, weight_age, weight_pet_class, weight_sex,
                                                   weight_weight, weight_exercise, weight_environment, weight_defecation,
                                                   weight_food_count, weight_food_amount, weight_snack_amount, weight_food_kind])

    #10:dog, 20:cat
    if species == "10":
        anonymous_data = pd.read_csv('data/dog_data.csv')
    elif species == "20":
        anonymous_data = pd.read_csv('data/cat_data.csv')

    similarity_scores = cosine_similarity([pet_features_weight], anonymous_data['species', 'breed', 'age', 'pet_class', 'sex', 'weight', 'exercise', 'environment', 'defecation', 'food_count', 'food_amount', 'snack_amount', 'food_kind'])
    most_similar_pet_index = np.argmax(similarity_scores)

    print(similarity_scores)
    print(most_similar_pet_index)

#데이터 타입 확인
pet_disease_recommend(10,"BEA",2,"SH","IM",10.4,1,2,1,1,4,0,1)

# def similar_recommend(level, category):
#
#   weight_level = 2
#   weight_category = 5
#
#   user_features = np.array([level, category])
#   user_features_weighted = user_features * np.array([weight_level, weight_category])
#
#   anonymous_data = pd.read_csv('C:\project\project\SECodeVerse_API\output.csv')  # 여기에 익명의 사용자들이 푼 문제 데이터가 들어있는 파일 경로를 넣어주세요
#
#   similarity_scores = cosine_similarity([user_features_weighted], anonymous_data[['level', 'inserted_pk']])
#   most_similar_problem_index = np.argmax(similarity_scores)
#
#   recommended_problems = []
#   for i in range(5):
#       while (
#           anonymous_data.iloc[most_similar_problem_index]['question_pk'] in recommended_problems
#       ):
#           similarity_scores[0, most_similar_problem_index] = -1  # 이미 추천된 문제나 사용자가 푼 문제는 제외
#           most_similar_problem_index = np.argmax(similarity_scores)
#       recommended_problems.append(anonymous_data.iloc[most_similar_problem_index]['question_pk'])
#
#   return recommended_problems