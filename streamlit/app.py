#사용자 사용 화면(UI)
import os
import streamlit as st
import requests
from pathlib import Path
API_URL = os.getenv("API_URL","https://project-hdg3.onrender.com/predict")

#페이지설정
st.set_page_config(
    page_title="중고차 가격 예측 서비스",
    layout="wide",
    initial_sidebar_state="collapsed")

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
        ("Camry", "$24,000", IMAGE_DIR / "Camry.jpg")],

    (25000,50000):[
    ("Innova", "$32,000", IMAGE_DIR/"Innova.jpg"),
    ("Corolla Altis", "$27,000", IMAGE_DIR/"Corolla Altis.jpg"),
    ("Camry", "$35,000", IMAGE_DIR/"Camry.jpg"),
    ("Creta", "$29,000", IMAGE_DIR/"Creta.jpg")]}

#추천차량 함수
def recommend_car(price):

    for (low, high), cars in car_recommend.items():

        if low <= price < high:
            return cars

    return []   

#예측 결과에 따른 추천 차량 이미지 표시
def recommend_car(price):

    for (low, high), cars in car_recommend.items():

        if low <= price < high:
            return cars

    return []



# CSS
st.markdown("""
<style>

/* 전체 배경 */
.stApp{
    background:#f4f7fb;}

/* 상단 여백 */
.block-container{
    padding-top:2rem;
    padding-bottom:2rem;
    max-width:1200px;}

/* Hero */
.hero{

    background:linear-gradient(135deg,#2563eb,#4f46e5);
    border-radius:25px;
    padding:40px;
    color:white;
    text-align:center;
    margin-bottom:30px;
    box-shadow:0 10px 30px rgba(0,0,0,.15);}

.hero h1{
    font-size:42px;
    margin-bottom:8px;}

.hero p{
    font-size:20px;
    opacity:.95;}

/* 입력 카드 */
div[data-testid="stVerticalBlockBorderWrapper"]{
    background:white !important;
    border:none !important;
    border-radius:20px !important;
    padding:30px !important;
    box-shadow:0 6px 20px rgba(0,0,0,.08);}

/* Label */
label{
    font-size:18px !important;
    font-weight:700 !important;}

/* Number Input */
div[data-baseweb="input"] input{
    height:52px;
    border-radius:12px;
    font-size:18px;}

/* Select */
div[data-baseweb="select"]{font-size:18px;}

/* 버튼 */
.stButton>button{
    width:100%;
    height:55px;
    border:none;
    border-radius:14px;
    background:linear-gradient(90deg,#2563eb,#4f46e5);
    color:white;
    font-size:20px;
    font-weight:700;
    transition:.25s;}

.stButton>button:hover{
    transform:translateY(-2px);
    box-shadow:0 8px 20px rgba(37,99,235,.35);}

/* Success */
div[data-testid="stAlert"]{
    border-radius:15px;}

/* 간격 */
div[data-testid="stVerticalBlock"]{gap:20px;}

/* 결과 카드 Hover */
.result-card{
    transition:0.3s;}

.result-card:hover{
    transform:translateY(-5px);}

/* 차량 이미지 */

.stImage img{
    border-radius:18px;
    transition:0.3s;}

.stImage img:hover{
    transform:scale(1.03);}

/* AI 분석 카드 */

.ai-card{
    background:white;
    border-left:6px solid #2563eb;
    padding:25px;
    border-radius:18px;
    box-shadow:0 8px 18px rgba(0,0,0,.08);}

/* 추천 차량 카드 */

.car-card{
    background:white;
    border-radius:18px;
    padding:15px;
    box-shadow:0 8px 18px rgba(0,0,0,.08);
    transition:0.3s;}

.car-card:hover{
    transform:translateY(-6px);
    box-shadow:0 12px 30px rgba(0,0,0,.12);}

</style>
""", unsafe_allow_html=True)

#페이지 title 설정 
st.title("🚘 중고차 가격 예측 서비스")
st.write("중고차 정보를 입력하면 예상 가격을 예측합니다.")

# 입력 바탕
box = st.container(border=True)

