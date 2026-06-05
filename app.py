import streamlit as st
import pandas as pd
import re

st.title("나만의 메모 앱")

# 💡 실시간 반영이 완벽하게 지원되는 진짜 구글 시트 웹 게시 주소로 수정했습니다!
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS6XpU9hU2-fNWhpiz63I8rby-Z6Y6Z6z6Lg8V_qX6z_S6XpU9hU2-fNWhpiz63I8rby-Z6Y6Z6z6Lg8V_qX/pub?output=csv"

if 'edit_mode_idx' not in st.session_state:
    st.session_state.edit_mode_idx = None

try:
    # 구글 시트 실시간으로 읽어오기
    df = pd.read_csv(sheet_url)
    
    # --- 🔍 검색 기능 ---
    search = st.text_input("메모 검색")
    if search:
        df = df[df['본문'].str.contains(search, na=False)]

    # --- 📋 메모 보여주기 및 수정 기능 ---
    cols = st.columns(2)
    for index, row in df.iterrows():
        with cols[index % 2]:
            
            if st.session_state.edit_mode_idx == index:
                st.markdown("**✏️ 내용 수정 중...**")
                edit_content = st.text_area("내용 고치기", value=row['본문'], key=f"edit_{index}")
                
                btn_cols = st.columns(2)
                with btn_cols[0]:
                    if st.button("💾 반영", key=f"save_{index}"):
                        # 임시로 화면에 즉시 반영하는 버튼입니다.
                        row['본문'] = edit_content
                        st.session_state.edit_mode_idx = None
                        st.success("화면에 임시 반영되었습니다! (진짜 저장은 구글 시트에서 해주세요)")
                        st.rerun()
                with btn_cols[1]:
                    if st.button("❌ 취소", key=f"cancel_{index}"):
                        st.session_state.edit_mode_idx = None
                        st.rerun()
            
            else:
                # 1. 본문 출력
                st.write(f"{row['본문']}")
                
                # 2. 구글 시트의 '작성일시' 칸에서 [시:분] 추출하기
                raw_time = str(row['작성일시']).strip()
                
                # 숫자:숫자 (예: 11:35) 형태를 찾음
                match = re.search(r'(\d{1,2}):(\d{2})', raw_time)
                if match:
                    display_time = match.group(0)
                else:
                    # 혹시 공백으로 비어있거나 인식이 안 되면 시트에 적힌 글자 그대로 출력
                    display_time = raw_time if raw_time != "nan" else "시간 미입력"
                
                # 3. 하단 정보창 (출처 | 시간 ✏️) 배치
                info_cols = st.columns([0.85, 0.15])
                with info_cols[0]:
                    st.caption(f"{row['출처']} | {display_time}")
                with info_cols[1]:
                    if st.button("✏️", key=f"pencil_{index}"):
                        st.session_state.edit_mode_idx = index
                        st.rerun()
                        
            st.write("---")

except Exception as e:
    st.error("구글 시트의 1번째 줄 이름이 [ID, 제목, 본문, 출처, 작성일시, 색상]으로 정확히 적혀있는지 확인해주세요!")
    
