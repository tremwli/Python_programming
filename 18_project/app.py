import streamlit as st
from datetime import date
import pandas as pd
from song_api import get_song
import time 
import unicodedata

try:
    st.title("크롱틱")

    if "song" not in st.session_state:
            st.session_state.song = []

    if "practice_lines" not in st.session_state:    
        st.session_state.practice_lines = []
    if "typed_lines" not in st.session_state:
        st.session_state.typed_lines = []

    if "lines_speeds" not in st.session_state:
        st.session_state.lines_speeds = []

    if "start_time" not in st.session_state:
            st.session_state.start_time = 0

    if "typeq" not in st.session_state:
        st.session_state.typeq = ""

        
    col1, col2 = st.columns(2)

    with col1:
        title = st.text_input("노래 제목")

    with col2:
        artist = st.text_input("가수")

    if st.button("노래 검색하기"):

        if title and artist:
            st.session_state.song = get_song(title=title, artist=artist)
            
        elif artist == "" :
            st.info("가수를 입력해주세요.")

        elif title == "":
            st.info("노래 제목을 입력해주세요.")
        
        else:
            st.info("노래 제목과 가수를 입력해주세요.")

    st.divider()
            
    if st.session_state.song:
        option = []

        for song in st.session_state.song:
            option.append(song["제목"] + "-" + song["가수"])

        selected = st.radio("곡 선택", option)

        selected_index = option.index(selected)
        selected_song = st.session_state.song[selected_index]
     
    if st.button("가사 미리보기"):
        st.info(selected_song["가사"])
    
    if st.button("타자 시작하기"):
        st.session_state.practice_lines = selected_song["가사"].splitlines()
        st.session_state.index = 0
        st.session_state.start_time = time.perf_counter()
        st.session_state.typed_lines = []
        st.session_state.lines_speeds = []

    st.divider()

    if st.session_state.practice_lines:
        if st.session_state.index < len(st.session_state.practice_lines):
            
            with st.form("typing_form", clear_on_submit=True):
            
                    userWrite = st.text_input(st.session_state.practice_lines[st.session_state.index])
                    submitted = st.form_submit_button("^o^/")
            
                    if submitted:
                        st.session_state.typed_lines.append(userWrite)
                        
                        st.session_state.index += 1
                        
                        end_time = time.perf_counter()
                        interval = end_time - st.session_state.start_time
                    
                        st.session_state.typeq = unicodedata.normalize("NFD", userWrite)

                        st.session_state.lines_speeds.append(len(st.session_state.typeq) / interval * 60)
                        
                        st.session_state.start_time = end_time
                        st.rerun()
                
                    if st.session_state.lines_speeds:
                        st.info(f"현재 타수 : {st.session_state.lines_speeds[-1]:.1f}타/분")
            
        else:
            mean = sum(st.session_state.lines_speeds) / len(st.session_state.lines_speeds)
            st.title("결과")
            st.info(f"빠르기 : {mean:.1f}타/분")
            st.info(f"최대 빠르기 : {max(st.session_state.lines_speeds):.1f}타/분")
            

except Exception as e:
    st.error(e)         