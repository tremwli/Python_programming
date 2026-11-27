# 뉴스 기사 분류하기 (Streamlit 웹 화면)

import os
import streamlit as st
from transformers import pipeline

# ===========================================================
#  1. 모델 불러오기
#  - ai.py 에서 파인 튜닝하고 저장한 뉴스 분류 모델을 불러옴
# ===========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
save_dir = os.path.join(BASE_DIR, "model")


@st.cache_resource                                  # 모델을 한 번만 불러서 계속 재사용
def load_classifier():
    return pipeline((                 ), model=save_dir)


# ===========================================================
#  2. 화면 만들기
# ===========================================================

st.title("📰 뉴스 기사 분류기")
st.write("뉴스 기사 제목을 입력하면 정치 / 경제 / 문화 / 스포츠 중 어디에 속하는지 알려줘요.")

classifier = load_classifier()

news = st.text_input("뉴스 기사 제목", placeholder="예) 여야가 새해 예산안 처리를 두고 협상을 이어갔어요")

if st.button("분류하기"):
    news = news.strip()

    if not news:
        st.warning("뉴스 기사 제목을 입력해 주세요.")
    else:
        with st.spinner("분류하는 중..."):
            results = classifier(news, top_k=None)      # [{'label': '정치', 'score': 0.68}, ...] 점수 높은 순

        best = results[0]                               # 점수가 가장 높은 범주
        st.success(f"분류 결과 : **{best['label']}** ({best['score']:.0%})")

        # 범주별 확률 보여주기
        st.subheader("범주별 확률")
        for result in results:
            st.progress(result["score"], text=f"{result['label']}  {result['score']:.0%}")
