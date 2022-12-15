import re
import pandas as pd

def preprocess_data(file):


    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    messages = re.split(pattern,file)[1:]
    dates = re.findall(pattern,file)

    def datetimeclean(data):
        string = data.split(',')
        date,time = string[0],string[1]
        time = time.split('-')
        time = time[0].strip()
        return date+" "+time

    df = pd.DataFrame({'Messages':messages,
             'Dates':dates})

    df['Dates'] = df['Dates'].apply(lambda x:datetimeclean(x))

    user = []
    message = []
    for messages in df['Messages']:
        
        entry = re.split('([\w\W]+?):\s',messages)
        if entry[1:]:
            user.append(entry[1])
            message.append(entry[2])
        else:
            user.append('Group notfication')
            message.append(entry[0])
    
    df['User'] = user
    df['Message'] = message

    df['Message'] = df['Message'].apply(lambda x: x.split('\n')[0])

    del df['Messages']

    df['Only date'] = pd.to_datetime(df['Dates']).dt.date

    df['Year'] = pd.to_datetime(df['Dates']).dt.year

    df['Month_num'] = pd.to_datetime(df['Dates']).dt.month

    df['Month'] = pd.to_datetime(df['Dates']).dt.month_name()

    df['Day'] = pd.to_datetime(df['Dates']).dt.day

    df['Day_name'] = pd.to_datetime(df['Dates']).dt.day_name()

    df['Hour'] = pd.to_datetime(df['Dates']).dt.hour

    df['Minute'] = pd.to_datetime(df['Dates']).dt.minute

    return df


