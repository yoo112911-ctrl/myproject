# streamlit webapp의 pages 경로 밑에 서브 페이지로 다음을 생성해주세요.
# 머신러닝의 개념에 대해 학습할 콘텐츠 생성
# 간단하게 머신러닝의 개념을 실습할 수 있는 시뮬레이터 포함(mock data를 생성해서(분류 데이터) 직접 실습하도록 함) 


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from sklearn.datasets import make_blobs
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="머신러닝의 개념 & 실습 시뮬레이터",
    page_icon="🤖",
    layout="wide",
)

# 메인 타이틀
st.title("🤖 머신러닝의 개념 및 실습 시뮬레이터")
st.markdown("---")

# 탭 구성: 개념 학습 / 실습 시뮬레이터
tab1, tab2 = st.tabs(["📚 1. 머신러닝의 개념", "🎮 2. 머신러닝 분류 시뮬레이터"])

# ==========================================
# TAB 1: 머신러닝의 개념
# ==========================================
with tab1:
  st.header("💡 머신러닝(Machine Learning)이란?")
  st.write("""
    **머신러닝**은 사람이 일일이 규칙(Rule)을 명시적으로 프로그래밍하지 않아도, 
    컴퓨터가 **데이터를 기반으로 스스로 학습하여 패턴을 찾고 예측/결정을 내리게 하는 인공지능(AI)의 한 분야**입니다.
    """)

  st.markdown("### 🔄 전통적 프로그래밍 vs 머신러닝")
  col1, col2 = st.columns(2)
  with col1:
    st.info("""
        **💻 전통적 프로그래밍**
        - **입력:** 데이터 + 명시적 규칙(Rule)
        - **출력:** 결과(Answer)
        - *예: "특정 조건(규칙)을 만족하면 A그룹으로 분류하라"*
        """)
  with col2:
    st.success("""
        **🤖 머신러닝**
        - **입력:** 데이터 + 결과(Answer / Label)
        - **출력:** 규칙(Model / Pattern)
        - *예: 수많은 데이터와 정답을 준 뒤, 컴퓨터가 스스로 분류 기준 규칙을 찾아냄*
        """)

  st.markdown("---")
  st.markdown("### 🎯 머신러닝의 3가지 주요 학습 유형")

  m_col1, m_col2, m_col3 = st.columns(3)
  with m_col1:
    st.subheader("1. 지도학습 (Supervised Learning)")
    st.write("""
        - **정답(Label)이 있는 데이터**를 학습합니다.
        - **분류(Classification):** 범주형 정답 예측 (예: 스팸 메일 여부, 암 양성/음성)
        - **회귀(Regression):** 연속형 숫자 예측 (예: 집값 예측, 주가 예측)
        """)
  with m_col2:
    st.subheader("2. 비지도학습 (Unsupervised Learning)")
    st.write("""
        - **정답(Label)이 없는 데이터**에서 구조나 패턴을 찾아냅니다.
        - **군집화(Clustering):** 비슷한 데이터끼리 그룹화 (예: 고객 세분화)
        - **차원 축소(Dimensionality Reduction):** 데이터 핵심 특성 추출
        """)
  with m_col3:
    st.subheader("3. 강화학습 (Reinforcement Learning)")
    st.write("""
        - 에이전트가 환경과 상호작용하며 **보상(Reward)을 최대화**하도록 학습합니다.
        - 예: 알파고, 자율주행, 로봇 제어, 게임 AI
        """)

