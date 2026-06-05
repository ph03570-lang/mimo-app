import streamlit as st
import pandas as pd

st.title("나만의 메모 앱")

# 질문자님의 진짜 구글 시트 변환 주소입니다.
sheet_url = "https://docs.google.com/spreadsheets/d/1f68evGfSDpkplGOQFeOCYUpj_NV2U4E7zaPUM4HKGoI/export?format=csv"

# 어떤 메모를 수정 중인지 기억하는 저장소
if 'edit_mode_idx' not in st.session_state:
    st.session_state.edit_mode_idx = None

try:
    # 구글 시트 실시간으로 읽어오기
    df = pd.read_csv(sheet_url)
    
    # --- 🔍 검색 기능 ---
    search = st.text_input("메모 검색")
    if search:
        df = df[df['본문'].str.contains(search, na=False)]

    # --- 📋 메모 보여주기 및 수정 아이콘 배치 ---
    cols = st.columns(2)
    for index, row in df.iterrows():
        with cols[index % 2]:
            
            # 💡 수정 아이콘(✏️)을 눌렀을 때 나타나는 수정 창
            if st.session_state.edit_mode_idx == index:
                st.markdown("**✏️ 구글 시트 메모 복사 후 수정 중...**")
                edit_content = st.text_area("내용 고치기 (임시)", value=row['본문'], key=f"edit_{index}")
                
                btn_cols = st.columns(2)
                with btn_cols[0]:
                    if st.button("💾 반영", key=f"save_{index}"):
                        # 임시로 화면에만 반영 (진짜 저장은 구글 시트에서 직접 하시면 앱에 실시간 반영됩니다!)
                        df.at[index, '본문'] = edit_content
                        st.session_state.edit_mode_idx = None
                        st.rerun()
                with btn_cols[1]:
                    if st.button("❌ 취소", key=f"cancel_{index}"):
                        st.session_state.edit_mode_idx = None
                        st.rerun()
            
            # 💡 평소에 구글 시트 내용을 보여주는 화면
            else:
                # 1. 본문 출력
                st.write(f"{row['본문']}")
                
                # 2. 하단 정보창 (출처 | 작성일시 ✏️) 한 줄로 배치
                info_cols = st.columns([0.85, 0.15])
                with info_cols[0]:
                    # 구글 시트의 '작성일시' 칸에 적힌 날짜와 시간이 그대로 출력됩니다.
                    st.caption(f"{row['출처']} | {row['작성일시']}")
                with info_cols[1]:
                    # 날짜 바로 옆에 붙는 앙증맞은 ✏️ 아이콘 버튼
                    if st.button("✏️", key=f"pencil_{index}"):
                        st.session_state.edit_mode_idx = index
                        st.rerun()
                        
            st.write("---")

except Exception as e:
    st.error("구글 시트의 1번째 줄 이름이 [ID, 제목, 본문, 출처, 작성일시, 색상]으로 정확히 적혀있는지 확인해주세요!")
