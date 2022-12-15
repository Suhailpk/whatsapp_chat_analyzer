import streamlit as st
import preprocess
import stats
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

st.sidebar.title('WhatsApp Chat Analyzer')

uploaded_file = st.sidebar.file_uploader('Choose a file')

if uploaded_file is not None:
    
    bytes_data = uploaded_file.getvalue()

    data = bytes_data.decode("utf-8")

    df = preprocess.preprocess_data(data)


    user_list = df['User'].unique()

    user_list = user_list.tolist()

    user_list.remove('Group notfication')

    user_list.sort()

    user_list.insert(0,'Overall')

    user_name = st.sidebar.selectbox('Show analysis with respect to',user_list)

    st.title(f'WhatsApp Chat Analysis for {user_name}')

    button = st.sidebar.button('Show Analysis')

    if button:

        if user_name == 'Overall':

            overall_df =  df['User']

            num_messages,num_words,num_media,num_links =  stats.fecthdata(user_name=overall_df,df=df)

            col1,col2,col3,col4 = st.columns(4)

            with col1:
                st.header('Total No. Of Messages')
                st.title(num_messages)

            with col2:
                st.header('Total No. Of Words')
                st.title(num_words)

            with col3:
                st.header('Total No. Of Media Shared')
                st.title(num_media)

            with col4:
                st.header('Total No. Of Links Shared')
                st.title(num_links)

            st.title("Most Busy Users")
            counts,user_rate = stats.busyuser(df)
            fig,ax = plt.subplots()

            col1,col2 = st.columns(2)
            with col1:
                ax.bar(counts.index,counts.values,color = 'red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(user_rate)

        else:

            num_messages,num_words,num_media,num_links =  stats.fecthdata(user_name=user_name,df=df)

            col1,col2,col3,col4 = st.columns(4)

            with col1:
                st.header('Total No. Of Messages')
                st.title(num_messages)

            with col2:
                st.header('Total No. Of Words')
                st.title(num_words)

            with col3:
                st.header('Total No. Of Media Shared')
                st.title(num_media)

            with col4:
                st.header('Total No. Of Links Shared')
                st.title(num_links)

        #wordcloud        
        st.title("Wordcloud")
        wordcloud = stats.wordcloud(df=df,user=user_name)
        fig,ax = plt.subplots()
        ax.imshow(wordcloud)
        ax.axis(False)
        st.pyplot(fig)

        #most common words
        st.title('Most Common Words')
        most_common_df = stats.mostcommon(user=user_name,df=df)

        fig,ax= plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #most common emojis
        st.title('Most Common Emojis')
        emojis_df = stats.top_emojis(user=user_name,df=df)
        emojis_df.columns = ['Emoji','Count']
        fig,ax = plt.subplots()

        col1,col2 = st.columns(2)
        with col1:
            st.dataframe(emojis_df)

        with col2:
            emojis_count = list(emojis_df['Count'])
            perlist = [(i/sum(emojis_count))*100 for i in emojis_count]
            emojis_df['Percenatage use'] = np.array(perlist)
            st.dataframe(emojis_df)
        
        #monthly timeline
        st.title('Monthly Timeline')
        df_month = stats.monthly_timeline(user=user_name,df=df)
        fig,ax =  plt.subplots()

        ax.plot(df_month['Month_year'],df_month['Message'],color = 'green')
        plt.xticks(rotation = 'vertical')
        plt.tight_layout()
        st.pyplot(fig)

        #Activity maps

        st.title('Activity maps')

        col1,col2 = st.columns(2)
        with col1:
            st.header('Most Busy Day')
            df_activity_day = stats.activity_day(user=user_name,df=df)
            fig, ax = plt.subplots()
            ax.bar(df_activity_day.index,df_activity_day.values,color = 'purple')
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)

        with col2:
            st.header('Most Busy Months')
            df_activity_month = stats.activity_month(user=user_name,df=df)
            fig, ax = plt.subplots()
            ax.bar(df_activity_month.index,df_activity_month.values,color = 'orange')
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)
                
                
                
               
                
            



                