# ==========================================
# TAB 2: 머신러닝 분류 시뮬레이터
# ==========================================
with tab2:
  st.header("🎮 분류(Classification) 시뮬레이터")
  st.write(
      "가상의 데이터(Mock Data)를 생성하고, 다양한 머신러닝 모델을 직접 작동시켜"
      " 보세요!"
  )

  # 사이드바 설정 영역
  st.sidebar.header("⚙️ 시뮬레이터 설정")

  st.sidebar.subheader("1. Mock Data 생성 설정")
  n_samples = st.sidebar.slider(
      "샘플 개수 (Data Size)",
      min_value=100,
      max_value=1000,
      value=300,
      step=50,
  )
  cluster_std = st.sidebar.slider(
      "데이터 노이즈/분산 정도",
      min_value=0.5,
      max_value=3.0,
      value=1.2,
      step=0.1,
  )
  random_state = st.sidebar.number_input(
      "랜덤 시드 (Random State)", value=42, step=1
  )

  st.sidebar.subheader("2. 머신러닝 알고리즘 선택")
  model_name = st.sidebar.selectbox(
      "알고리즘 선택",
      [
          "K-최근접 이웃 (KNN)",
          "결정 트리 (Decision Tree)",
          "로지스틱 회귀 (Logistic Regression)",
      ],
  )

  # 알고리즘별 하이퍼파라미터 설정
  if model_name == "K-최근접 이웃 (KNN)":
    n_neighbors = st.sidebar.slider(
        "이웃 수 (K)", min_value=1, max_value=15, value=5
    )
    model = KNeighborsClassifier(n_neighbors=n_neighbors)
  elif model_name == "결정 트리 (Decision Tree)":
    max_depth = st.sidebar.slider(
        "최대 깊이 (Max Depth)", min_value=1, max_value=10, value=3
    )
    model = DecisionTreeClassifier(max_depth=max_depth, random_state=42)
  else:
    C_val = st.sidebar.slider(
        "규제 매개변수 (C)", min_value=0.01, max_value=10.0, value=1.0
    )
    model = LogisticRegression(C=C_val)

  # 1. Mock Data 생성 (2차원 특성을 갖는 2개 클래스 분류 데이터)
  X, y = make_blobs(
      n_samples=n_samples,
      centers=2,
      cluster_std=cluster_std,
      random_state=random_state,
  )

  # Train / Test 분리
  X_train, X_test, y_train, y_test = train_test_split(
      X, y, test_size=0.2, random_state=random_state
  )

  # 2. 모델 학습 및 예측
  model.fit(X_train, y_train)
  y_pred = model.predict(X_test)
  acc = accuracy_score(y_test, y_pred)

  # 3. 화면 레이아웃 (시각화 & 평가)
  col_left, col_right = st.columns([1.2, 1])

  with col_left:
    st.subheader("📌 결정 경계 (Decision Boundary) 시각화")

    fig, ax = plt.subplots(figsize=(7, 5))

    # 격자를 통한 결정 경계(Decision Boundary) 계산
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(
        np.arange(x_min, x_max, 0.02), np.arange(y_min, y_max, 0.02)
    )

    Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    # 경계면 바탕색 지정
    ax.contourf(xx, yy, Z, alpha=0.3, cmap=plt.cm.coolwarm)

    # 학습 데이터 점 표기 (원 형태)
    ax.scatter(
        X_train[:, 0],
        X_train[:, 1],
        c=y_train,
        cmap=plt.cm.coolwarm,
        edgecolors="k",
        alpha=0.7,
        label="Train Data",
    )
    # 테스트 데이터 점 표기 (X 형태)
    ax.scatter(
        X_test[:, 0],
        X_test[:, 1],
        c=y_test,
        cmap=plt.cm.coolwarm,
        marker="x",
        s=60,
        linewidths=1.5,
        label="Test Data",
    )

    ax.set_title(f"{model_name} Decision Boundary")
    ax.set_xlabel("Feature 1")
    ax.set_ylabel("Feature 2")
    ax.legend()
    st.pyplot(fig)

  with col_right:
    st.subheader("📊 모델 성능 평가")
    st.metric(label="정확도 (Accuracy)", value=f"{acc * 100:.2f}%")

    st.markdown("#### 혼동 행렬 (Confusion Matrix)")
    cm = confusion_matrix(y_test, y_pred)
    cm_df = pd.DataFrame(
        cm,
        columns=["예측: 클래스 0", "예측: 클래스 1"],
        index=["실제: 클래스 0", "실제: 클래스 1"],
    )
    st.dataframe(cm_df)

    st.markdown("#### 💡 관찰 팁")
    st.info("""
        - **노이즈/분산**을 키울수록 두 클래스 데이터가 섞여 정확도가 저하됩니다.
        - **KNN**에서 K를 극단적으로 작게 고르면 과적합(Overfitting), 크게 고르면 단순화(Underfitting) 경향을 보입니다.
        - **결정 트리**의 깊이(Max Depth)를 깊게 설정할수록 결정 경계가 복잡해집니다.
        """)