import streamlit as st
import pandas as pd

st.title("나만의 메모 앱")

# 주소 끝자리를 pub?output=csv로 완벽하게 수정한 주소입니다.
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR1Yy_jU2wW-g-E787Xz8D32f0n6vR0z_Wv9-G2Z-vV6y-X/pub?output=csv"

try:
    # 구글 시트 데이터를 실시간으로 읽어오는 코드
    df = pd.read_csv(sheet_url)
    
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
    st.error("구글 시트 주소를 올바르게 입력했는지, 혹은 시트의 열 이름(ID, 제목, 본문, 출처, 작성일, 색상)이 정확한지 확인해주세요!")
