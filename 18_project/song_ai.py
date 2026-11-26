# AI 모듈
# - 파인 튜닝한 모델로 급식 리뷰를 긍정 / 부정으로 분류

import os
import streamlit as st
from transformers import pipeline
from sentence_transformers import SentenceTransformer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "model")



# ===========================================================
#  1. 준비하기
#  - @st.cache_resource : 모델을 처음 사용할 때 한 번만 불러오고,
#    이후에는 (재실행, 다른 세션에서도) 같은 객체를 재사용
# ===========================================================




@st.cache_resource(show_spinner="모델 불러오는 중...") # 이거 하면 더 빨라짐
def get_model():
    model = SentenceTransformer("nlpai-lab/KURE-v1")
    return model


def search(query, songs, top_n=5):
    model = get_model()

    passages = []
    for song in songs:
         passages.append(song["가사"])

    query_vec = model.encode( query, normalize_embeddings=True)
    passage_vecs = model.encode(passages, normalize_embeddings=True)

    scores = model.similarity(query_vec, passage_vecs)[0]

    for i in range(len(songs)):
        songs[i]["점수"] = float(scores[i])

    
    songs.sort(key=lambda s: s["점수"], reverse=True)  
    return songs[:top_n] 