import streamlit as st
import pandas as pd
from datetime import datetime

st.title("나만의 메모 앱")

# 앱 내부 메모리에 임시 저장 공간 만들기
if 'memo_list' not in st.session_state:
    st.session_state.memo_list = [
        {"제목": "앱 만들자", "본문": "내 생각메모 정리하고싶어", "출처": "하영", "작성일": "2026-06-05"}
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

# --- 📋 메모 보여주기 및 바로 수정 기능 ---
filtered_memos = []
for idx, memo in enumerate(st.session_state.memo_list):
    if search and search not in memo['본문']:
        continue
    filtered_memos.append((idx, memo))

# 2단 카드 레이아웃으로 메모 출력하기
cols = st.columns(2)
for display_idx, (original_idx, memo) in enumerate(filtered_memos):
    with cols[display_idx % 2]:
        
        # 💡 현재 이 메모가 "수정 모드" 상태라면? -> 바로 글자 입력창을 보여줌
        if st.session_state.edit_mode_idx == original_idx:
            st.markdown("**✏️ 메모 수정 중...**")
            edit_content = st.text_area("본문 고치기", value=memo['본문'], key=f"direct_edit_{original_idx}")
            
            # [저장]과 [취소] 버튼을 나란히 배치
            btn_cols = st.columns(2)
            with btn_cols[0]:
                if st.button("💾 저장", key=f"save_btn_{original_idx}"):
                    st.session_state.memo_list[original_idx]['본문'] = edit_content
                    st.session_state.edit_mode_idx = None  # 수정 모드 종료
                    st.rerun()
            with btn_cols[1]:
                if st.button("❌ 취소", key=f"cancel_btn_{original_idx}"):
                    st.session_state.edit_mode_idx = None  # 수정 없이 종료
                    st.rerun()
                    
        # 💡 평소 상태라면? -> 본문 글씨와 함께 우측에 [✏️] 버튼을 보여줌
        else:
            # 본문 내용과 수정 아이콘 버튼을 깔끔하게 한 줄로 배치
            memo_cols = st.columns([0.85, 0.15])
            with memo_cols[0]:
                st.write(f"{memo['본문']}")
            with memo_cols[1]:
                # 연필 아이콘 버튼을 누르면 수정 모드로 변신!
                if st.button("✏️", key=f"pencil_icon_{original_idx}"):
                    st.session_state.edit_mode_idx = original_idx
                    st.rerun()
                    
            st.caption(f"{memo['출처']} | {memo['작성일']}")
            
        st.write("---") # 메모 간 구별선
