import streamlit as st
from google.oauth2.service_account import Credentials
import gspread
import pandas as pd
from datetime import datetime
import pytz

# 🔍 주소를 직접 입력하지 않아도, 인터넷 창 주소에서 구글 시트 ID를 자동으로 추출하는 마법의 기능입니다.
def get_spreadsheet_url_from_query():
    query_params = st.query_params
    if "sheet_url" in query_params:
        return query_params["sheet_url"]
    return None

# 기본 연결 주소 설정
detected_url = get_spreadsheet_url_from_query()
if detected_url:
    SPREADSHEET_URL = detected_url
else:
    # 주소가 감지되지 않았을 때만 예시 주소를 사용합니다.
    SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMCEUiO_naNMIlevAIBADANBgkqhki9w0BA/edit"

def get_gspread_client():
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds_dict = dict(st.secrets["gcp_service_account"])
    return gspread.authorize(Credentials.from_service_account_info(creds_dict, scopes=scope))

try:
    gc = get_gspread_client()
    doc = gc.open_by_url(SPREADSHEET_URL)
    worksheet = doc.get_worksheet(0)
except Exception as e:
    st.title("📝 나만의 스마트 메모 앱")
    st.error("⚠️ 구글 시트와 앱이 아직 연결되지 않았습니다.")
    st.info("아래 빈칸에 질문자님의 [구글 시트 인터넷 주소]를 통째로 붙여넣고 엔터를 치시면 즉시 연결됩니다!")
    
    # 코드를 수정할 필요 없이, 앱 화면에서 직접 주소를 넣고 쓸 수 있는 안전장치입니다.
    input_url = st.text_input("https://docs.google.com/spreadsheets/d/1f68evGfSDpkplGOQFeOCYUpj_NV2U4E7zaPUM4HKGoI/edit?gid=0#gid=0:", value=SPREADSHEET_URL)
    if input_url and input_url != SPREADSSHEET_URL:
        st.query_params["sheet_url"] = input_url
        st.rerun()
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
