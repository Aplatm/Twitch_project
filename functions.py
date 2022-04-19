

# creating a function to return a list of the channels filtered by language and sorting them by rank column
def language_filter_df(language):
    return df[df['Language'] == language].sort_values(by='Rank', ascending= True)
# same for df_stats
def language_filter_df_stats(df_stats, language):
    return df_stats[df_stats['Language'] == language].sort_values(by='Rank', ascending= True)

# finding the streamers with most hours of streaming in df
def stream_time_filter_df():
    return df[['Channel','Stream Time(Hours)']]\
        .sort_values(by='Stream Time(Hours)', ascending= False).reset_index(drop=True)
# same for df_stats
def stream_time_filter_df_stats():
    return df_stats[['Channel','Stream Time(Hours)']]\
        .sort_values(by='Stream Time(Hours)', ascending= False).reset_index(drop=True)

# creating a function what returns depending on the name of the column introduced,
# a list with the channel and the values of the column
def channel_filter_df(column):
    return df[['Channel',column]].sort_values(by=column, ascending= False).reset_index(drop=True)

# same for df_stats
def channel_filter_df_stats(column):
    return df_stats[['Channel',column]].sort_values(by=column, ascending= False).reset_index(drop=True)

# Ordering channels by mean and language in order to find the most popular channels
def one_for_all_filter_df():
    return df[['Watch Time (Hours)','Stream Time(Hours)','Followers','Average viewers','Peak viewers','Language']]\
    .groupby(['Language'], as_index=False).mean().round(2).sort_values(by='Watch Time (Hours)', ascending= False)

# same for df_stats
def one_for_all_filter_df_stats():
    return df_stats[['Watch Time (Hours)','Stream Time(Hours)','Followers','Average Viewers','Peak Views','Language']]\
    .groupby(['Language'], as_index=False).mean().round(2).sort_values(by='Watch Time (Hours)', ascending= False)

# comparation between the two dataframes
def compare_df(df1, df2):
    return df1.merge(df2, on='Language', suffixes=('_2020', '_2022'))

# crating a dataframe filtered just by the average viewers and Channel
def viewers_filter_df():
     return df[['Channel','Average viewers']].sort_values(by='Average viewers', ascending= False).reset_index(drop=True)

# same for df_stats
def viewers_filter_df_stats():
    return df_stats[['Channel','Average Viewers']].sort_values(by='Average Viewers', ascending= False).reset_index(drop=True)

# now we can compare the two dataframes
def compare_viewers_df(df1, df2):
    return df1.merge(df2, on='Channel', suffixes=('_2020', '_2022'))

# creating a function to separate spanish streamers from the rest filtered by the average viewers
def spanish_viewers_filter_df():
    return df[['Channel','Average viewers']].loc[df['Language'] == 'Spanish']\
        .sort_values(by='Average viewers', ascending= False)

# same for df_stats
def spanish_viewers_filter_df_stats():
    return df_stats[['Channel','Average Viewers']].loc[df_stats['Language'] == 'Spanish']\
        .sort_values(by='Average Viewers', ascending= False)

# now we can compare the two dataframes
def compare_spanish_viewers_df(df1, df2):
    return df1.merge(df2, on='Channel', suffixes=('_2020', '_2022'))

# comparation between stream time filtered by language and channel
def compare_stream_time_df(language):
    lengua1= df[['Channel','Stream Time(Hours)']].loc[df['Language'] == language].sort_values(by='Stream Time(Hours)', ascending= False)
    lengua2= df_stats[['Channel','Stream Time(Hours)']].loc[df_stats['Language'] == language].sort_values(by='Stream Time(Hours)', ascending= False)
    return lengua1.merge(lengua2, on='Channel', suffixes=('_2020', '_2022'))


# creating a function to create a horizontal bar plot
def horizontal_bar_plot(df, title, x_label, y_label):
    fig = go.Figure(data=[go.Bar(x=df[x_label], y=df[y_label])])
    fig.update_layout(title=title, xaxis_title=x_label, yaxis_title=y_label)
    fig.show()