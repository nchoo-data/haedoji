import streamlit as st
import pandas as pd
import random
from collections import defaultdict
    
# -------------------------------------------------
# 기본 설정
# -------------------------------------------------
st.set_page_config(page_title="추구미 테스트", layout="centered")

st.markdown(
    """
    <style>
    .question-title {
        text-align: center;
        font-size: 26px;
        font-weight: 700;
        margin: 32px 0 40px 0;
        color: var(--text-color);
    }

    .option-btn {
        width: 100%;
        max-width: 720px;
        margin: 0 auto 28px auto;
        padding: 22px 20px;
        text-align: center;

        white-space: nowrap;
        font-size: clamp(13px, 3.5vw, 17px);
    
        border-radius: 999px;
        border: 3px solid #AEB7E6;
        background-color: #FFFFFF;
        color: #111111;
        font-size: 17px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s ease;
    }

    .option-btn:hover {
        background-color: #EEF1FF;
    }

    .option-selected {
        background-color: #EEF1FF;
        border-color: #6C63FF;
        font-weight: 700;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------
# 전역 CSS (모든 요소 가운데 정렬)
# -------------------------------------------------
st.markdown(
    """
    <style>
        .center-container {
            max-width: 720px;
            margin: 0 auto;
            text-align: center;
        }
        div.stButton > button {
            width: 300px;
            height: 58px;
            font-size: 17px;
            font-weight: 600;
            border-radius: 14px;
            margin: 0 auto;
            display: block;
        }
        input {
            text-align: center;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------
# 엑셀 파일 변수 설정 
# -------------------------------------------------

FILE_PATH = "추구미 26문항.xlsx"

# -------------------------------------------------
# 엑셀 로드
# -------------------------------------------------

def load_data():
    current_df = pd.read_excel(FILE_PATH, sheet_name="현재 내 모습 진단")
    ideal_df   = pd.read_excel(FILE_PATH, sheet_name="추구미 진단")
    improve_df = pd.read_excel(FILE_PATH, sheet_name="보완 포인트")
    return current_df, ideal_df, improve_df

current_df, ideal_df, improve_df = load_data()

# -------------------------------------------------
# 질문 데이터 생성
# -------------------------------------------------
def build_questions(df):
    questions = []
    for _, row in df.iterrows():
        options = [
            {"text": row["option_A"], "type": row["type_A"]},
            {"text": row["option_B"], "type": row["type_B"]},
            {"text": row["option_C"], "type": row["type_C"]},
            {"text": row["option_D"], "type": row["type_D"]},
            {"text": row["option_E"], "type": row["type_E"]},
        ]
        questions.append({
            "question": row["question"],
            "options": options
        })
    return questions

CURRENT_QUESTIONS = build_questions(current_df)
IDEAL_QUESTIONS   = build_questions(ideal_df)

TOTAL_CURRENT = len(CURRENT_QUESTIONS)
TOTAL_IDEAL   = len(IDEAL_QUESTIONS)
TYPE_PAGE   = TOTAL_CURRENT + TOTAL_IDEAL + 2   # 유형페이지
FIX_PAGE    = TOTAL_CURRENT + TOTAL_IDEAL + 3   # 보완점페이지


# -------------------------------------------------
# 세션 상태
# -------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = 0
    st.session_state.name = ""
    st.session_state.current_scores = defaultdict(int)
    st.session_state.ideal_scores = defaultdict(int)
    st.session_state.scroll_top = False

# -------------------------------------------------
# Intro Page
# -------------------------------------------------
if st.session_state.page == 0:
    st.markdown(
        """
        <div class="center-container">
            <h1><b>💨나의 추구미와 가까워지기🏃‍♂</b></h1>
            <p>나는 내 추구미와 얼마나 가까울까❓ 추구미에 따른 보완점 제안 서비스❕</p>
            <br>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 대표 이미지
    st.image("assets/추구미image_최종.png", use_container_width=True)


    # 소개 문구
    st.markdown(
        """
    <div align="center">

    ### 🤔 **추구미**에 대해 알고 계신가요? 

    ☑️ **추구미란?** <br>
    '추구하다'와 '美(아름다울 미)'의 합성어로,  
    Z세대가 자신의 이상적인 이미지를 추구하는 과정을 나타내는 신조어입니다.

 
    📋 **테스트 소개** <br>
    이 테스트는 현재의 내 모습과 나의 추구미를 진단하고,  
    추구미에 도달하기 위해 보완할 점을 제시해줍니다.

    </div>
    """,
        unsafe_allow_html=True
    )

    st.divider()

    # 이름 입력
    st.markdown("<div class='center-container'><b>이름을 입력하세요.</b></div>", unsafe_allow_html=True)
    name = st.text_input("", placeholder="이름 입력")
  

    # 시작 버튼
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("테스트를 시작하시겠습니까?", use_container_width=True):
            if not name.strip():
                st.warning("이름을 입력해주세요.")
            else:
                st.session_state.name = name.strip()
                st.session_state.page = 1
                st.rerun()

# -------------------------------------------------
# Step 1: 현재 상태
# -------------------------------------------------
elif 1 <= st.session_state.page <= TOTAL_CURRENT:
    idx = st.session_state.page - 1
    q = CURRENT_QUESTIONS[idx]

    st.markdown(
        "<div class='center-container'><h3>Step 1. 현재상태 진단</h3></div>",
        unsafe_allow_html=True
    )
    st.divider()
    options = q["options"].copy()

    # 질문 출력
    st.markdown(
        f"<div class='question-title'>{q['question']}</div>",
        unsafe_allow_html=True
    )

    # 선택 상태 키
    select_key = f"selected_cur_{idx}"
    if select_key not in st.session_state:
        st.session_state[select_key] = None

    # 선택지 버튼 (선택 즉시 다음 질문으로 이동)
    for i, opt in enumerate(q["options"]):
        if st.button(
            opt["text"],
            key=f"cur_{st.session_state.page}_{i}",
            use_container_width=True
        ):
            st.session_state.current_scores[opt["type"]] += 1
            st.session_state.page += 1
            st.rerun()


# -------------------------------------------------
# 쉬어가는 페이지
# -------------------------------------------------
elif st.session_state.page == TOTAL_CURRENT + 1:
    st.markdown(
        "<h3 style='text-align:center;'>다음 스텝을 진행합니다.</h3>",
        unsafe_allow_html=True,
    )
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("계속하기"):
            st.session_state.page += 1
            st.rerun()

# -------------------------------------------------
# Step 2: 추구미
# -------------------------------------------------
elif TOTAL_CURRENT + 2 <= st.session_state.page <= TOTAL_CURRENT + TOTAL_IDEAL + 1:
    idx = st.session_state.page - (TOTAL_CURRENT + 2)
    q = IDEAL_QUESTIONS[idx]

    st.markdown(
        "<div class='center-container'><h3>Step 2. 추구미 진단</h3></div>",
        unsafe_allow_html=True
    )
    st.divider()
    
    options = q["options"]

    # 질문 출력
    st.markdown(
        f"<div class='question-title'>{q['question']}</div>",
        unsafe_allow_html=True
    )

    # 선택 상태 키
    select_key = f"selected_ideal_{idx}"
    if select_key not in st.session_state:
        st.session_state[select_key] = None

    # 선택지 버튼 (선택 즉시 다음 질문으로 이동)
    for i, opt in enumerate(q["options"]):
        if st.button(
            opt["text"],
            key=f"ideal_{st.session_state.page}_{i}",
            use_container_width=True
        ):
            st.session_state.ideal_scores[opt["type"]] += 1
            st.session_state.page += 1 
            st.rerun()


# -------------------------------------------------
# 유형 페이지
# -------------------------------------------------
elif st.session_state.page == TYPE_PAGE:
    name = st.session_state.name

    current_code = max(st.session_state.current_scores, key=st.session_state.current_scores.get)
    ideal_code   = max(st.session_state.ideal_scores, key=st.session_state.ideal_scores.get)

    current_type = current_code
    ideal_type   = ideal_code
    improve_row = improve_df[improve_df["type_name"] == ideal_type].iloc[0]
    core_kw = improve_row["core_kw"]

    st.markdown(
        f"<div class='center-container'><h2>{name}님의 추구미는'{ideal_type}' 입니다🤩<br></h2> <p><b>키워드: {core_kw}</b></p></div>",
        unsafe_allow_html=True,
    )

    st.divider()

    # 🔽 하단 이미지 추가
    st.image("assets/자연형이미지.jpg", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("보완점 확인하기", use_container_width=True):
            st.session_state.page = FIX_PAGE
            st.rerun()


# -------------------------------------------------
# 보완점 페이지
# -------------------------------------------------
elif st.session_state.page == FIX_PAGE:
    name = st.session_state.name

    current_code = max(st.session_state.current_scores, key=st.session_state.current_scores.get)
    ideal_code   = max(st.session_state.ideal_scores, key=st.session_state.ideal_scores.get)

    current_type = current_code
    ideal_type   = ideal_code
    improve_row = improve_df[improve_df["type_name"] == ideal_type].iloc[0]

    core_msg = improve_row["core_msg"]
    direction_msg = improve_row["direction_msg"]
    actions = [
        improve_row["action_1"],
        improve_row["action_2"],
        improve_row["action_3"],
    ]
    st.markdown(
        "<div class='center-container'><h3>🤍추구미에 도달하기 위한 [보완점]을 제시해드릴게요😉</h3></div>",
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.image("assets/자연형보완점이미지.jpg", width=500)

    st.markdown(
        """
        <style>
        .fix-box {
            border: 1px solid #ddd;
            border-radius: 12px;
            padding: 20px;
            margin-top: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="fix-box">
            <h3>핵심 메시지</h3>
            <p>{core_msg}</p>
            <h3>보완 방향</h3>
            <p>{direction_msg}</p>
            <h3>일상 속 실천</h3>
            <ul>
                <li>{actions[0]}</li>
                <li>{actions[1]}</li>
                <li>{actions[2]}</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )



    st.markdown("</div>", unsafe_allow_html=True)


    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("처음으로 돌아가기"):
            st.session_state.page = 0
            st.session_state.current_scores.clear()
            st.session_state.ideal_scores.clear()
            st.session_state.name = ""
            st.rerun()
