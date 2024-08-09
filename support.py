from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extractor = URLExtract()


def fetch_stats(selected_user, df):

    if selected_user != "Overall Group":
        df = df[df["user"] == selected_user]

    # starting date of group
    start_date = df["only_date"].min()

    # last date of group
    last_date = df["only_date"].max()

    # fetch number of messages
    num_messages = df.shape[0]
    # fetch number of words
    words = []
    for message in df['message']:
        words.extend(message.split(" "))

    # fetch number of media messages
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    # No. of group members
    members = df["user"].nunique() -1

    # fetch number of links shared
    links = []
    for message in df["message"]:
        links.extend(extractor.find_urls(message))

    return start_date,last_date, num_messages, len(words), num_media_messages, len(links), members


def most_busy_users(df):
    x = df["user"].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'count': 'percent'})
    return x, df


def create_wordcloud(selected_user, df):

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall Group':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=400, height=400, min_font_size=8, background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc


def most_common_words(selected_user, df):

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall Group':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(12))
    return most_common_df


def emoji_helper(selected_user, df):
    if selected_user != 'Overall Group':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))), columns=["emoji", "count"])
    # emoji_df.rename(columns={0:"emoji", 1:"count"})

    return emoji_df


def monthly_timeline(selected_user, df):

    if selected_user != 'Overall Group':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline


def daily_timeline(selected_user, df):

    if selected_user != 'Overall Group':
        df = df[df['user'] == selected_user]

    daily_timeline_df = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline_df


def week_activity_map(selected_user, df):

    if selected_user != 'Overall Group':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()


def month_activity_map(selected_user, df):

    if selected_user != 'Overall Group':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()


def period_heatmap(selected_user, df):

    if selected_user != 'Overall Group':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='hourly_period', values='message',
                                  aggfunc='count').fillna(0)

    return user_heatmap
