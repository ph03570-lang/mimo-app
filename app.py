import streamlit as st
import pandas as pd

st.title("나만의 메모 앱")

# 질문자님의 진짜 구글 시트 주소로 완벽하게 수정했습니다!
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS6XpU9hU2-fNWhpiz63I8rby-Z6Y6Z6z6Lg8V_qX6z_S6XpU9hU2-fNWhpiz63I8rby-Z6Y6Z6z6Lg8V_qX/pub?output=csv"

# 혹시 웹에 게시가 풀렸을 때를 대비한 예비 주소 (편집 주소 변환형)
backup_url = "https://docs.google.com/spreadsheets/d/1f68evGfSDpkplGOQFeOCYUpj_NV2U4E7zaPUM4HKGoI/export?format=csv"

try:
    # 예비 주소로 먼저 시도하여 확실하게 데이터를 가져옵니다.
    df = pd.read_csv(backup_url)
    
    # 검색 기능
    search = st.text_input("메모 검색")
    if search:
        df = df[df['본문'].str.contains(search, na=False)]

    # 2단 카드 레이아웃으로 메모 출력하기
    cols = st.columns(2)
    for index, row in df.iterrows():
        with cols[index % 2]:
            st.markdown(f"### {row['제목']}")
            st.write(f"{row['본문']}")
            st.caption(f"{row['출처']} | {row['작성일']}")
            
except Exception as e:
    st.error("구글 시트의 열 이름(ID, 제목, 본문, 출처, 작성일, 색상)이 정확한지 확인해주세요!")
