import streamlit as st
import subprocess
import sys

# 🚀 에러를 일으키는 주범인 도구들을 강제로 자동 설치하는 마법의 코드입니다.
def install_packages():
    packages = ["gspread", "google-auth", "pandas", "pytz"]
    for package in packages:
        try:
            __import__(package)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install_packages()

# 이제 도구들이 다 설치되었으니 정상적으로 불러옵니다.
from google.oauth2.service_account import Credentials
import gspread
import pandas as pd
from datetime import datetime
import pytz

# 🛠️ 여기 따옴표 안에 질문자님의 진짜 구글 시트 주소를 붙여넣으세요!
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/질문자님의_시트_주소/edit"

def get_gspread_client():
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds_dict = dict(st.secrets["gcp_service_account"])
    return gspread.authorize(Credentials.from_service_account_info(creds_dict, scopes=scope))

try:
    gc = get_gspread_client()
    doc = gc.open_by_url(SPREADSHEET_URL)
    worksheet = doc.get_worksheet(0)
except Exception as e:
    st.error("구글 시트 주소를 확인하시거나, 복사한 이메일을 구글 시트에 '공유(편집자)' 했는지 확인해 주세요!")
    st.stop()

KST = pytz.timezone('Asia/Seoul')
st.title("📝 나만의 스마트 메모 앱")

# --- 메모 작성 칸 ---
st.subheader("🆕 새 메모 작성")
with st.form("memo_form", clear_on_submit=True):
    user_name = st.text_input("작성자 이름", placeholder="이름을 입력하세요")
    memo_content = st.text_area("메모 내용", placeholder="여기에 메모를 작성하세요...")
    if st.form_submit_button("메모 저장하기"):
        if user_name.strip() and memo_content.strip():
            now = datetime.now(KST)
            worksheet.append_row([user_name, now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S"), memo_content])
            st.success("성공적으로 저장되었습니다!")
            st.rerun()
        else:
            st.warning("이름과 내용을 모두 입력해 주세요!")

# --- 메모 목록 및 수정 ---
st.subheader("📂 저장된 메모 목록")
data = worksheet.get_all_values()
if len(data) > 1:
    df = pd.DataFrame(data[1:], columns=["이름", "날짜", "시간", "내용"])
    for idx in reversed(df.index):
        row = df.loc[idx]
        with st.container(border=True):
            st.markdown(f"**👤 {row['이름']}** │ 📅 {row['날짜']} │ ⏰ {row['시간']}")
            st.write(row['내용'])
            
            if st.button("✏️ 수정", key=f"edit_{idx}"):
                st.session_state[f"editing_{idx}"] = True
                
            if st.session_state.get(f"editing_{idx}", False):
                with st.form(key=f"edit_form_{idx}"):
                    e_name = st.text_input("이름 수정", value=row['이름'])
                    e_content = st.text_area("내용 수정", value=row['내용'])
                    col1, col2 = st.columns(2)
                    if col1.form_submit_button("💾 저장"):
                        now = datetime.now(KST)
                        worksheet.update(range_name=f"A{int(idx)+2}:D{int(idx)+2}", values=[[e_name, now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S"), e_content]])
                        st.session_state[f"editing_{idx}"] = False
                        st.rerun()
                    if col2.form_submit_button("❌ 취소"):
                        st.session_state[f"editing_{idx}"] = False
                        st.rerun()
else:
    st.info("아직 저장된 메모가 없습니다.")
