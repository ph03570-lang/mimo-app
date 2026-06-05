import streamlit as st
from google.oauth2.service_account import Credentials
import gspread
import pandas as pd
from datetime import datetime
import pytz

# 1. 구글 시트 연동 설정
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/질문자님의_시트_주소/edit"

def get_gspread_client():
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    # Streamlit Secrets에 저장한 가상 직원 열쇠를 가져옵니다
    creds_dict = dict(st.secrets["gcp_service_account"])
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    return gspread.authorize(creds)

try:
    gc = get_gspread_client()
    doc = gc.open_by_url(SPREADSHEET_URL)
    worksheet = doc.get_worksheet(0)
except Exception as e:
    st.error(f"구글 시트 연결 실패. 공유 설정이나 주소를 확인하세요: {e}")
    st.stop()

# 한국 시간 설정
KST = pytz.timezone('Asia/Seoul')

st.title("📝 나만의 스마트 메모 앱")

# --- 기능 1: 메모 작성 창 ---
st.subheader("🆕 새 메모 작성")
with st.form("memo_form", clear_on_submit=True):
    user_name = st.text_input("작성자 이름", placeholder="이름을 입력하세요")
    memo_content = st.text_area("메모 내용", placeholder="여기에 메모를 작성하세요...")
    submit_btn = st.form_submit_submit("메모 저장하기")
    
    if submit_btn:
        if user_name.strip() == "" or memo_content.strip() == "":
            st.warning("이름과 내용을 모두 입력해 주세요!")
        else:
            # 현재 날짜와 시간 분리하여 생성
            now = datetime.now(KST)
            current_date = now.strftime("%Y-%m-%d")
            current_time = now.strftime("%H:%M:%S")
            
            # 구글 시트에 행 추가 (이름, 날짜, 시간, 내용)
            worksheet.append_row([user_name, current_date, current_time, memo_content])
            st.success("구글 시트에 메모가 안전하게 저장되었습니다!")
            st.rerun()

# --- 기능 2 & 3: 메모 목록 표시 및 수정 ---
st.subheader("📂 저장된 메모 목록 (구글 시트 동기화)")

# 구글 시트에서 데이터 읽어오기
data = worksheet.get_all_values()
if len(data) <= 1:
    st.info("아직 저장된 메모가 없습니다. 첫 메모를 작성해 보세요!")
else:
    # 첫 줄을 제목(이름, 날짜, 시간, 내용)으로 하여 데이터프레임 생성
    df = pd.DataFrame(data[1:], columns=["이름", "날짜", "시간", "내용"])
    
    # 역순으로 배치 (최신 메모가 위로 오도록)
    for idx in reversed(df.index):
        row = df.loc[idx]
        
        with st.container(border=True):
            col1, col2 = st.columns([8, 2])
            
            with col1:
                st.markdown(f"**👤 {row['이름']}** │ 📅 {row['날짜']} │ ⏰ {row['시간']}")
                st.write(row['내용'])
            
            with col2:
                # 수정 버튼 아이콘
                if st.button("✏️ 수정", key=f"edit_{idx}"):
                    st.session_state[f"editing_{idx}"] = True
            
            # 수정 활성화 창
            if st.session_state.get(f"editing_{idx}", False):
                with st.form(key=f"edit_form_{idx}"):
                    edit_name = st.text_input("이름 수정", value=row['이름'])
                    edit_content = st.text_area("내용 수정", value=row['내용'])
                    
                    save_col, cancel_col = st.columns(2)
                    with save_col:
                        if st.form_submit_button("💾 저장"):
                            # 수정된 시간으로 업데이트 원할 시 아래 주석 해제
                            now = datetime.now(KST)
                            row['날짜'] = now.strftime("%Y-%m-%d")
                            row['시간'] = now.strftime("%H:%M:%S")
                            
                            # 구글 시트의 실제 행 위치 (행 번호는 index + 2)
                            sheet_row_num = int(idx) + 2
                            worksheet.update(range_name=f"A{sheet_row_num}:D{sheet_row_num}", 
                                             values=[[edit_name, row['날짜'], row['시간'], edit_content]])
                            
                            st.session_state[f"editing_{idx}"] = False
                            st.success("메모가 수정되었습니다!")
                            st.rerun()
                    with cancel_col:
                        if st.form_submit_button("❌ 취소"):
                            st.session_state[f"editing_{idx}"] = False
                            st.rerun()
