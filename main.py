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
# 구역 2. (다음 그래프를 위한 자리)
# ==============================================================
st.header("2. 다음 그래프 자리")
st.write("여기에 새로운 그래프를 추가할 예정입니다.")

# st.info("**이 그래프로 알 수 있는 것:** (여기에 그래프 해석 문구를 작성하세요.)")


# ==============================================================
# 구역 3. (다음 그래프를 위한 자리)
# ==============================================================
st.header("3. 다음 그래프 자리")
st.write("여기에 새로운 그래프를 추가할 예정입니다.")

# st.info("**이 그래프로 알 수 있는 것:** (여기에 그래프 해석 문구를 작성하세요.)")
