import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="영화 데이터 그래프 도감 2", layout="wide")

st.title("영화 데이터 그래프 도감 2 - 분포와 관계")


# 데이터 불러오기 및 전처리
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)

    # 장르 전처리: 세로막대 기호(|)로 여러 개 적힌 경우 첫 번째 장르만 추출
    df["main_genre"] = df["genre"].astype(str).apply(lambda x: x.split("|")[0])
    return df


df = load_data()

# 1. 장르별 영화 편수 도넛 그래프
st.subheader("1. 장르별 영화 편수 분포")

# 장르별 편수 집계
genre_counts = df["main_genre"].value_counts().reset_index()
genre_counts.columns = ["장르", "편수"]

fig = px.pie(
    genre_counts,
    names="장르",
    values="편수",
    hole=0.4,
    hover_data=["편수"],
    title="장르별 영화 편수 비율",
)

# 마우스오버 시 편수와 비율이 함께 표시되도록 설정
fig.update_traces(hovertemplate="<b>%{label}</b><br>편수: %{value}편<br>비율: %{percent}")

st.plotly_chart(fig, use_container_width=True)

st.divider()

# 그래프 아래 설명 구역
with st.container():
    st.markdown("### 💡 이 그래프로 알 수 있는 것")
    st.write(
        "박스오피스 상위권 영화 중 특정 장르(예: 드라마다 드라마/액션 등)의 비중이 얼마나 큰지 한눈에 파악할 수 있으며, 시장에서 인기 있는 주요 장르 분포를 알 수 있습니다."
    )
