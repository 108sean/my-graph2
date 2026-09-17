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

    # 장르 전처리: .str.split()을 사용하여 첫 번째 장르만 안전하게 추출
    df["main_genre"] = df["genre"].astype(str).str.split("|").str[0]
    return df


df = load_data()

# ----------------------------------------------------
# 1. 장르별 영화 편수 도넛 그래프
# ----------------------------------------------------
st.subheader("1. 장르별 영화 편수 분포")

# 장르별 편수 집계
genre_counts = df["main_genre"].value_counts().reset_index()
genre_counts.columns = ["장르", "편수"]

fig1 = px.pie(
    genre_counts,
    names="장르",
    values="편수",
    hole=0.4,
    hover_data=["편수"],
    title="장르별 영화 편수 비율",
)

# 마우스오버 시 편수와 비율이 함께 표시되도록 설정
fig1.update_traces(
    hovertemplate="<b>%{label}</b><br>편수: %{value}편<br>비율: %{percent}"
)

st.plotly_chart(fig1, use_container_width=True)

# 1번 그래프 설명 구역
with st.container():
    st.markdown("### 💡 이 그래프로 알 수 있는 것")
    st.write(
        "박스오피스 상위권 영화 중 특정 장르의 비중이 얼마나 큰지 한눈에 파악할 수 있으며, 시장에서 인기 있는 주요 장르 분포를 알 수 있습니다."
    )

st.write("")  # 여백 추가

# ----------------------------------------------------
# 2. 장르 및 영화별 총 관객수 트리맵 그래프
# ----------------------------------------------------
st.subheader("2. 장르 및 영화별 총 관객수 분포 (트리맵)")

# 중복 방지를 위한 영화코드(movieCd) 기준 그룹화 및 aggregation
df_tree = (
    df.groupby(["main_genre", "movieCd", "movieNm"], as_index=False)[
        "total_audi"
    ]
    .sum()
)

fig2 = px.treemap(
    df_tree,
    path=["main_genre", "movieNm"],  # 장르 -> 영화명 계층 구조
    values="total_audi",  # 칸 크기: 총 관객수
    title="장르별 영화 및 총 관객수 분포",
    color="main_genre",  # 장르별 색상 구분
)

# 마우스오버 시 영화명 및 총 관객수가 쉼표로 포맷팅되어 표시되도록 설정
fig2.update_traces(
    hovertemplate="<b>%{label}</b><br>총 관객수: %{value:,}명"
)

st.plotly_chart(fig2, use_container_width=True)

# 2번 그래프 설명 구역
with st.container():
    st.markdown("### 💡 이 그래프로 알 수 있는 것")
    st.write(
        "장르 전체의 관객 규모뿐만 아니라, 특정 장르 내에서 어떤 영화가 흥행을 주도했는지(관객수 비중) 직관적으로 알 수 있습니다."
    )
