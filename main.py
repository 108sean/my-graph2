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
```<ElicitationsGroup message="추가로 구성할 기능이나 그래프가 있으신가요?">
  <Elicitation label="사이드바 필터(장르, 국가 선택) 구현하기" query="main.py에 사이드바를 추가해서 장르와 제작 국가를 필터링할 수 있도록 고쳐 줘."/>
  <Elicitation label="다섯 번째 그래프(상영횟수 vs 총관객 수) 추가하기" query="main.py에 first_show(개봉일 상영횟수)와 total_audi(총 관객수)의 관계를 보여주는 다섯 번째 그래프를 추가해 줘."/>
</ElicitationsGroup>
