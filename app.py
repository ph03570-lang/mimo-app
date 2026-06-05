import streamlit as st
import pandas as pd
from datetime import datetime

st.title("나만의 메모 앱")

# 앱 내부 메모리에 임시 저장 공간 만들기 (기본 예시에 시간 정보 추가)
if 'memo_list' not in st.session_state:
    st.session_state.memo_list = [
        {"제목": "앱 만들자", "본문": "내 생각메모 정리하고싶어", "출처": "하영", "작성일": "2026-06-05 11:14"}
    ]

# 어떤 메모를 수정 중인지 기억하는 저장소
if 'edit_mode_idx' not in st.session_state:
    st.session_state.edit_mode_idx = None

# --- ✍️ 새 메모 작성 칸 ---
with st.expander("📝 새 메모 작성하기 (여기를 눌러 펼치세요)", expanded=False):
    with st.form("memo_form", clear_on_submit=True):
        new_title = st.text_input("제목 (메모를 구별할 이름)")
        new_content = st.text_area("본문 내용")
        new_author = st.text_input("작성자(출처)", value="하영")
        
        submitted = st.form_submit_button("메모 저장하기")
        if submitted:
            if new_title and new_content:
                # 💡 날짜 뒤에 시:분(예: 2026-06-05 11:14)까지 자동 기록하도록 변경
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
                st.session_state.memo_list.append({
                    "제목": new_title,
                    "본문": new_content,
                    "출처": new_author,
                    "작성일": current_time
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
        
        # 💡 현재 수정 모드일 때의 화면
        if st.session_state.edit_mode_idx == original_idx:
            st.markdown("**✏️ 메모 수정 중...**")
            edit_content = st.text_area("본문 고치기", value=memo['본문'], key=f"direct_edit_{original_idx}")
            
            btn_cols = st.columns(2)
            with btn_cols[0]:
                if st.button("💾 저장", key=f"save_btn_{original_idx}"):
                    st.session_state.memo_list[original_idx]['본문'] = edit_content
                    # 수정 완료 시점의 시간으로 업데이트하고
