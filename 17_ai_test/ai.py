# 모델 파인 튜닝하기 (뉴스 기사 분류 모델)

import os
import json
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

# ===========================================================
#  1. 패키지 목록
#  - torch : PyTorch 딥러닝 라이브러리
#  - AutoTokenizer : 문장을 모델이 읽을 수 있는 숫자로 바꾸는 도구
#  - AutoModelForSequenceClassification : 문장 하나를 통째로 읽고 범주 하나로 분류하는 모델
#  - pipeline : 저장한 모델을 다시 불러서 간단하게 사용하는 도구
#  - 예시) "코스피가 상승했어요" → [AutoTokenizer] → 숫자 → [AutoModelForSequenceClassification] → 경제
#
#  [설치]
#  - pip install transformers torch
# ===========================================================

# ===========================================================
#  2. 우리가 만들 모델
#  - 뉴스 기사 제목을 읽고 정치(0) / 경제(1) / 문화(2) / 스포츠(3) 로 분류
#  - KoELECTRA : 한국어 문장을 학습한 작은 모델 (영어 모델은 한국어를 구분하지 못함)
#  - 범주마다 기사 제목 40개씩 (학습용: 32개, 평가용: 8개)
#
#  [순서]
#  1) 데이터 준비하고 학습용 / 평가용으로 나누기
#  2) 기존 모델과 토크나이저 불러오기
#  3) 모델 학습하기 (예측 -> 오차 -> 수정 반복)
#  4) 학습한 모델을 저장하고 다시 불러서 사용하기
# ===========================================================

# ===========================================================
#  3. 데이터 준비하기
#  - (기사 제목, 정답) 형태 -> 정답은 0(정치) / 1(경제) / 2(문화) / 3(스포츠)
#  - 범주를 돌아가며 한 개씩 배치
# ===========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, "data", "news.json"), encoding="utf-8") as f:
    news = json.load(f)

categories = ["정치", "경제", "문화", "스포츠"]                 # 번호 순서 : 0: 정치, 1: 경제, 2: 문화, 3: 스포츠

# 범주별 기사 제목을 한 개씩 돌아가며 합치기
data = []
for i in range(40):
    data.append((news["정치"][i], 0))                           # (정치, 0)
    data.append((news["경제"][i], 1))                           # (경제, 1)
    data.append((news["문화"][i], 2))                           # (문화, 2)
    data.append((news["스포츠"][i], 3))                         # (스포츠, 3)


# ===========================================================
#  4. 학습용 / 평가용 데이터 나누기
#  - 학습용 데이터 (train) : 모델이 공부하는 데이터
#  - 평가용 데이터 (test)  : 모델이 한 번도 못 본 데이터. 시험 문제 역할
#  - 5번째마다 평가용(test)으로 따로 빼고, 나머지는 학습용(train)으로 사용
#
#  [주의]
#  - 평가용 데이터는 학습에 절대 사용하지 않음
#  - 학습 정확도는 높은데 평가 정확도가 낮으면 외우기만 한 것 (= 과적합)
# ===========================================================

# 5번째마다 평가용, 나머지는 학습용
train_data = [d for i, d in enumerate(data) if i % 5 != 4]
test_data = [d for i, d in enumerate(data) if i % 5 == 4]

print(f"학습용 {len(train_data)}개 / 평가용 {len(test_data)}개")


# ===========================================================
#  5. 기존 모델 불러오기
#  - from_pretrained(모델이름) : 허깅페이스에서 이미 학습된 모델을 내려받아 불러옴
#    (최초 1회 다운로드, 이후에는 내 PC에 저장된 캐시 사용)
#  - id2label : 분류할 범주가 4개(정치, 경제, 문화, 스포츠)라는 것을 모델에 알려줌
# ===========================================================

model_name = "monologg/koelectra-small-v3-discriminator"        # 허깅페이스 모델 이름 (한국어 KoELECTRA small)

tokenizer = AutoTokenizer.from_pretrained(model_name)           # 토크나이저 불러오기
model = AutoModelForSequenceClassification.from_pretrained(     # KoELECTRA 본체 + 4개 분류용 층
    model_name,
    id2label={0: "정치", 1: "경제", 2: "문화", 3: "스포츠"},     # 분류개수와 출력이름 지정
)


# ===========================================================
#  6. 데이터 변환하기
#  - (기사 제목, 정답) 목록을 모델에 넣을 수 있는 형태로 바꾸기
#  - 문장 -> 숫자 텐서, 정답 -> 정수 텐서로 바꿈
# ===========================================================

def make_dataset(data):
    texts = [text for text, label in data]                          # 기사 제목만 모음
    labels = torch.tensor([label for text, label in data])          # 정답(0~3)만 모아 텐서로 변환

    inputs = tokenizer(texts, padding=True, return_tensors="pt")    # 문장 -> 숫자
    return inputs, labels


# 학습용, 평가용 데이터를 각각 숫자로 변환
train_inputs, train_labels = make_dataset(train_data)
test_inputs, test_labels = make_dataset(test_data)


