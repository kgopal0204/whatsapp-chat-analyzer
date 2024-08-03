import streamlit as st
import preprocessor
import support

import preprocessor

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a File")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    st.dataframe(df)

    user_list  = df["user"].unique().tolist()
    user_list.remove("group_notification")
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Select option to Analysis", user_list)

    if st.sidebar.button("Show Analysis"):
        num_messages, words, num_media_messages, num_links = support.fetch_stats(selected_user, df)

        st.title("Top Statistics")
        col1, col2 = st.columns(2)

        with col1:
            st.header("1. Total Messages")
            st.title(num_messages)
        with col2:
            st.header("2. Total Words")
            st.title(words)

        col3, col4 = st.columns(2)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(num_links)