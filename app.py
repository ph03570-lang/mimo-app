import streamlit as st
import pandas as pd
import re

st.title("나만의 메모 앱")

# 질문자님의 진짜 구글 시트 주소입니다.
sheet_url = "https://docs.google.com/spreadsheets/d/1f68evGfSDpkplGOQFeOCYUpj_NV2U4E7zaPUM4HKGoI/export?format=csv"

if 'edit_mode_idx' not in st.session_state:
    st.session_state.edit_mode_idx = None

try:
    # 구글 시트 데이터 실시간 로드
    df = pd.read_csv(sheet_url)
    
    # --- 🔍 검색 기능 ---
    search = st.text_input("메모 검색")
    if search:
        df = df[df['본문'].str.contains(search, na=False)]

    # --- 📋 메모 보여주기 및 수정 기능 ---
    cols = st.columns(2)
    for index, row in df.iterrows():
        with cols[index % 2]:
            
            # [수정 모드] 버튼을 눌렀을 때
            if st.session_state.edit_mode_idx == index:
                st.markdown("**✏️ 내용 수정 중...**")
                edit_content = st.text_area("내용 고치기", value=row['본문'], key=f"edit_{index}")
                
                btn_cols = st.columns(2)
                with btn_cols[0]:
                    if st.button("💾 저장", key=f"save_{index}"):
                        df.at[index, '본문'] = edit_content
                        st.session_state.edit_mode_idx = None
                        st.success("수정이 완료되었습니다!")
                        st.rerun()
                with btn_cols[1]:
                    if st.button("❌ 취소", key=f"cancel_{index}"):
                        st.session_state.edit_mode_idx = None
                        st.rerun()
            
            # [일반 모드] 평소 화면
            else:
                # 1. 본문 출력
                st.write(f"{row['본문']}")
                
                # 2. 구글 시트의 '작성일시' 칸에서 [시:분] 추출하기
                raw_time = str(row['작성일시']).strip()
                match = re.search(r'(\d{1,2}):(\d{2})', raw_time)
                if match:
                    display_time = match.group(0)
                else:
                    display_time = raw_time if raw_time != "nan" else "시간 미입력"
                
                # 3. 하단 정보창 (출처 | 시간 ✏️) 배치 (에러 났던 들여쓰기를 완벽히 고쳤습니다!)
                info_cols = st.columns([0.82, 0.18])
                with info_cols[0]:
                    st.caption(f"{row['출처']} | {display_time}")
                with info_cols[1]:
                    if st.button("✏️", key=f"pencil_{index}"):
                        st.session_state.edit_mode_idx = index
                        st.rerun()
                        
            st.write("---")

except Exception as e:
    st.error("구글 시트 연결 오류 또는 첫 줄 이름 문제 발생!")
