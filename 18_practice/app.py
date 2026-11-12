from api import get_post
import streamlit as st
import pandas as pd

try:

    
    st.title("d")
    COLUMNS = ["글", "번호", "제목", "유저"]


    title = st.text_input("제목")
    limit = st.number_input("이거필수인가")
    if title and limit:
        if st.button("게시글 조회"):
            posts = get_post(title, limit)

        if posts:        
            st.divider()
            df = pd.DataFrame(posts)
            st.dataframe(df, hide_index=True)        

except Exception as e:
    print(e)