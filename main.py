import streamlit as st
import requests
import json

from dotenv import load_dotenv
import os

# load .env
load_dotenv()

API_KEY = os.environ.get('apiKey')
HASH = os.environ.get('hash')

st.header('육아 정책 알림 문자 전송봇')
st.markdown('대상에 맞는 육아 정책을 골라 적절한 인삿말과 함께 문자를 작성해드립니다.')

if 'stage' not in st.session_state:
    st.session_state.stage = 0

def set_state(i):
    st.session_state.stage = i

if st.session_state.stage == 0:
    st.button('문자 작성 시작하기', on_click=set_state, args=[1])

if st.session_state.stage >= 1:
    center = st.text_input('기관명', on_change=set_state, args=[2])

if st.session_state.stage >= 2:
    target = st.selectbox(
        '문자 수신 대상',
        ['다자녀', '난임 부부', '차상위계층', '임산부', '워킹부부', '직접 입력'], 
        on_change=set_state, args=[3]
      )
    if target == '직접 입력':
        target = st.text_input('구체적으로 알려주셔도 좋아요!', on_change=set_state, args=[3])

if st.session_state.stage >= 3:
    weather = st.selectbox(
        '오늘의 날씨',
        ['봄', '여름', '가을', '겨울', '화창', '추움', '장마', '눈', '직접 입력'], 
        on_change=set_state, args=[4]
      )
    if weather == '직접 입력':
        weather = st.text_input('구체적인 날씨도 좋아요!', on_change=set_state, args=[4])

if st.session_state.stage >= 4:
    tell = st.text_input('수신자 문의처', on_change=set_state, args=[5])

if st.session_state.stage >= 5:
    with st.spinner('문자를 작성하고 있어요!'):
        response = requests.post( 
            url="https://api-laas.wanted.co.kr/api/preset/chat/completions", 
            headers={
                "project": "PROMPTHON_PRJ_428",
                "apiKey": API_KEY, 
                "Content-Type": "application/json; charset=utf-8",
            },
            data=json.dumps({
            "hash": HASH, 
            "params": {
                "기관": center,
                "target":target,
                "weather":weather,
                "문의처":tell
            } 
            }))

            # 'content' 값 추출
        content = response.json()['choices'][0]['message']['content']
        print(content)

            # 결과 출력
        container = st.container(border=True)    
        container.write(content)




