import re
from collections import Counter
from urlextract import  URLExtract
from wordcloud import WordCloud
import pandas as pd
import emoji
def fetch_stats(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user'] == selected_user]
    num_messages = df.shape[0]
    words = []
    for i in df['message']:
        words.extend(i.split())
    num_words = len(words)

    num_mediam_msg=df[df['message']=='<Media omitted>\n'].shape[0]

    ## fetch links
    links=[]
    extract = URLExtract()
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, num_words, num_mediam_msg,len(links)

def fetch_most_busy_user(df):
    x = df['user'].value_counts().head()
    df=round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'user':'name','count':'percent'})
    return x,df

def create_word_cloud(selected_user,df):
    f = open('stopenglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            # Remove special symbols but keep letters, numbers, emojis
            word = re.sub(r'[^a-zA-Z0-9\u0800-\uFFFF]', '', word)
            if word and word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp['message']=temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=' '))
    return df_wc

def most_commom_words(selected_user,df):
    f = open('stopenglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            word = re.sub(r'[^a-zA-Z0-9\u0800-\uFFFF]', '', word)

            if word and word not in stop_words:
                words.append(word)

    return pd.DataFrame(Counter(words).most_common(20))


def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    emojis = []

    for message in df['message']:
        for c in message:
            if emoji.is_emoji(c):
                emojis.append(c)
    emoji_counts = Counter(emojis)
    emoji_df = pd.DataFrame(emoji_counts.most_common(len(emoji_counts)), columns=['emoji', 'count'])
    return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    timeline = df.groupby(['year', 'month_num', 'month'])['message'].count().reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append((timeline['month'][i] + '-' + str(timeline['year'][i])))
    timeline['time'] = time
    return timeline

def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    daily_time = df.groupby('only_date')['message'].count().reset_index()
    return daily_time
def week_Activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['month'].value_counts()
def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    user_heatmap=df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count').fillna(0)
    return user_heatmap






