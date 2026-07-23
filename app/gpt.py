from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    base_url=os.getenv("OPENAI_BASE_URL"),
    api_key=os.getenv("OPENAI_API_KEY")
)


def analyze_price(
    predicted_price,
    year,
    present_price,
    kms_driven,
    fuel_type,
    seller_type,
    transmission,
    owner,
):

    prompt = f"""
예측된 중고차 가격은 {predicted_price:.0f} USD 입니다.

차량 정보
- 연식 : {year}
- 신차가격 : {present_price} USD
- 주행거리 : {kms_driven} km
- 연료 : {fuel_type}
- 판매자 : {seller_type}
- 변속기 : {transmission}
- 이전소유자 : {owner}명

다음 내용을 한국어로 5줄 정도 작성해주세요.

1. 예측 가격 설명
2. 가격이 높은 이유 또는 낮은 이유
3. 구매 추천 여부
"""

    response = client.chat.completions.create(
        model="openai/gpt-5-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content