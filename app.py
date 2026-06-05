import streamlit as st
import pandas as pd
from datetime import datetime

st.title("나만의 메모 앱")

# 앱 내부 메모리에 임시 저장 공간 만들기
if 'memo_list' not in st.session_state:
    st.session_state.memo_list = [
        {"제목": "앱 만들자", "본문": "내 생각메모 정리하고싶어", "출처": "하영", "작성일": "2026-06-05"}
    ]

# --- ✍️ 새 메모 작성 칸 ---
with st.expander("📝 새 메모 작성하기 (여기를 눌러 펼치세요)", expanded=False):
    with st.form("memo_form", clear_on_submit=True):
        new_title = st.text_input("제목 (메모를 구별할 이름)")
        new_content = st.text_area("본문 내용")
        new_author = st.text_input("작성자(출처)", value="하영")
        
        submitted = st.form_submit_button("메모 저장하기")
        if submitted:
            if new_title and new_content:
                current_date = datetime.now().strftime("%Y-%m-%d")
                st.session_state.memo_list.append({
                    "제목": new_title,
                    "본문": new_content,
                    "출처": new_author,
                    "작성일": current_date
                })
                st.rerun()
            else:
                st.error("제목과 본문을 모두 입력해 주세요!")

st.write("---")

# --- 🔍 검색 기능 ---
search = st.text_input("메모 검색")

# --- 📋 메모 보여주기 및 수정 기능 ---
filtered_memos = []
for idx, memo in enumerate(st.session_state.memo_list):
    if search and search not in memo['본문']:
        continue
    filtered_memos.append((idx, memo))

# 2단 카드 레이아웃으로 메모 출력하기
cols = st.columns(2)
for display_idx, (original_idx, memo) in enumerate(filtered_memos):
    with cols[display_idx % 2]:
        st.write(f"{memo['본문']}")
        st.caption(f"{memo['출처']} | {memo['작성일']}")
        
        # 🛠️ 각 메모별 개별 수정 칸 (괄호 오타를 완벽하게 고쳤습니다!)
        with st.expander("✏️ 이 메모 수정하기", expanded=False):
            edit_content = st.text_area("본문 수정", value=memo['본문'], key=f"edit_content_{original_idx}")
            edit_author = st.text_input("작성자 수정", value=memo['출처'], key=f"edit_author_{original_idx}")
            
            if st.button("수정 완료", key=f"edit_btn_{original_idx}"):
                st.session_state.memo_list[original_idx]['본문'] = edit_content
                st.session_state.memo_list[original_idx]['출처'] = edit_author
                st.success("수정되었습니다!")
                st.rerun()
        st.write("")
