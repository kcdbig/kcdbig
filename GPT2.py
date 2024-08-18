

import requests
import streamlit as st
from streamlit_chat import message
import openai
import os

# OpenAI API 키 설정
openai.api_key = os.environ.get('OPENAI_API_KEY')  # 환경 변수에서 API 키 가져오기

# 시스템 지침 정의
system_instruction1 = '''너는 중학교 1학년 과학교사야, 상냥하고 친절해.'''

# 세션 스테이트 초기화
if 'messages' not in st.session_state:
    st.session_state['messages'] = [{
        "role": "assistant",
        "content": '나는 중학교 1학년 과학교사 챗봇이야. 이름이 뭐니?'
    }]

if 'stop' not in st.session_state:
    st.session_state['stop'] = False

def chat(text):
    messages = [{"role": "system", "content": system_instruction1}]
    messages.extend(st.session_state['messages'])
    user_turn = {"role": "user", "content": text}
    messages.append(user_turn)
    st.session_state['messages'].append(user_turn)

    # OpenAI API 호출
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=messages
    )

    assistant_messages = response['choices'][0]['message']['content']
    assistant_turn = {"role": "assistant", "content": assistant_messages}
    st.session_state['messages'].append(assistant_turn)

    return assistant_messages

# Streamlit 앱 타이틀
st.title('중학교 1학년 과학교사 챗봇')

if not st.session_state['stop']:
    row1 = st.container()
    row2 = st.container()
    row3 = st.container()

    with row2:
        with st.form('form', clear_on_submit=True):
            input_text = st.text_input('You')
            submitted = st.form_submit_button('Send')
            if submitted and input_text:
                chat(input_text)

    with row1:
        for i, msg_obj in enumerate(st.session_state['messages']):
            msg = msg_obj['content']
            is_user = (i % 2 == 1)  # 질문/응답 구분
            message(msg, is_user=is_user, key=i)

    with row3:
        if st.button('과학 질문하기'):
            recommendation = chat("위의 대화를 기반으로 과학과 관련된 질문이나 설명을 해줘.")
            st.success(recommendation)
            del st.session_state['messages']  # 메시지 초기화

