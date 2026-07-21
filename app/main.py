#FastAPI
from fastapi import FastAPI
from schemas import CarInput, PredictionResponse
from predictor import predict_price

# FastAPI 앱 생성
app = FastAPI(
    title="Used Car Price Prediction API",
    description="중고차 가격 예측 서비스",
    version="1.0"
)

# 서버 실행 확인
@app.get("/")
def home():
    return {
        "message": "중고차 가격 예측 API가 실행 중입니다."
    }

# 가격 예측
@app.post("/predict", response_model=PredictionResponse)
def predict(car: CarInput):

    # 입력 데이터를 딕셔너리로 변환
    data = car.model_dump()

    # 모델 예측
    result = predict_price(data)

    # 결과 반환
    return PredictionResponse(
        predicted_price=result
    )