# ===========================================================
#  7. 정확도 확인하기
#  - predict : 문장들의 범주 번호(0: 정치 / 1: 경제 / 2: 문화 / 3: 스포츠)를 예측
#  - accuracy : 예측한 번호가 정답과 얼마나 맞는지 비율로 계산
# ===========================================================

def predict(inputs):
    model.eval()                                    # 평가 모드
    with torch.no_grad():                           # 학습하지 않고 예측만 하기
        logits = model(**inputs).logits             # 문장 숫자를 모델에 넣고 분류 점수(logits)만 꺼내기
    return logits.argmax(dim=1)                     # 점수가 가장 높은 범주를 선택


def accuracy(inputs, labels):
    return (predict(inputs) == labels).float().mean().item()


print()
print("[학습 전]")
print(f"학습용 정확도 : {accuracy(train_inputs, train_labels):.0%}")
print(f"평가용 정확도 : {accuracy(test_inputs, test_labels):.0%}")


# ===========================================================
#  8. 학습하기
#  - 학습용 데이터로 모델의 값(가중치)을 조금씩 고쳐서 정답을 더 잘 맞히게 만드는 과정
#  - 예측 -> 오차 -> 수정 반복
#    1) 예측 : 모델이 기사 제목을 보고 범주별 점수를 계산
#    2) 오차 : 예측과 정답이 얼마나 다른지 계산 (loss, 작을수록 좋음)
#    3) 수정 : 오차가 줄어드는 방향으로 모델의 값을 조금 고침
#  - epoch : 학습 데이터 전체를 한 번 학습하는 것
#  - 옵티마이저(optimizer) : 모델의 값을 고쳐주는 도구 (AdamW)
#  - lr(learning rate, 학습률) : 한 번에 고치는 크기
#    (너무 크면 정답을 지나쳐 학습이 불안정하고, 너무 작으면 학습이 느림)
# ===========================================================

# 옵티마이저 생성 (lr = 학습률)
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4)

print()
print("[학습]")
for epoch in range(1, 51):                          # 50번 반복
    model.train()                                   # 학습 모드
    # 정답(labels)를 함께 넣으면 모델이 예측 점수(logits)와 함께 오차(loss)도 계산해줌
    outputs = model(**train_inputs, labels=train_labels)
    loss = outputs.loss                             # 오차 (텐서)

    optimizer.zero_grad()                           # 이전 기울기 지우기
    loss.backward()                                 # 기울기 계산
    optimizer.step()                                # 값 고치기

    print(f"epoch {epoch:2d} | loss = {loss.item():.3f}")
    # -> 반복할수록 loss 가 줄어들면 학습이 잘 되고 있는 것

print()
print("[학습 후]")
print(f"학습용 정확도 : {accuracy(train_inputs, train_labels):.0%}")    # 공부한 문장으로 본 시험
print(f"평가용 정확도 : {accuracy(test_inputs, test_labels):.0%}")      # 처음 보는 문장으로 본 시험


# ===========================================================
#  9. 모델 저장하기
#  - 파인 튜닝한 모델은 지금 메모리에만 있어서 프로그램을 끄면 사라짐
#  - 파일로 저장해두면 다시 학습하지 않고 불러서 사용할 수 있음
#  - 모델과 토크나이저 두개 파일을 저장
#  - 모델 : 학습으로 고쳐진 값(가중치) + 설정(분류 개수, 정치 / 경제 / 문화 / 스포츠 이름 등)
#  - 토크나이저 : 모델이 학습한 숫자 규칙을 저장
# ===========================================================

save_dir = os.path.join(BASE_DIR, "model")

model.save_pretrained(save_dir)         # 학습한 모델 저장 (고쳐진 가중치 + 설정)
tokenizer.save_pretrained(save_dir)     # 토크나이저 저장 (모델과 같은 폴더에)


# ===========================================================
#  10. 저장한 모델 불러오기
#  - 모델 이름 대신 내 폴더 경로를 넣음 (허깅페이스에서 내려받지 않고 내 PC의 파일을 사용)
#  - 학습에 사용하지 않은 새로운 기사 제목으로 확인
#  - 결과 : label(정치 / 경제 / 문화 / 스포츠) + score(확률, 0~1)
# ===========================================================

classifier = pipeline("text-classification", model=save_dir)

sentences = [
    "여야가 새해 예산안 처리를 두고 협상을 이어갔어요",
    "원 달러 환율이 올라 수입 물가 부담이 커졌어요",
    "국립중앙박물관에서 조선 시대 그림 전시가 시작됐어요",
    "공격수가 시즌 첫 골을 터뜨리며 팀 승리를 이끌었어요",
]

print()
print("[저장한 모델로 새 기사 분류하기]")
for sentence in sentences:
    result = classifier(sentence)[0]    # {'label': '정치', 'score': 0.91} 형태의 결과 중 첫 번째
    print(f"{result['label']} ({result['score']:.2f}) : {sentence}")
