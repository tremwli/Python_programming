import streamlit as st
from song_api import get_song
from song_db import init_db, load_songs, save_songs, add_song, get_songs
from song_ai import search
import streamlit.components.v1 as components
import time 
import unicodedata
import pandas as pd


try:
    init_db()
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
        if title.strip() == "":
            st.info("노래 제목을 입력해주세요.")
        elif artist.strip() == "":
            st.info("가수를 입력해주세요.")
        else:
            search_title = title.strip()
            search_artist = artist.strip()

            saved_songs = load_songs(search_title, search_artist)

            if saved_songs:
                st.session_state.song = saved_songs
                print("DB에 저장된 거 가져옴")
            else:
                api_songs = get_song( title=search_title, artist=search_artist)

                st.session_state.song = api_songs or []

                if api_songs:
                    save_songs(search_title, search_artist, api_songs)
                else:
                    st.info("검색 결과 없음. 띄어쓰기를 확인하거나 아래 곡 추가하기를 할 것")


    ai_query = st.text_input("AI 검색 : 첫 실행 시 시간이 오래 걸립니다.", placeholder="예) 일어나서 춤추고 싶어지는 신나는 노래 ")

    if st.button("AI로 검색하기"):
        if ai_query.strip() == "":
            st.info("검색어를 입력해주세요.")
        else:
            all_songs = get_songs()

            if not all_songs:
                st.info("DB에 저장된 곡이 없습니다.")
            else:
                with st.spinner("DB에서 찾는 중..."):
                    st.session_state.song = search(ai_query.strip(), all_songs)
                for i in st.session_state.song:
                    st.write(i["제목"], i["점수"])
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

        countdown = st.empty()

        for number in range(3, 0, -1):
            countdown.title(number)
            time.sleep(1)

        countdown.empty()

        

        lyrics = selected_song["가사"].lstrip("\ufeff")
        st.session_state.practice_lines = []

        for line in lyrics.splitlines():
            if line.strip() != "":
                st.session_state.practice_lines.append(line)


        
        st.session_state.index = 0
        st.session_state.start_time = time.perf_counter()
        st.session_state.typed_lines = []
        st.session_state.lines_speeds = []

    st.divider()

   

    if st.session_state.practice_lines:
        if st.session_state.index < len(st.session_state.practice_lines):
            
           
            
            with st.form("typing_form", clear_on_submit=True):
            
                    userWrite = st.text_input(f"{st.session_state.practice_lines[st.session_state.index]} ",  key="typing_input",)
                    submitted = st.form_submit_button(f"진행도 : {st.session_state.index + 1}  / {len(st.session_state.practice_lines)}")
            
                    if submitted:
                    

                        typed = unicodedata.normalize("NFC", userWrite).strip()
                        target = unicodedata.normalize("NFC", st.session_state.practice_lines[st.session_state.index]).strip()
                       

                        if typed == target:
                            st.session_state.typed_lines.append(userWrite)
                            
                            st.session_state.index += 1
                            
                            end_time = time.perf_counter()
                            interval = end_time - st.session_state.start_time
                        
                            st.session_state.typeq = unicodedata.normalize("NFD", userWrite)

                            st.session_state.lines_speeds.append(len(st.session_state.typeq) / interval * 60)
                            
                            st.session_state.start_time = end_time
                            
                            st.rerun()
                    
                           
                        else: 
                            st.error("오타! 다시 쓰세요.")
                            
                            

                    if st.session_state.lines_speeds:
                        st.info(f"현재 타수 : {st.session_state.lines_speeds[-1]:.1f}타/분")

                        
            
        else:
            mean = sum(st.session_state.lines_speeds) / len(st.session_state.lines_speeds)
            st.title("결과")
            st.info(f"빠르기 : {mean:.1f}타/분")
            st.info(f"최대 빠르기 : {max(st.session_state.lines_speeds):.1f}타/분")

        
    with st.expander("곡 직접 추가"):
        add_title = st.text_input("추가할 곡 제목", key="add_title")
        add_artist = st.text_input("추가할 가수", key="add_artist")
        add_lyrics = st.text_area("가사 입력", key="add_lyrics")

        if st.button("곡 저장하기"):
            if add_title.strip() and add_artist.strip() and add_lyrics.strip():
                add_song(
                    add_title.strip(),
                    add_artist.strip(),
                    add_lyrics.strip()
                )
                st.success("DB 저장 완료")
            else:
                st.info("제목, 가수, 가사를 모두 입력해주세요.")

    # 여기부터 수행
       
    

except Exception as e:
    st.error(e)         