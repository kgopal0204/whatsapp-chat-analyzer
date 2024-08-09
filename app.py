import streamlit as st
import preprocessor
import support
import matplotlib.pyplot as plt
import seaborn as sns
import time

st.sidebar.title("Whatsapp Chat Analyzer")
st.title("WhatsApp Chat Analyzer")
st.markdown("**Developed with Streamlit, Developed by Krishna Gopal**")

uploaded_file = st.sidebar.file_uploader("Choose a WhatsApp Text File")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    # st.dataframe(df)

    user_list = df["user"].unique().tolist()
    user_list.remove("group_notification")
    user_list.sort()
    user_list.insert(0, "Overall Group")

    selected_user = st.sidebar.selectbox("Select option to Analysis", user_list)

    st.header("Analysis of " + selected_user + " :")

    if st.sidebar.button("Show Analysis"):
        start_date,last_date, num_messages, words, num_media_messages, num_links, members = (
            support.fetch_stats(selected_user, df))

        with st.spinner("Analyzing..."):
            time.sleep(2)

        st.title("Top Statistics :")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Chat From:")
            st.header(start_date)
        with col2:
            st.subheader("Chat To:")
            st.header(last_date)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Total Messages:")
            st.header(num_messages)
        with col2:
            st.subheader("Total Used Words:")
            st.header(words)

        col3, col4 = st.columns(2)
        with col3:
            st.subheader("Total Media Shared:")
            st.header(num_media_messages)
        with col4:
            st.subheader("Total Links Shared:")
            st.header(num_links)

        st.subheader("Total Members:")
        st.header(members)

        # monthly timeline
        st.title("Monthly Timeline :")
        timeline = support.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation=90)
        st.pyplot(fig)

        # daily timeline
        st.title("Daily Timeline :")
        daily_timeline = support.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # activity map
        st.title('Activity Maps :')
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day = support.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month")
            busy_month = support.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Heatmap :")
        user_heatmap = support.period_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        sns.heatmap(user_heatmap, ax=ax)
        st.pyplot(fig)

        # finding the busiest users in the group(Group level)
        if selected_user == 'Overall Group':
            x, new_df = support.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                st.title("Most Active user Percentage")
                st.dataframe(new_df)

            with col2:
                st.title('Most Busy Users')
                ax.bar(x.index, x.values, color='green')
                plt.xticks(rotation=30)
                st.pyplot(fig)

        # WordCloud
        st.title("Wordcloud :")
        df_wc = support.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        st.title('Most Common Words :')
        most_common_df = support.most_common_words(selected_user, df)

        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1], color="#d35400")
        st.pyplot(fig)

        # emoji analysis
        emoji_df = support.emoji_helper(selected_user, df)
        st.title("Emoji Analysis :")

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df["count"].head(), labels=emoji_df["emoji"].head(), autopct="%0.2f")
            st.pyplot(fig)
