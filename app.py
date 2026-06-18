import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 페이지 기본 설정
st.set_page_config(page_title="FreeRoad", page_icon="📍")
st.title("🚇 FreeRoad (자유로운 길)")
st.subheader("교통약자를 위한 경기도 배리어프리 실시간 지도")

try:
    # 가장 원초적인 방식으로 데이터 호출
    df = pd.read_csv("data.csv")
    df = df.dropna(subset=['시설위도', '시설경도'])
    
    # 지도 중심점 잡기
    m = folium.Map(location=[df['시설위도'].mean(), df['시설경도'].mean()], zoom_start=11)

    # 핀 꽂기 루프 연산
    for idx, row in df.iterrows():
        popup_text = f"<b>{row['시설명']}</b><br>{row['시설기본주소']}"
        folium.Marker(
            location=[row['시설위도'], row['시설경도']],
            popup=folium.Popup(popup_text, max_width=300),
            tooltip=row['시설명']
        ).add_to(m)

    # 화면에 지도 출력
    st_folium(m, width=350, height=450)
    st.success(f"성공적으로 로드된 시설: {len(df)}개")

except Exception as e:
    st.error(f"오류 추적 메세지: {e}")
