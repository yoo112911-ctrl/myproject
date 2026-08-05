import os
import streamlit as st

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="토너먼트 최소 대결 수 계산 콘텐츠", page_icon="💡", layout="wide"
)

st.title("💡 토너먼트 최소 대결 수 계산 콘텐츠  (HTML 렌더링)")
st.write(
    "직접 개발하신 사례 콘텐츠(aaa.html)를 아래의 전용 뷰어 화면에서 직접"
    " 확인하실 수 있습니다."
)
st.markdown("---")

# 2. aaa.html 파일 경로 설정 및 렌더링
# aaa.html 파일이 프로젝트 루트 디렉터리에 있다고 가정합니다.
html_file_path = "aaa.html"

if os.path.exists(html_file_path):
  # 파일 읽기
  with open(html_file_path, "r", encoding="utf-8") as f:
    html_content = f.read()

  # 3. iframe 렌더링 (기본 1024x768, 상하/좌우 스크롤 가능 처리)
  # iframe 내부에 스타일(overflow: auto 등)을 주어 큰 콘텐츠 대응
  iframe_code = f"""
    <div style="width: 100%; display: flex; justify-content: center; background-color: #f9f9f9; padding: 10px; border-radius: 8px;">
        <iframe 
            srcdoc="{html_content.replace('"', '&quot;')}" 
            width="1024" 
            height="768" 
            style="border: 1px solid #ccc; border-radius: 4px; background-color: white; overflow: auto;"
            scrolling="yes">
        </iframe>
    </div>
    """

  # Streamlit components를 이용한 HTML 출력
  st.components.v1.html(iframe_code, height=800, scrolling=True)

else:
  # 파일이 없는 경우 예외 처리 및 가이드 안내
  st.error(
      f"⚠️ '{html_file_path}' 파일을 찾을 수 없습니다. 프로젝트 루트 폴더에"
      " 파일을 위치시켜 주세요."
  )

  st.info(
      "📁 **폴더 구조 확인 예시**\n"
      "- 📂 your_streamlit_project/\n"
      "  - 📄 app.py\n"
      "  - 📄 aaa.html  *(여기에 위치해야 합니다)*\n"
      "  - 📂 pages/\n"
      "    - 📄 02_머신러닝의사례.py"
  )