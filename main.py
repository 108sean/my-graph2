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

fig1.update_traces(
    hovertemplate="<b>%{label}</b><br>편수: %{value}편<br>비율: %{percent}"
)

st.plotly_chart(fig1, use_container_width=True)

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

df_tree = (
    df.groupby(["main_genre", "movieCd", "movieNm"], as_index=False)[
        "total_audi"
    ].sum()
)

fig2 = px.treemap(
    df_tree,
    path=["main_genre", "movieNm"],
    values="total_audi",
    title="장르별 영화 및 총 관객수 분포",
    color="main_genre",
)

fig2.update_traces(
    hovertemplate="<b>%{label}</b><br>총 관객수: %{value:,}명"
)

st.plotly_chart(fig2, use_container_width=True)

with st.container():
    st.markdown("### 💡 이 그래프로 알 수 있는 것")
    st.write(
        "장르 전체의 관객 규모뿐만 아니라, 특정 장르 내에서 어떤 영화가 흥행을 주도했는지(관객수 비중) 직관적으로 알 수 있습니다."
    )

st.write("")  # 여백 추가

# ----------------------------------------------------
# 3. 총 관객수 히스토그램
# ----------------------------------------------------
st.subheader("3. 총 관객수 분포 (히스토그램)")

fig3 = px.histogram(
    df,
    x="total_audi",
    nbins=30,
    title="총 관객수 구간별 영화 수 분포",
    labels={"total_audi": "총 관객수"},
)

fig3.update_traces(
    hovertemplate="관객수 구간: %{x}<br>영화 수: %{y}편"
)

st.plotly_chart(fig3, use_container_width=True)

top_movie = df.loc[df["total_audi"].idxmax()]
top_title = top_movie["movieNm"]
top_audi = top_movie["total_audi"]

with st.container():
    st.markdown("### 💡 이 그래프로 알 수 있는 것")
    st.write(
        f"대부분의 영화가 총 관객수 **100만 명 미만~200만 명 이하**의 하위 구간에 모여 있는 비대칭적 분포를 보이며, "
        f"가장 관객이 많은 영화는 **'{top_title}'**(약 {top_audi:,}명)입니다."
    )

st.write("")  # 여백 추가

# ----------------------------------------------------
# 4. 개봉일 스크린수 vs 총 관객수 산점도
# ----------------------------------------------------
st.subheader("4. 개봉일 스크린수와 총 관객수의 관계 (산점도)")

fig4 = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    color="main_genre",
    hover_name="movieNm",
    title="개봉일 스크린수 vs 총 관객수",
    labels={
        "first_scrn": "개봉일 스크린수",
        "total_audi": "총 관객수",
        "main_genre": "장르",
    },
)

fig4.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>개봉일 스크린수: %{x:,}개<br>총 관객수: %{y:,}명"
)

st.plotly_chart(fig4, use_container_width=True)

with st.container():
    st.markdown("### 💡 이 그래프로 알 수 있는 것")
    st.write(
        "개봉일 스크린수가 많을수록 대체로 총 관객수도 증가하는 양의 상관관계를 보이지만, 스크린수 대비 폭발적인 관객수를 기록한 흥행 상위 영화들도 확인할 수 있습니다."
    )

st.write("")  # 여백 추가

# ----------------------------------------------------
# 5. 주요 장르별 총 관객수 상자 그림 (박스플롯)
# ----------------------------------------------------
st.subheader("5. 주요 장르별 총 관객수 분포 (박스플롯)")

# 영화가 10편 이상인 장르만 추출
genre_counts_series = df["main_genre"].value_counts()
major_genres = genre_counts_series[genre_counts_series >= 10].index
df_major_genres = df[df["main_genre"].isin(major_genres)]

fig5 = px.box(
    df_major_genres,
    x="main_genre",
    y="total_audi",
    color="main_genre",
    points="outliers",  # 이상치 점 표시
    hover_name="movieNm",  # 이상치/점 마우스오버 시 영화명 표시
    title="주요 장르별(10편 이상) 총 관객수 박스플롯",
    labels={"main_genre": "장르", "total_audi": "총 관객수"},
)

fig5.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>총 관객수: %{y:,}명"
)

st.plotly_chart(fig5, use_container_width=True)

with st.container():
    st.markdown("### 💡 이 그래프로 알 수 있는 것")
    st.write(
        "주요 장르 간 중앙값의 차이와 흥행 편차를 비교할 수 있으며, 일반적인 범위(상자 내부)를 크게 벗어나 기록적인 관객수를 달성한 흥행 이상치(Outlier) 영화를 식별할 수 있습니다."
    )
