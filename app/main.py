#FastAPI
from app.gpt import analyze_price
from fastapi import FastAPI
from app.schemas import CarInput, PredictionResponse
from app.predictor import predict_price

# FastAPI 앱 생성
app = FastAPI(title="Used Car Price Prediction API",description="중고차 가격 예측 서비스",version="1.0")

# 서버 실행 확인
@app.get("/")
def home():
    return {"message": "중고차 가격 예측 API가 실행 중입니다."}

# 가격 예측
@app.post("/predict", response_model=PredictionResponse)
def predict(car: CarInput):

    # 입력 데이터를 딕셔너리로 변환
    data = car.model_dump()

    # 모델 예측
    result = predict_price(data)

    # GPT 분석
    analysis = analyze_price(
    predicted_price=result,
    year=car.Year,
    present_price=car.Present_Price,
    kms_driven=car.Kms_Driven,
    fuel_type=car.Fuel_Type,
    seller_type=car.Seller_Type,
    transmission=car.Transmission,
    owner=car.Owner)

    # 결과 반환
    return PredictionResponse(predicted_price=result,currency="USD",analysis=analysis)