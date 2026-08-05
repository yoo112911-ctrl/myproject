import os
import sqlite3

import streamlit as st

# ---------------------------------------------------------
# 0. 경로 설정 (★수정 포인트★)
# GitHub/Streamlit Cloud에서는 실행 위치가 로컬과 다를 수 있으므로,
# 항상 "이 파일이 있는 폴더"를 기준으로 절대경로를 만든다.
# ---------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "myproject.db")

# 1. 페이지 설정 (반드시 최상단)
st.set_page_config(layout="wide", page_title="국어과 AIDT")


st.markdown("""
<style>
    div[data-testid="stSidebarNav"] a[href*="토너먼트웹엡"] span {
        color: #0000FF !important;
        font-weight: 700 !important;
    }
</style>
""", unsafe_allow_html=True)

# 2. DB 초기화 함수 (myproject.db)
def init_db():
  conn = sqlite3.connect(DB_PATH)
  c = conn.cursor()

  # users 테이블 (회원 정보)
  c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            userid TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

  # learning_history 테이블 (형성평가 응시 기록)
  c.execute("""
        CREATE TABLE IF NOT EXISTS learning_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            userid TEXT NOT NULL,
            m1 TEXT, m2 TEXT, m3 TEXT, m4 TEXT, m5 TEXT,
            m6 TEXT, m7 TEXT, m8 TEXT, m9 TEXT, m10 TEXT,
            score INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
  conn.commit()
  conn.close()


init_db()

# 3. 세션 상태 초기화 (로그인 정보 유지)
if "logged_in" not in st.session_state:
  st.session_state.logged_in = False
if "userid" not in st.session_state:
  st.session_state.userid = ""

# ---------------------------------------------------------
# [사이드바] 로그인 & 회원가입 시스템
# ---------------------------------------------------------
st.sidebar.title("🔐 사용자 로그인")

if st.session_state.logged_in:
  st.sidebar.success(f"**{st.session_state.userid}**님 환영합니다! 🎉")
  st.sidebar.info("💡 서브 페이지(형성평가 등)를 이용하실 수 있습니다.")

  if st.sidebar.button("로그아웃"):
    st.session_state.logged_in = False
    st.session_state.userid = ""
    st.rerun()

else:
  st.sidebar.warning("로그인이 필요합니다.")
  auth_mode = st.sidebar.radio("메뉴 선택", ["로그인", "회원가입"])

  if auth_mode == "로그인":
    login_id = st.sidebar.text_input("아이디", key="sidebar_login_id")
    login_pw = st.sidebar.text_input(
        "비밀번호", type="password", key="sidebar_login_pw"
    )

    if st.sidebar.button("로그인"):
      conn = sqlite3.connect(DB_PATH)
      c = conn.cursor()
      c.execute(
          "SELECT * FROM users WHERE userid = ? AND password = ?",
          (login_id, login_pw),
      )
      user = c.fetchone()
      conn.close()

      if user:
        st.session_state.logged_in = True
        st.session_state.userid = login_id
        st.sidebar.success("로그인 성공!")
        st.rerun()
      else:
        st.sidebar.error("아이디 또는 비밀번호가 틀렸습니다.")

  elif auth_mode == "회원가입":
    new_id = st.sidebar.text_input("새 아이디", key="sidebar_new_id")
    new_pw = st.sidebar.text_input(
        "새 비밀번호", type="password", key="sidebar_new_pw"
    )

    if st.sidebar.button("가입하기"):
      if new_id and new_pw:
        try:
          conn = sqlite3.connect(DB_PATH)
          c = conn.cursor()
          c.execute(
              "INSERT INTO users (userid, password) VALUES (?, ?)",
              (new_id, new_pw),
          )
          conn.commit()
          conn.close()
          st.sidebar.success("가입 완료! 로그인해 주세요.")
        except sqlite3.IntegrityError:
          st.sidebar.error("이미 존재하는 아이디입니다.")
      else:
        st.sidebar.warning("아이디와 비밀번호를 입력하세요.")

st.sidebar.markdown("---")


# ---------------------------------------------------------
# [메인 화면] 기존 선생님 작성 내용 (1차시, 2차시, 3차시)
# ---------------------------------------------------------
st.title("This is my first webapp!!")
st.subheader("수학과 AIDT")

# [1차시]
col1, col2 = st.columns((4, 1))

with col1:
  with st.expander("1차시_동영상", expanded=True):
    st.title("동영상 시청......")
    youtube_url = "https://www.youtube.com/watch?v=U57LVkQVf4o"
    st.video(youtube_url)

with col2:
  with st.expander("Tips...", expanded=True):
    st.subheader("Tips...")
    tip_img = "https://i.ytimg.com/vi/MP8R6kBykzE/maxresdefault.jpg"
    st.image(tip_img)
    st.write("This is a term....")

# [2차시]
col1, col2 = st.columns((4, 1))

with col1:
  with st.expander("2차시_동영상"):
    st.title("동영상 시청......")
    # ★수정: 절대경로로 변경
    img_path = os.path.join(BASE_DIR, "img", "image.png")
    if os.path.exists(img_path):
      st.image(img_path)
    else:
      st.warning(
          f"⚠️ 이미지를 찾을 수 없습니다: img/image.png 가 저장소의 "
          "img 폴더에 있는지 확인해주세요."
      )

with col2:
  with st.expander("Tips..."):
    st.subheader("Tips...")
    tip_img = "https://i.ytimg.com/vi/MP8R6kBykzE/maxresdefault.jpg"
    st.image(tip_img)
    st.write("This is a term....")

# [3차시]
col1, col2 = st.columns((4, 1))

with col1:
  with st.expander("3차시_동영상"):
    st.title("머신러닝의 개념")

    # 머신러닝 개념 설명 (개조식 텍스트)
    st.markdown("""
        ### 🤖 머신러닝(Machine Learning)이란?
        * **정의**: 명시적으로 프로그램을 작성하지 않고, 데이터로부터 **패턴을 학습**하여 의사결정이나 예측을 수행하는 인공지능 기술
        * **전통적 프로그래밍과의 차이**:
          * *전통적 프로그래밍*: 데이터 + 규칙 ➔ **결과**
          * *머신러닝*: 데이터 + 결과 ➔ **규칙(모델)**
        * **핵심 요소**:
          1. **데이터(Data)**: 학습을 위한 품질 좋은 자료
          2. **특성(Feature)**: 예측에 영향을 주는 데이터의 주요 변수
          3. **모델(Model)**: 패턴을 학습하여 생성된 알고리즘 결과물
        """)

    # ★수정: 절대경로로 변경 (같은 이미지를 다시 사용)
    concept_img = os.path.join(BASE_DIR, "img", "image.png")
    if os.path.exists(concept_img):
      st.image(concept_img)
    else:
      st.warning(
          f"⚠️ 이미지를 찾을 수 없습니다: img/image.png 가 저장소의 "
          "img 폴더에 있는지 확인해주세요."
      )

with col2:
  with st.expander("Tips..."):
    st.subheader("Tips...")

    # 머신러닝 하위 개념 요약
    st.info("""
        💡 **머신러닝 3가지 유형**
        
        1. **지도학습 (Supervised)**
           * 정답(Label)이 있는 데이터 학습
           * *예: 분류(Classification), 회귀(Regression)*
        
        2. **비지도학습 (Unsupervised)**
           * 정답이 없는 데이터의 구조/패턴 발견
           * *예: 군집화(Clustering), 차원축소*
        
        3. **강화학습 (Reinforcement)**
           * 보상(Reward)을 통해 최적의 행동 방침 학습
           * *예: 게임 AI, 자율주행*
        """)
