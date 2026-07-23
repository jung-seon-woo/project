#백업
#사용자 사용 화면(UI)
import streamlit as st
import requests
import random
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent
IMAGE_DIR = BASE_DIR / "images"

car_recommend = {
    (0,5000):[
        ("Alto 800", "$3,500", IMAGE_DIR / "Alto 800.jpg"),
        ("Wagon R", "$4,500", IMAGE_DIR / "Wagon R.jpg")],

    (5000,9000):[
        ("Swift", "$7,500", IMAGE_DIR / "Swift.jpg"),
        ("Baleno", "$8,500",IMAGE_DIR / "Baleno.jpg")],

    (9000,13000):[
        ("i20", "$9,500", IMAGE_DIR / "i20.jpg"),
        ("Ciaz", "$11,500", IMAGE_DIR / "Ciaz.jpg")],

    (13000,18000):[
        ("Verna", "$15,500", IMAGE_DIR / "Verna.jpg"),
        ("Creta", "$17,000", IMAGE_DIR / "Creta.jpg")],

    (18000,25000):[
        ("Corolla Altis", "$21,000", IMAGE_DIR / "Corolla Altis.jpg"),
        ("camry", "$24,000", IMAGE_DIR / "camry.jpg")],

    (25000,50000):[
    ("Innova", "$32,000", IMAGE_DIR/"Innova.jpg"),
    ("Corolla Altis", "$27,000", IMAGE_DIR/"Corolla Altis.jpg"),
    ("Camry", "$35,000", IMAGE_DIR/"camry.jpg"),
    ("Creta", "$29,000", IMAGE_DIR/"Creta.jpg")]}

#예측 결과에 따른 추천 차량 이미지 표시
def recommend_car(price):

    for (low, high), cars in car_recommend.items():

        if low <= price < high:
            return cars

    return []



# CSS
st.markdown("""
<style>

/* 입력창 */
div[data-baseweb="input"] input{
    height:55px;
    font-size:20px;}

/* 선택박스 */
div[data-baseweb="select"]{
    font-size:20px;}

/* Label(연식, 신차 가격...) */
label{
    font-size:20px !important;
    font-weight:bold !important;}

/* 버튼 */
.stButton>button{
    width:100%;
    height:55px;
    font-size:20px;
    font-weight:bold;
    background:#ff6b00;
    color:white;
    border:none;
    border-radius:0px;}

.stButton>button:hover{
    background:#e85f00;
    color:white;}

/* 박스 */
div[data-testid="stVerticalBlockBorderWrapper"]{
    border:5px solid #000000 !important;
    border-radius:0px !important;
    padding:25px !important;
    background:white !important;
    box-shadow:none !important;}


div[data-testid="stVerticalBlock"]{gap:18px;}
</style>
""", unsafe_allow_html=True)

#페이지 title 설정 
st.title("🚘 중고차 가격 예측 서비스")
st.write("중고차 정보를 입력하면 예상 가격을 예측합니다.")

# 사용자 입력
box = st.container(border=True)

with box:

    col1, col2, col3, col4 = st.columns(4)


    with col1:
        year = st.number_input("연식", min_value=1900, max_value=2023, value=2020)

    with col2:
        present_price = st.number_input("신차 가격 ($)",min_value=1000,value=12000,step=500,)
        esent_price_lakh = round(present_price / 1180, 2)

    with col3:
        kms_driven = st.number_input("주행 거리",min_value=0,value=50000)

    with col4:
        st.markdown("<br>", unsafe_allow_html=True)

        predict = st.button("🔍 예측",use_container_width=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        fuel_type = st.selectbox("엔진 유형",["가솔린", "디젤", "CNG"])

    with col2:
        seller_type = st.selectbox("판매자 유형",["개인", "딜러"])

    with col3:
        transmission = st.selectbox("변속기 유형",["수동", "자동"])

    with col4:
        owner = st.number_input("이전 소유자 수",min_value=0,value=0)
        st.markdown("</div>", unsafe_allow_html=True)

# 예측 버튼
if predict:
    # 달러 → Lakh 변환
    present_price_lakh = round(present_price / 1180, 2)

    # 입력 데이터를 딕셔너리로 변환
    input_data = {
        "Year": year,
        "Present_Price": present_price_lakh,
        "Kms_Driven": kms_driven,
        "Fuel_Type": fuel_type,
        "Seller_Type": seller_type,
        "Transmission": transmission,
        "Owner": owner
}

    try:
        # FastAPI 서버에 요청 보내기
        response = requests.post("http://localhost:8000/predict",json=input_data) 

        if response.status_code == 200:

            result = response.json()
            analysis = result["analysis"]
            predicted_price = result["predicted_price"]

            st.success(f"예상 중고차 가격 : ${round(predicted_price)} {result['currency']}")

            # GPT 분석 출력
            st.markdown("---")
            st.subheader("🤖 AI 차량 분석")
            st.info(analysis)


            recommendations = recommend_car(predicted_price)

            if recommendations:

                st.markdown("---")
                st.subheader("🚗 예측 가격에 맞는 추천 차량")

                cols = st.columns(len(recommendations))

                for col, (name, price, image) in zip(cols, recommendations):

                    with col:
                        st.image(image, use_container_width=True)
                        st.markdown(
                            f"""
                            <div style="text-align:center;">
                                <h3>{name}</h3>
                                <p style="color:#ff6b00;font-size:22px;font-weight:bold;">
                                    {price}
                                </p>
                            </div>
                            """,
                            unsafe_allow_html=True)
            

            else:
                st.info("해당 가격대의 추천 차량이 없습니다.")

        else:
            st.error("예측에 실패했습니다. 서버를 확인하세요.")

    except Exception as e:
        st.error("FastAPI 서버와 연결할 수 없습니다.")
        st.write(e)