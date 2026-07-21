#모델예측(함수만 정의)
from pathlib import Path
import joblib
import pandas as pd

#현재 파일 기준 경로 설정
BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR.parent / "model"

#모델 및 전처리 파일 불러오기
model = joblib.load(MODEL_DIR / "model.pkl")
label_encoders = joblib.load(MODEL_DIR / "label_encoders.pkl")
feature_columns = joblib.load(MODEL_DIR / "feature_columns.pkl")

#예측 함수
def predict_price(data: dict):

    df = pd.DataFrame([data])

    #문자열 데이터를 숫자형으로 변환
    categorical_columns = ["Fuel_Type","Seller_Type","Transmission"]

    for col in categorical_columns:
        df[col] = label_encoders[col].transform(df[col])

    # 학습했던 데이터 양식 순서 맞추기
    df = df[feature_columns]

# 모델 예측
    prediction = model.predict(df)
    return round(float(prediction[0]), 2)

#코드 테스트 (주석처리할것)
if __name__ == "__main__":
    sample = {
        "Year": 2018,
        "Present_Price": 8.5,
        "Kms_Driven": 30000,
        "Fuel_Type": "Petrol",
        "Seller_Type": "Dealer",
        "Transmission": "Manual",
        "Owner": 0
    }

    result = predict_price(sample)
    print(f"예측 중고차 가격 : ${result:.1f}")