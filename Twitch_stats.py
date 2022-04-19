
# Importing the libraries
import pandas as pd
import sys
sys.path.append("../")
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from functions import *

# driver configuration
opciones=Options()

opciones.add_experimental_option('excludeSwitches', ['enable-automation'])
opciones.add_experimental_option('useAutomationExtension', False)
opciones.add_experimental_option("detach",True)
opciones.headless=False    # si True, no aperece la ventana (headless=no visible)
# add_argument('--start-maximized')         # comienza maximizado
# opciones.add_argument('user-data-dir=selenium')    # mantiene las cookies
# opciones.add_extension('driver_folder/adblock.crx')       # adblocker
opciones.add_argument('--incognito')

driver = "../../chromedriver.exe" # remember substitute this for your driver path
driver = webdriver.Chrome(driver,options = opciones)

# Reading the data from the csv file
df = pd.read_csv('../data/twitchdata-update.csv')

# Getting driver the url
url = 'https://sullygnome.com/channels/365/watched'
driver.get(url)

# Getting the html code
xpath = '//*[@id="mostWatchedChannelscontainer"]'
find_element = driver.find_element_by_xpath(xpath)

# Getting the html code
tr = driver.find_elements_by_tag_name('tr')

# Putting the html code in a list
stats = []
driver.find_elements_by_tag_name('td')[0].text

# Getting the data from the html code and append it to the list
for i in range(len(driver.find_elements_by_tag_name('td'))):
   stats.append(driver.find_elements_by_tag_name('td')[i].text)

driver.quit()

