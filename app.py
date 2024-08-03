import streamlit as st
import preprocessor, support
import matplotlib.pyplot as plt
import seaborn as sns

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
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)

        col3, col4 = st.columns(2)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(num_links)

        # finding the busiest users in the group(Group level)
        if selected_user == 'Overall':
            x, new_df = support.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                st.title('Most Busy Users')
                ax.bar(x.index, x.values, color='green')
                plt.xticks(rotation = 30)
                st.pyplot(fig)

            with col2:
                st.title("Most Active user Percentage")
                st.dataframe(new_df)

        # WordCloud
        st.title("Wordcloud")
        df_wc = support.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        most_common_df = support.most_common_words(selected_user, df)

        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])

        st.title('Most commmon words')
        st.pyplot(fig)
