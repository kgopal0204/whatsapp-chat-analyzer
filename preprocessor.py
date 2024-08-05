import pandas as pd
import re


def preprocess(data):
    pattern = r"\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s[a,p,A,P]{1}[m,M]{1}\s-\s"
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    df["message_date"] = df["message_date"].str.replace("\u202f", " ")

    # convert data type of message_date
    def convert_date(date_str):
        if re.search(r"\d{1,2}/\d{1,2}/\d{4}", date_str):
            return pd.to_datetime(date_str, format="%d/%m/%Y, %I:%M %p - ")
        elif re.search(r"\d{1,2}/\d{1,2}/\d{2}", date_str):
            return pd.to_datetime(date_str, format="%d/%m/%y, %I:%M %p - ")
        else:
            return pd.NaT  # Return NaT if the date format is not recognized

    df["message_date"] = df["message_date"].apply(convert_date)

    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['hourly_period'] = period

    return df
