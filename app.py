import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 1. 앱 페이지 레이아웃 스마트폰 최적화
st.set_page_config(page_title="FreeRoad", page_icon="📍", layout="centered")

st.title("🚇 FreeRoad (자유로운 길)")
st.subheader("교통약자를 위한 경기도 배리어프리 실시간 지도")

# 2. 데이터셋 불러오기 함수 구동
@st.cache_data
def load_data():
    df = pd.read_csv("data.csv", encoding="cp949")
    df = df.dropna(subset=['시설위도', '시설경도'])
    return df

try:
    df = load_data()
    
    # 3. 경기도 시군명 필터링 UI 기능 활성화
    sigungu_list = ["전체"] + sorted(list(df['시군명'].unique()))
    selected_sigungu = st.selectbox("🔍 원하는 경기도 시/군을 선택하세요:", sigungu_list)
    
    if selected_sigungu != "전체":
        df = df[df['시군명'] == selected_sigungu]

    # 4. 지도 엔진 중심점 렌더링 최적화
    start_lat = df['시설위도'].mean()
    start_lon = df['시설경도'].mean()
    m = folium.Map(location=[start_lat, start_lon], zoom_start=11)

    # 5. 지도 레이어 위에 268개 시설 데이터 핀(Marker) 자동 매핑
    for idx, row in df.iterrows():
        popup_text = f"<b>{row['시설명']}</b><br>{row['시설기본주소']}<br>영업상태: {row['영업상태구분명']}"
        
        folium.Marker(
            location=[row['시설위도'], row['시설경도']],
            popup=folium.Popup(popup_text, max_width=300),
            tooltip=row['시설명'],
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(m)

    # 6. 인터페이스 렌더링 출력
    st_folium(m, width=350, height=450)
    
    st.success(f"현재 화면에 표시된 배리어프리 시설: {len(df)}개")

except Exception as e:
    st.error("데이터를 불러오는 중 오류가 발생했습니다. 파일명을 확인해주세요.")
