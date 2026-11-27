# ===========================================================
#  [Claude가 채운 내용 요약]
#  ai.py (ex2 급식 리뷰 분류 코드와 같은 방식, 범주만 2개 -> 4개)
#  - 85줄  id2label={0: "정치", 1: "경제", 2: "문화", 3: "스포츠"}
#          (데이터 만들 때 붙인 번호 0~3과 순서를 똑같이 맞춤)
#  - 99줄  tokenizer(...)          : 문장 -> 숫자 (ex2 make_dataset)
#  - 115줄 model.eval()            : 평가 모드 (ex2 predict)
#  - 116줄 torch.no_grad()         : 학습 없이 예측만 (ex2 predict)
#  - 145줄 model.parameters()      : 고칠 모델의 모든 값 (ex2 옵티마이저)
#  - 150줄 model.train()           : 학습 모드
#  - 152줄 labels=train_labels     : 학습용 정답을 같이 넣어 loss 계산
#  - 155~157줄 zero_grad() / backward() / step() : 지우기 -> 계산 -> 고치기
#  - 190줄 pipeline("text-classification", ...) : 저장한 모델 불러오기 (ex3)
#  app.py (이 파일)
#  - 43줄  pipeline("text-classification", ...) : ai.py와 같은 작업 이름 (15 review_ai.py)
#
#  [TODO - 직접 채워야 할 곳]
#  - 없음. 모델 폴더는 ai.py가 저장하는 "model" 폴더를 그대로 씀
#
#  [실행 순서]
#  1) python ai.py          -> 학습 후 17_ai_test/model 폴더에 모델 저장
#  2) streamlit run app.py  -> 웹 화면 실행
#  ※ model 폴더는 .gitignore 때문에 GitHub에 안 올라가는 게 정상
# ===========================================================

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
    return pipeline("text-classification", model=save_dir)


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
