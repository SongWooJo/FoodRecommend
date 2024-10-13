import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def refrigerator(materials):
  df = pd.read_csv('./data/recipe(20000).csv', encoding = 'cp949')

  recipe_sample_list = df['description'].tolist()
  materials_string = ''.join(materials)

  vectorizer = TfidfVectorizer()

  all_docs = recipe_sample_list + [materials_string]
  tfidf_matrix = vectorizer.fit_transform(all_docs)

  similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])

  # 코사인 유사도 결과
  top = np.argsort(similarities[0])[::-1][:5]
  recommended_dish = df['food'].iloc[top].tolist()

  return recommended_dish