with box:

    st.subheader("📝 차량 정보 입력")
    st.write("예측할 차량의 정보를 입력해주세요.")
    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        year = st.number_input("연식",min_value=1900,max_value=2023,value=2020)
        present_price = st.number_input("신차 가격 ($)",min_value=1000,value=12000,step=500)
        kms_driven = st.number_input("주행 거리 (km)",min_value=0,value=50000)
        owner = st.number_input("👤 이전 소유자 수",min_value=0,value=0)

    with col2:

        fuel_type = st.selectbox("⛽ 엔진 유형",["가솔린","디젤","CNG"])
        seller_type = st.selectbox("🏪 판매자 유형",["개인","딜러"])
        transmission = st.selectbox("⚙️ 변속기",["수동","자동"])

        st.write("")
        st.write("")
        st.write("")

        predict = st.button("AI 가격 예측하기",use_container_width=True)

# 예측 버튼
if predict:

    # 달러 → Lakh 변환
    present_price_lakh = round(present_price / 1180,2)

    # FastAPI 전송 데이터
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

        with st.spinner("🤖 AI가 차량 가격을 분석하는 중입니다..."):
            #api주소 상수화
            response = requests.post(API_URL,json=input_data)

        if response.status_code == 200:

            result = response.json()

            predicted_price = result["predicted_price"]

            analysis = result["analysis"]

            st.markdown("---")

            st.markdown(
                f"""
<div style="
background:linear-gradient(135deg,#2563eb,#4f46e5);
padding:30px;
border-radius:20px;
color:white;
text-align:center;
margin-bottom:20px;
">

<h3 style="margin-bottom:10px;">
💰 예측 가격
</h3>

<h1 style="font-size:52px;">
${round(predicted_price):,}
</h1>

<p>
{result["currency"]}
</p>

</div>
""",
                unsafe_allow_html=True)

            recommendations = recommend_car(predicted_price)

            # GPT 분석 
            st.markdown("## AI 차량 분석")
            st.markdown(
                f"""
<div class="ai-card">

{analysis}

</div>
""",
                unsafe_allow_html=True)


            # 추천 차량       
            if recommendations:
                st.markdown("## 추천 차량")
                cols = st.columns(len(recommendations))

                for col, (name, price, image) in zip(cols,recommendations):

                    with col:
                        if image.exists():
                            st.image(image,use_container_width=True)

                        else:
                            st.warning("이미지를 찾을 수 없습니다.")

                        st.markdown(
                            f"""
<div class="car-card">

<h3 style="font-size:24px;">
{name}
</h3>

<h2 style="
font-size:30px;
color:#2563eb;
margin-top:10px;
font-weight:700;
">
{price}
</h2>

</div>
""",
                            unsafe_allow_html=True)

            else:
                st.warning("추천 가능한 차량이 없습니다.")

        else:

            st.markdown(
                """
<div style="
background:#fff4f4;
border-left:6px solid #ef4444;
padding:20px;
border-radius:16px;
margin-top:20px;
">

<h3>❌ 예측 실패</h3>

<p>
서버에서 가격을 예측하지 못했습니다.<br>
FastAPI 서버 상태를 확인한 후 다시 시도해주세요.
</p>

</div>
""",
                unsafe_allow_html=True)

    except Exception as e:

        st.markdown(
            f"""
    <div style="
    background:#fff8e6;
    border-left:6px solid #f59e0b;
    padding:20px;
    border-radius:16px;
    margin-top:20px;
    ">

    <h3>⚠️ FastAPI 서버 연결 실패</h3>

    <p>
    localhost:8000 서버에 연결할 수 없습니다.
    </p>

    <hr>

    <p style="font-size:14px;color:#666;">
    {e}
    </p>

    </div>
    """,
            unsafe_allow_html=True)
            
st.markdown("---")

st.markdown(
    """
<div style="
text-align:center;
padding:20px;
color:#888;
font-size:15px;
">

🚗 AI Used Car Price Prediction System

<br>

Made with ❤️ using
<b>FastAPI</b>,
<b>Streamlit</b>,
<b>OpenAI GPT</b>

</div>
""",
    unsafe_allow_html=True)