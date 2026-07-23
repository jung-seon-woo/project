# Request/Response (FastAPI가 사용자에게 어떤 데이터를 받을지 정의)
from pydantic import BaseModel

#중고차 입력 데이터
class CarInput(BaseModel):
    Year: int
    Present_Price: float
    Kms_Driven: int
    Fuel_Type: str
    Seller_Type: str
    Transmission: str
    Owner: int

# 예측 결과
class PredictionResponse(BaseModel):
    predicted_price: float
    currency: str
    analysis: str