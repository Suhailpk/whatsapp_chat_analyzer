from urlextract import URLExtract
from wordcloud import WordCloud,STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
import emoji


extract = URLExtract()


def fecthdata(user_name,df):

    df_user = df[df['User'] == user_name]

    num_messages = df_user.shape[0]

    words = []
    for messages in df_user['Message']:
        words.extend(messages.split())

    num_words = len(words)

    link = []
    for links in df_user['Message']:
        link.extend(extract.find_urls(links))

    num_links = len(link)

    num_media = df_user[df_user['Message'] == '<Media omitted>'].shape[0]

    return num_messages,num_words,num_media,num_links


def wordcloud(df,user):

    if user == 'Overall':
        df_wordcloud = df
    else:
        df_wordcloud =  df[df['User'] == user]
        
    stopwords = set(STOPWORDS)

    wordclouds = WordCloud(width = 800, height = 800,
                background_color ='white',
                stopwords = stopwords,
                min_font_size = 10)

    df_wc = wordclouds.generate(df_wordcloud['Message'].str.cat(sep = " "))
    return df_wc

def busyuser(df):

    df_without_grp_notfcn = df[df["User"] != 'Group notfication']
    counts = df_without_grp_notfcn['User'].value_counts().head()

    user_time_rate = pd.DataFrame(df_without_grp_notfcn['User'].value_counts()/df_without_grp_notfcn.shape[0]*100)

    return counts,user_time_rate

def mostcommon(user,df):
    
    f = open('stop_hinglish.txt','r')
    stopwords = f.read()
    stopwords = stopwords.split('\n')
    
    if user == 'Overall':
        top_words = df[df['Message'] != '<Media omitted>']
    else:
        top_words = df[(df['User'] == user) & (df['Message'] != '<Media omitted>')]
    
    words = []
    for messages in top_words['Message']:
        for message in messages.lower().split():
            if message not in stopwords:
                words.append(message)
                
    most_common = pd.DataFrame(Counter(words).most_common(20))
    return most_common


def top_emojis(user,df):
    
    if user == 'Overall':
        df_emojis = df
    else:
        df_emojis = df[df['User'] == user]
    
    emojis = []
    for message in df_emojis['Message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    emojis_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    
    return emojis_df


def monthly_timeline(user,df):

    if user == 'Overall':
        df_month = df
    else:
        df_month = df[df['User'] == user]
    
    temp = df_month.groupby(['Year','Month_num','Month']).count()['Message'].reset_index()
    
    time = []
    for i in range(temp.shape[0]):
        time.append(str(temp['Month'][i])+ '-' + str(temp['Year'][i]))
    temp['Month_year'] = time
    
    return temp

def activity_day(user,df):
    if user == 'Overall':
        df_activity_day = df
    else:
        df_activity_day = df[df['User'] == user]
        
    return df_activity_day['Day_name'].value_counts()


def activity_month(user,df):
    if user == 'Overall':
        df_activity_month = df
    else:
        df_activity_month = df[df['User'] == user]
        
    return df_activity_month['Month'].value_counts()