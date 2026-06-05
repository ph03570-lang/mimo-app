import streamlit as st
import pandas as pd

st.title("나만의 메모 앱")

# 데이터 불러오기 (이미 연동된 시트 데이터 사용)
# 실제 서비스 시에는 여기서 시트 데이터를 다시 로드합니다.
data = [['ID', '제목', '본문', '출처', '작성일', '색상'], ['1', '앱 만들자', '전문이 잘 보입니다', '하영', '2026-06-05', '#FFD1DC']]
df = pd.DataFrame(data[1:], columns=data[0])

# 검색 기능
search = st.text_input("메모 검색")
if search:
    df = df[df['본문'].str.contains(search)]

# 2단 카드 레이아웃
cols = st.columns(2)
for index, row in df.iterrows():
    with cols[index % 2]:
        st.markdown(f"### {row['제목']}")
        st.write(f"{row['본문']}")
        st.caption(f"{row['출처']} | {row['작성일']}")
