import pandas as pd
import plotly.express as px
import streamlit as st

# ------------------------------------------------------------
# 기본 설정
# ------------------------------------------------------------
st.set_page_config(page_title="영화 데이터 그래프 도감 1 - 시간", layout="wide")
st.title("영화 데이터 그래프 도감 1 - 시간")
st.caption("KOBIS 일별 박스오피스 데이터(최근 1년, 10위권)를 시간의 흐름 관점에서 살펴봅니다.")

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"


# ------------------------------------------------------------
# 데이터 로드
# ------------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)
    # 날짜 열(하이픈 없는 8자리 숫자, 예: 20250901)을 실제 날짜형으로 변환
    df["날짜"] = pd.to_datetime(df["날짜"], format="%Y%m%d")
    return df


df = load_data()

with st.expander("원본 데이터 미리보기"):
    st.dataframe(df.head(20), use_container_width=True)


# ==============================================================
# 구역 1. 영화별 일별 관객수 추이
# ==============================================================
st.header("1. 영화별 일별 관객수 추이")

movie_list = sorted(df["영화명"].unique())
selected_movie = st.selectbox("영화를 선택하세요", movie_list, key="movie_select_1")

movie_df = (
    df[df["영화명"] == selected_movie]
    .sort_values("날짜")
    .loc[:, ["날짜", "일관객"]]
)

fig1 = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    markers=True,
    title=f"'{selected_movie}' 일별 관객수 변화",
)
fig1.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>일일 관객수: %{y:,}명<extra></extra>"
)
fig1.update_layout(xaxis_title="날짜", yaxis_title="일일 관객수(명)")

st.plotly_chart(fig1, use_container_width=True)

st.info("**이 그래프로 알 수 있는 것:** (여기에 그래프 해석 문구를 작성하세요.)")


# ==============================================================
# 구역 2. 누적 관객 TOP 5 영화의 일별 관객수 비교
# ==============================================================
st.header("2. 누적 관객 TOP 5 영화의 일별 관객수 비교")

top5_movies = (
    df.groupby("영화명")["일관객"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .index
    .tolist()
)

top5_df = (
    df[df["영화명"].isin(top5_movies)]
    .sort_values("날짜")
    .loc[:, ["날짜", "영화명", "일관객"]]
)

fig2 = px.line(
    top5_df,
    x="날짜",
    y="일관객",
    color="영화명",
    markers=True,
    title="기간 내 일관객 합계 TOP 5 영화의 날짜별 일일 관객수",
)
fig2.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>일일 관객수: %{y:,}명<extra>%{fullData.name}</extra>"
)
fig2.update_layout(
    xaxis_title="날짜",
    yaxis_title="일일 관객수(명)",
    legend_title="영화명",
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="left",
        x=0,
    ),
    margin=dict(t=100),
)

st.plotly_chart(fig2, use_container_width=True)
st.caption("범례의 영화명을 클릭하면 해당 영화의 선을 켜고 끌 수 있습니다.")

st.info("**이 그래프로 알 수 있는 것:** (여기에 그래프 해석 문구를 작성하세요.)")


# ==============================================================
# 구역 3. 날짜별 10위권 전체 일관객 합계
# ==============================================================
st.header("3. 날짜별 10위권 전체 일관객 합계")

daily_total = (
    df.groupby("날짜")["일관객"]
    .sum()
    .reset_index()
    .sort_values("날짜")
)

top3_days = daily_total.sort_values("일관객", ascending=False).head(3)

fig3 = px.area(
    daily_total,
    x="날짜",
    y="일관객",
    title="날짜별 박스오피스 10위권 일관객 합계",
)
fig3.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>합계 관객수: %{y:,}명<extra></extra>"
)
fig3.update_layout(xaxis_title="날짜", yaxis_title="10위권 합계 관객수(명)")

# 합계가 가장 컸던 3일을 점과 날짜 라벨로 표시
fig3.add_scatter(
    x=top3_days["날짜"],
    y=top3_days["일관객"],
    mode="markers+text",
    text=top3_days["날짜"].dt.strftime("%Y-%m-%d"),
    textposition="top center",
    marker=dict(size=10, color="red", symbol="star"),
    name="합계 TOP 3일",
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>합계 관객수: %{y:,}명<extra>TOP 3</extra>",
)

st.plotly_chart(fig3, use_container_width=True)

st.info("**이 그래프로 알 수 있는 것:** (여기에 그래프 해석 문구를 작성하세요.)")
