import streamlit as st
import pandas as pd
from datetime import datetime

st.title("나만의 메모 앱")

# 앱 내부 메모리에 임시 저장 공간 만들기
if 'memo_list' not in st.session_state:
    st.session_state.memo_list = [
        {"제목": "앱 만들자", "본문": "내 생각메모 정리하고싶어", "출처": "하영", "작성일": "2026-06-05"}
    ]

# --- ✍️ 앱 화면에서 메모 입력하는 칸 ---
st.subheader("📝 새 메모 작성하기")
with st.form("memo_form", clear_on_submit=True):
    new_title = st.text_input("제목")
    new_content = st.text_area("본문")
    new_author = st.text_input("작성자(출처)", value="하영")
    
    # [메모 저장하기] 버튼
    submitted = st.form_submit_button("메모 저장하기")
    if submitted:
        if new_title and new_content:
            # 현재 날짜 자동으로 넣기
            current_date = datetime.now().strftime("%Y-%m-%d")
            # 입력한 내용을 저장 공간에 추가
            st.session_state.memo_list.append({
                "제목": new_title,
                "본문": new_content,
                "출처": new_author,
                "작성일": current_date
            })
            st.success("메모가 성공적으로 저장되었습니다!")
        else:
            st.error("제목과 본문을 모두 입력해 주세요!")

st.write("---")

# --- 🔍 검색 및 메모 보여주기 칸 ---
df = pd.DataFrame(st.session_state.memo_list)

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
