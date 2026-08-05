import sqlite3
import pandas as pd
import streamlit as st

st.set_page_config(page_title="머신러닝 형성평가", page_icon="📝", layout="wide")

# 로그인 여부 확인
if "logged_in" not in st.session_state or not st.session_state.logged_in:
  st.warning("⚠️ 형성평가에 응시하려면 먼저 메인 페이지에서 로그인해 주세요.")
  st.stop()

st.title("📝 머신러닝 개념 형성평가")
st.write(
    f"사용자 **[{st.session_state.userid}]**님 환영합니다! 형성평가는 수시로"
    " 응시 가능하며, 결과는 DB에 자동 저장됩니다."
)
st.markdown("---")

# 10개 문제 데이터 정의
quiz_data = [
    {
        "num": 1,
        "question": "1. 머신러닝(Machine Learning)의 정의로 가장 적절한 것은?",
        "options": [
            "1) 사람이 모든 규칙을 직접 코드로 작성하는 기술",
            "2) 데이터로부터 컴퓨터가 스스로 학습하여 패턴을 찾아내는 기술",
            "3) 하드웨어를 물리적으로 조립하여 가동하는 기술",
            "4) 인터넷 연결 없이 수동으로만 작동하는 프로그램",
            "5) 정해진 그래픽만 자동으로 출력하는 시스템",
        ],
        "hint": "전통적 프로그래밍과 달리 '스스로 규칙을 찾는다'는 점에 주목하세요.",
        "answer": "2)",
    },
    {
        "num": 2,
        "question": (
            "2. 다음 중 '정답(Label)'이 포함된 데이터를 학습하여 예측하는"
            " 유형은?"
        ),
        "options": [
            "1) 비지도학습",
            "2) 강화학습",
            "3) 지도학습",
            "4) 전이학습",
            "5) 자가학습",
        ],
        "hint": "선생님이 정답지를 주고 가르치는 모습을 생각해보세요.",
        "answer": "3)",
    },
    {
        "num": 3,
        "question": (
            "3. 스팸 메일 차단과 같이 데이터를 정해진 카테고리로 나누는"
            " 지도학습 방식은?"
        ),
        "options": [
            "1) 회귀(Regression)",
            "2) 분류(Classification)",
            "3) 군집화(Clustering)",
            "4) 차원 축소",
            "5) 강화학습",
        ],
        "hint": "연속적인 수치가 아니라 '범주(Class)'를 맞히는 문제입니다.",
        "answer": "2)",
    },
    {
        "num": 4,
        "question": "4. 다음 중 지도학습의 '회귀(Regression)' 예시로 적절한 것은?",
        "options": [
            "1) 내일의 미세먼지 농도 수치 예측",
            "2) 고양이와 강아지 사진 구분",
            "3) 유사한 구매 성향의 고객 그룹화",
            "4) 게임 AI의 최적 이동 경로 탐색",
            "5) 스팸 메일 유무 판별",
        ],
        "hint": "예측 결과가 '연속된 숫자'인 것을 찾아보세요.",
        "answer": "1)",
    },
    {
        "num": 5,
        "question": (
            "5. 정답(Label)이 없는 데이터에서 스스로 구조나 패턴을 찾아내는"
            " 학습 유형은?"
        ),
        "options": [
            "1) 지도학습",
            "2) 비지도학습",
            "3) 강화학습",
            "4) 심화학습",
            "5) 규칙 기반 학습",
        ],
        "hint": "가르쳐주는 정답지(Label)가 없는 학습입니다.",
        "answer": "2)",
    },
    {
        "num": 6,
        "question": "6. 다음 중 비지도학습의 대표적인 기술에 해당하는 것은?",
        "options": [
            "1) 분류(Classification)",
            "2) 회귀(Regression)",
            "3) 군집화(Clustering)",
            "4) Q-Learning",
            "5) 텍스트 분류",
        ],
        "hint": "비슷한 데이터를 '끼리끼리' 묶어주는 기술입니다.",
        "answer": "3)",
    },
    {
        "num": 7,
        "question": (
            "7. 행동에 따른 '보상(Reward)'을 최대화하도록 학습하는 인공지능"
            " 방식은?"
        ),
        "options": [
            "1) 지도학습",
            "2) 비지도학습",
            "3) 강화학습",
            "4) 의사결정나무",
            "5) 로지스틱 회귀",
        ],
        "hint": "알파고(AlphaGo)나 로봇 제어 등에 주로 활용됩니다.",
        "answer": "3)",
    },
    {
        "num": 8,
        "question": (
            "8. 모델이 학습 데이터에는 지나치게 잘 맞지만, 새로운 데이터에서는"
            " 성능이 떨어지는 현상은?"
        ),
        "options": [
            "1) 과소적합(Underfitting)",
            "2) 과적합(Overfitting)",
            "3) 정규화(Normalization)",
            "4) 샘플링",
            "5) 최적화",
        ],
        "hint": "학습 데이터에만 '과하게' 적합된 상태입니다.",
        "answer": "2)",
    },
    {
        "num": 9,
        "question": (
            "9. 일반적으로 모델 검증을 위해 전체 데이터를 나누는 흔한"
            " 비율(Train : Test)은?"
        ),
        "options": [
            "1) 10% : 90%",
            "2) 50% : 50%",
            "3) 80% : 20%",
            "4) 0% : 100%",
            "5) 데이터를 나누지 않는다",
        ],
        "hint": "충분히 학습시키고 남은 일부로 시험을 봅니다.",
        "answer": "3)",
    },
    {
        "num": 10,
        "question": (
            "10. K-최근접 이웃(KNN) 알고리즘이 새로운 데이터를 분류하는 기준은?"
        ),
        "options": [
            "1) 데이터 간의 거리(유사도)",
            "2) 보상 점수의 크기",
            "3) 트리의 깊이",
            "4) 전체 데이터의 평균값",
            "5) 무작위 추출",
        ],
        "hint": "가장 가까이 위치한 '이웃' 점들과의 거리를 확인합니다.",
        "answer": "1)",
    },
]

