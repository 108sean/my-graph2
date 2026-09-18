# ----------------------------------------------------
# 8. 개봉일 스크린수 vs 총 관객수 (색상: 10위권 머문 날수)
# ----------------------------------------------------
st.subheader("8. 개봉일 스크린수와 총 관객수의 관계")

fig8 = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    color="days_in_top10",
    hover_name="movieNm",
    color_continuous_scale="Viridis",
    title="개봉일 스크린수 vs 총 관객수 (색상: 10위권 머문 날수)",
    labels={
        "first_scrn": "개봉일 스크린수",
        "total_audi": "총 관객수",
        "days_in_top10": "10위권 머문 날수",
    },
)

fig8.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>개봉일 스크린수: %{x:,}개<br>총 관객수: %{y:,}명<br>10위권 유지: %{marker.color}일"
)

st.plotly_chart(fig8, use_container_width=True)

with st.container():
    st.markdown("### 💡 이 그래프로 알 수 있는 것")
    st.write(
        "개봉일 스크린수와 총 관객수가 높을 때 점의 색상이 밝을수록 10위권에 오래 머문 영화임을 한눈에 확인할 수 있습니다."
    )