# Divide the list in list of lists (each list is a row) of 14 elements
stats_list = []
for i in range(len(stats)):
    if i%14 == 0:
        stats_list.append([])
    stats_list[i//14].append(stats[i])
stats_list.head()

# create a dataframe from the list of lists
df_stats = pd.DataFrame(stats_list)
df_stats.columns = ['Rank', 'Viewers', 'Channel', 'Watch Time (Hours)', 'Stream Time(Hours)', 'Peak Views', 'Average Viewers', 'Followers', 'Followers gained', 'Views gained', 'Partnered', 'Mature', 'Language', 'Average Follower Growth']
df_stats.head()

# cleaning data in stats_list dataframe
# checking null values
df_stats.isnull().sum()

# drop column views and average follower growth
df_stats.drop(columns=['Viewers'], inplace=True)
df_stats.drop(columns=['Average Follower Growth'], inplace=True)

# Fixing spaces cells in dataframe
df_stats['Watch Time (Hours)'] = df_stats['Watch Time (Hours)'].str.replace('\n', ' ')
df_stats['Stream Time(Hours)'] = df_stats['Stream Time(Hours)'].str.replace('\n',' ')
df_stats['Peak Views'] = df_stats['Peak Views'].str.replace('\n','')
df_stats['Average Viewers'] = df_stats['Average Viewers'].str.replace('\n',' ')
df_stats['Views gained'] = df_stats['Views gained'].str.replace('\n','')

# filling Mature empty cells with True or false values
for i in range(len(df_stats)):
    if df_stats['Mature'][i] == 'Mature':
        df_stats['Mature'][i] = 'True'
    else:
        df_stats['Mature'][i] = 'False'

# filling partnered empty cells with 'Unknown Status'.
for i in range(len(df_stats)):
    if df_stats['Partnered'][i] != 'Partnered':
        df_stats['Partnered'][i] = 'Unknown Status'

# Checking dataframes
df.head()
df_stats.head()

# making original df from csv file same as df_stats
# inserting Rank column in original df
df.insert(0, 'Rank', df_stats['Rank'])

# converting Watch time(Minutes) values to hours with the same format as df_stats Watch Time(Hours) values
for i in range(len(df)):
    df['Watch time(Minutes)'][i] = df['Watch time(Minutes)'][i]/60

# converting Stream time(minutes) values to hours with the same format as df_stats Stream Time(Hours) values
for i in range(len(df)):
    df['Stream time(minutes)'][i] = df['Stream time(minutes)'][i]/60

# renaming columns in df to match df_stats(Minutes to Hours)
df.rename(columns={'Watch time(Minutes)':'Watch Time (Hours)', 'Stream time(minutes)':'Stream Time(Hours)'}, inplace=True)
df.head()

# Transforming df_stats to match df in the same format(replacing commas for nothing)
for i in range(len(df_stats)):
    df_stats['Watch Time (Hours)'][i] = df_stats['Watch Time (Hours)'][i].replace(',','')
    df_stats['Stream Time(Hours)'][i] = df_stats['Stream Time(Hours)'][i].replace(',','')
    df_stats['Peak Views'][i] = df_stats['Peak Views'][i].replace(',','')
    df_stats['Average Viewers'][i] = df_stats['Average Viewers'][i].replace(',','')
    df_stats['Views gained'][i] = df_stats['Views gained'][i].replace(',','')
    df_stats['Followers gained'][i] = df_stats['Followers gained'][i].replace(',','')
    df_stats['Followers'][i] = df_stats['Followers'][i].replace(',','')

# cutting off df in rank to take only top 50
df = df.iloc[:50]
df.head()

# transforming string values to numeric values in df
df['Rank'] = df['Rank'].astype(int)
df['Views gained'] = df['Views gained'].astype(int)
df['Followers gained'] = df['Followers gained'].astype(int)
df['Average viewers'] = df['Average viewers'].astype(int)
df['Peak viewers'] = df['Peak viewers'].astype(int)
df['Followers'] = df['Followers'].astype(int)
df['Average viewers'] = df['Average viewers'].astype(int)
df['Views gained'] = df['Views gained'].astype(int)
df['Stream Time(Hours)'] = df['Stream Time(Hours)'].astype(int)
df['Watch Time (Hours)'] = df['Watch Time (Hours)'].astype(int)


# Deleting all elements in df_stats when match '(', in order to eliminate the
# % change from last year and transform the strings to int

for i in range(len(df_stats)):
    for j in range(len(df_stats.columns)):
        if df_stats.columns[j] == 'Average Viewers':
            df_stats.iloc[i,j] = df_stats.iloc[i,j].split('(')[0]
        if df_stats.columns[j] == 'Peak Views':
            df_stats.iloc[i,j] = df_stats.iloc[i,j].split('(')[0]
        if df_stats.columns[j] == 'Followers':
            df_stats.iloc[i,j] = df_stats.iloc[i,j].split('(')[0]
        if df_stats.columns[j] == 'Followers gained':
            df_stats.iloc[i,j] = df_stats.iloc[i,j].split('(')[0]
        if df_stats.columns[j] == 'Views gained':
            df_stats.iloc[i,j] = df_stats.iloc[i,j].split('(')[0]
        if df_stats.columns[j] == 'Stream Time(Hours)':
            df_stats.iloc[i,j] = df_stats.iloc[i,j].split('(')[0]
        if df_stats.columns[j] == 'Watch Time (Hours)':
            df_stats.iloc[i,j] = df_stats.iloc[i,j].split('(')[0]

# same operation with df_stats ( converting them to numeric values)
df_stats['Rank'] = df_stats['Rank'].astype(int)
df_stats['Views gained'] = df_stats['Views gained'].astype(int)
df_stats['Followers gained'] = df_stats['Followers gained'].astype(int)
df_stats['Average Viewers'] = df_stats['Average Viewers'].astype(int)
df_stats['Peak Views'] = df_stats['Peak Views'].astype(int)
df_stats['Followers'] = df_stats['Followers'].astype(int)
df_stats['Average Viewers'] = df_stats['Average Viewers'].astype(int)
df_stats['Views gained'] = df_stats['Views gained'].astype(int)
df_stats['Stream Time(Hours)'] = df_stats['Stream Time(Hours)'].astype(int)
df_stats['Watch Time (Hours)'] = df_stats['Watch Time (Hours)'].astype(int)

# Checking if the data types are correct
df.info()
df_stats.info()

# Calling function filtered by language & sorted by rank in df
language_filter_df('English')

# Calling function filtered by language & sorted by rank in df_stats
language_filter_df_stats('Spanish')

# Calling function filtered by the streamers with most hours of streaming in df
stream_time_filter_df()

# Calling function filtered by the streamers with most hours of streaming in df_stats
stream_time_filter_df_stats()

# calling function in order to get a list with the channel and the values of the column introduced
channel_filter_df('Watch Time (Hours)')

# Calling function in order to get a list with the channel and the values of the column introduced in df_stats
channel_filter_df_stats('Watch Time (Hours)')

# calling a function to get a dataframe with the mean of all numeric columns
# filtered by language sorted by hours watched
one_for_all_filter_df()

# calling a function to get a dataframe with the mean of all numeric columns filtered
# by language sorted by hours watched in df_stats
one_for_all_filter_df_stats()

# comparation between the two dataframes by one for alls functions
compare_df(one_for_all_filter_df(), one_for_all_filter_df_stats())

# calling a function to get the mean average viewers
viewers_filter_df()

# calling a function to get the mean average viewers in df_stats
viewers_filter_df_stats()

# comparation between the average viewers in 2020 and the average viewers in 2022
compare_viewers_df(viewers_filter_df(), viewers_filter_df_stats())

# calling a function to get the spanish streamers separated from the rest
spanish_viewers_filter_df()

# same with df_stats
spanish_viewers_filter_df_stats()

# calling a function to see hours streamed in both years
compare_stream_time_df('Spanish')
compare_stream_time_df('English')

# creating a bar plot for the average viewers in df
horizontal_bar_plot(viewers_filter_df(), 'Average viewers 2020',  'Average viewers','Channel')

# creating a bar plot for the average viewers in df
horizontal_bar_plot(viewers_filter_df(), 'Average viewers 2020', 'Channel', 'Average viewers')

# creating a bar plot for the average viewers in df_stats
horizontal_bar_plot(viewers_filter_df_stats(), 'Average viewers 2022', 'Channel', 'Average Viewers')

# creating a bar plot just for spanish viewers in df
horizontal_bar_plot(spanish_viewers_filter_df(), 'Average viewers 2020', 'Channel', 'Average viewers')

# creating a bar plot just for spanish viewers in df_stats
horizontal_bar_plot(spanish_viewers_filter_df_stats(), 'Average viewers 2022', 'Channel', 'Average Viewers')

# creating a bar plot for the average time in stream in df
horizontal_bar_plot(stream_time_filter_df(), 'Average stream time 2020', 'Channel', 'Stream Time(Hours)')

#creating a bar plot for the average time in stream in df_stats
horizontal_bar_plot(stream_time_filter_df_stats(), 'Average stream time 2022', 'Channel', 'Stream Time(Hours)')

# creating a connection to the database
mypasswd=open('pw.txt','r').readlines()[0]
engine = create_engine(f'mysql+pymysql://Aplatm:{mypasswd}@127.0.0.1:3306')
engine.execute('create database Twitch_Analytics')
engine = create_engine(f'mysql+pymysql://Aplatm:{mypasswd}@127.0.0.1:3306/Twitch_Analytics')

df= df.copy()
df_stats= df_stats.copy()

# saving dataframes to csv files
df.to_csv('df.csv')
df_stats.to_csv('df_stats.csv')

# creating a table in the database
df.to_sql('2020_stats', engine, if_exists='replace', index=False)
df_stats.to_sql('2022_stats', engine, if_exists='replace', index=False)