tab_eval, tab_history = st.tabs(["✍️ 형성평가 응시", "📊 나의 응시 이력"])

# ==========================================
# 탭 1: 형성평가 응시
# ==========================================
with tab_eval:
  with st.form("quiz_form"):
    user_answers = []

    for item in quiz_data:
      st.markdown(f"#### {item['question']}")

      # 5지 선다 라디오 버튼
      selected = st.radio(
          f"문항 {item['num']} 답안 선택:",
          item["options"],
          key=f"q_{item['num']}",
          index=None,
      )
      user_answers.append(selected)

      # 힌트 제공 (Expander)
      with st.expander("💡 힌트 보기"):
        st.info(item["hint"])

      # 정답 감추기 (Expander)
      with st.expander("👁️ 정답 확인하기 (미리보기)"):
        st.write(f"**정답:** {item['answer']}")

      st.markdown("---")

    submit_button = st.form_submit_button("🏁 형성평가 제출하기")

  if submit_button:
    # 모든 문항 입력 여부 검증
    if None in user_answers:
      st.error("⚠️ 아직 풀지 않은 문항이 있습니다. 모든 문항에 답해 주세요!")
    else:
      score = 0
      ans_selected_numbers = []  # m1~m10에 저장할 선택한 번호 문자열

      for idx, item in enumerate(quiz_data):
        user_ans = user_answers[idx]
        # 선택한 답의 번호만 추출 (예: "2) ..." -> "2")
        ans_num = user_ans.split(")")[0] + ")"
        ans_selected_numbers.append(ans_num)

        # 정답 채점 (문항당 10점)
        if user_ans.startswith(item["answer"]):
          score += 10

      # DB(myproject.db -> learning_history)에 저장
      conn = sqlite3.connect("myproject.db")
      c = conn.cursor()
      c.execute(
          """
            INSERT INTO learning_history (
                userid, m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, score
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
          (st.session_state.userid, *ans_selected_numbers, score),
      )
      conn.commit()
      conn.close()

      st.balloons()
      st.success(
          f"🎉 평가가 제출되었습니다! 최종 점수: **{score}점 / 100점**"
      )
      st.info(
          "상단의 **'📊 나의 응시 이력'** 탭에서 제출된 결과를 확인하실 수"
          " 있습니다."
      )

# ==========================================
# 탭 2: 나의 응시 이력 (DB 데이터 조회)
# ==========================================
with tab_history:
  st.subheader(f"📜 [{st.session_state.userid}] 님의 응시 이력 목록")

  conn = sqlite3.connect("myproject.db")
  query = """
        SELECT created_at AS '응시 일시', score AS '점수',
               m1, m2, m3, m4, m5, m6, m7, m8, m9, m10
        FROM learning_history
        WHERE userid = ?
        ORDER BY created_at DESC
    """
  df = pd.read_sql_query(query, conn, params=(st.session_state.userid,))
  conn.close()

  if not df.empty:
    st.dataframe(df, use_container_width=True)

    # 평균 점수 시각화
    avg_score = df["점수"].mean()
    st.metric(label="총 응시 횟수", value=f"{len(df)}회")
    st.metric(label="평균 점수", value=f"{avg_score:.1f}점")
  else:
    st.info("아직 응시한 기록이 없습니다. 평가를 진행해 주세요!")