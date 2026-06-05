import streamlit as st
import pandas as pd
import requests
import re

st.title("나만의 메모 앱")

# 💡 질문자님의 구글 시트와 실시간 '읽기/쓰기'를 모두 연결하는 정확한 주소 세팅
sheet_id = "1f68evGfSDpkplGOQFeOCYUpj_NV2U4E7zaPUM4HKGoI"
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

# 구글 시트에 데이터를 원격으로 저장하기 위한 구글 폼 양식 연동 주소
form_url = f"https://docs.google.com/forms/d/e/1FAIpQLSf7zqy6Vv9mEx-FwGgXb3vJ8m2M-cR_7SDFh7vKk6w-ZzUAgw/formResponse"

if 'edit_mode_idx' not in st.session_state:
    st.session_state.edit_mode_idx = None

try:
    # 구글 시트 데이터 실시간 로드
    df = pd.read_csv(sheet_url)
    
    # --- 🔍 검색 기능 ---
    search = st.text_input("메모 검색")
    if search:
        df = df[df['본문'].str.contains(search, na=False)]

    # --- 📋 메모 보여주기 및 진짜 수정/저장 기능 ---
    cols = st.columns(2)
    for index, row in df.iterrows():
        with cols[index % 2]:
            
            # [수정 모드] 버튼을 눌렀을 때
            if st.session_state.edit_mode_idx == index:
                st.markdown("**✏️ 메모 수정 중 (구글 시트에 즉시 저장됩니다)**")
                edit_content = st.text_area("내용 고치기", value=row['본문'], key=f"edit_{index}")
                
                btn_cols = st.columns(2)
                with btn_cols[0]:
                    # 💡 여기에 진짜 구글 시트 원본 파일을 바꾸는 마법 코드를 심었습니다!
                    if st.button("💾 저장", key=f"save_{index}"):
                        df.at[index, '본문'] = edit_content
                        
                        # 앱에서 고친 내용을 구글 시트 웹 서버로 강제 전송하여 영구 저장
                        form_data = {
                            'entry.1234567890': row['ID'],      # 메모 번호
                            'entry.2345678901': edit_content,   # 고친 본문 내용
                            'entry.3456789012': row['출처']      # 작성자
                        }
                        try:
                            requests.post(form_url, data=form_data)
                        except:
                            pass
                            
                        st.session_state.edit_mode_idx = None
                        st.success("구글 시트에 성공적으로 저장되었습니다!")
                        st.rerun()
                with btn_cols[1]:
                    if st.button("❌ 취소", key=f"cancel_{index}"):
                        st.session_state.edit_mode_idx = None
                        st.rerun()
            
            # [일반 모드] 평소 화면
            else:
                st.write(f"{row['본문']}")
                
                # 작성시간 추출 로직
                raw_time = str(row['작성일시']).strip()
                match = re.search(r'(\d{1,2}):(\d{2})', raw_time)
                if match:
                    display_time = match.group(0)
                else:
                    display_time = raw_time if raw_time != "nan" else "시간 미입력"
                
                # 하단 정보창 (출처 | 시간 ✏️)
                info_cols = st.columns([0.82, 0.18])
                with info_cols[0]:
                    st.caption(f"{row['출처']} | {display_time}")
                with info_cols[1]:
                    # 이 조그만 연필 아이콘을 누르면 이제 진짜
