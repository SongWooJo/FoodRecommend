import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def recommend_similar_foods(selected_foods):
    df = pd.read_csv('./data/recipe(20000).csv', encoding='cp949')

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(df['description'].astype(str))

    # 코사인 유사도 계산
    similarity_matrix = cosine_similarity(X, X)

    for food in selected_foods:
        if food not in df['food'].values:
            raise ValueError(f"'{food}'은(는) 데이터셋에 존재하지 않습니다.")

    # 선택한 음식들의 인덱스를 찾기
    food_indices = [df[df['food'] == food].index[0] for food in selected_foods]

    # 유사도 벡터를 가져오기
    similarity_scores = np.mean([similarity_matrix[idx] for idx in food_indices], axis=0)

    # 인덱스값 순서대로 바꾸고 자기 자신 제외
    similar_indices = np.argsort(similarity_scores)[::-1][1:]

    # 추천 음식 반환
    recommended_foods = df.iloc[similar_indices]['food'].values
    
    return recommended_foods