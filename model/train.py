# 데이터 전처리 및 모델 학습
import pandas as pd
import joblib

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

df = pd.read_csv("../data/Used_Car_Price_Data.csv")
# 데이터셋은 Lakh 단위 달러 단위로 변환
LAKH_TO_USD = 1180
df["Selling_Price"] = df["Selling_Price"] * LAKH_TO_USD

print(df.head())
print(df.info())
print(df.isnull().sum())

#결측치 제거 
df.drop("Car_Name", axis=1, inplace=True)

#문자열 데이터를 숫자형으로 변환
label_encoders = {}

categorical_columns = ["Fuel_Type","Seller_Type","Transmission"]

for col in categorical_columns:
    encoder = LabelEncoder()
    df[col] = encoder.fit_transform(df[col])
    label_encoders[col] = encoder

#입력(X) / 정답(y)
X = df.drop("Selling_Price", axis=1)
y = df["Selling_Price"]

#학습용 데이터와 테스트용 데이터 분리
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=42)

#모델생성
model = RandomForestRegressor(n_estimators=100,random_state=42)

#모델학습
model.fit(X_train, y_train)

#모델예측
y_pred = model.predict(X_test)

#성능평가
print("=" * 50)
print("R2 Score :", r2_score(y_test, y_pred))
print("MAE :", mean_absolute_error(y_test, y_pred))
print("RMSE :", mean_squared_error(y_test, y_pred) ** 0.5)
print("=" * 50)

#모델저장
joblib.dump(model, "model.pkl")

joblib.dump(label_encoders, "label_encoders.pkl")

joblib.dump(list(X.columns), "feature_columns.pkl")

print("모델 저장 완료!")