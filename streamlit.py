import streamlit as st
from shaping_data import df
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df2 = df.groupby(["Name", "Genre", "Review_Year", "Review_Month", 'Scores'], as_index=False)['hours'].sum()
df2["Review_Month"] = pd.to_numeric(df2["Review_Month"])
df2["Review_Year"] = pd.to_numeric(df2["Review_Year"])
df2["Scores"] = pd.to_numeric(df2["Scores"])
df2["hours"] = pd.to_numeric(df2["hours"])

df2["Name"] = df2["Name"].drop_duplicates(keep='first')
#df2 = df2[(df2["Genre"] != 'Pinball') & (df2["Genre"] != 'Card') & (df2["Genre"] != 'Party') & (df2["Genre"] != 'Flight')]
df2 = df2.dropna()

year = st.sidebar.slider(label='Select a year', min_value=1998, max_value=2020, value=[1998, 2020], step=1)
month = st.sidebar.slider(label='Select a month', min_value=1, max_value=12, value=[1, 12], step=1)

genre = st.sidebar.selectbox("Which genre DO you want to display ?", ['All', 'Action', 'Adventure', 'Racing', 'Compilation', 'Platformer', 'Shooter', 'Music', 'Strategy', 'RPG', 'Fighting', 'Puzzle',
                                                                      'Simulation', 'Board', 'Other', 'Sports', 'Trivia'])



st.header('Information about this analysis')
st.write('1 - Here is a quick exploratory data analysis about pc video game reviews and gaming time.')
st.write('2 - This analysis was made by merging Steam data (downloaded from https://www.kaggle.com/datasets/tamber/steam-video-games) with IGN data. '
         'IGN is a video game media and website. It regularly publishes video game analysis and reviews. '
         'IGN data was retrieved with web scrapping. Since Steam is a software only available on PC, the data scrapped from IGN covers only PC games.')
st.write('3 - IGN usually makes review up to two weeks after a game is released. Since it might be confusing, each chart will have a little description attached. ' )
st.write('5 - The dataset resulting from the merge of Steam and IGN data contains 892 rows, each row for a game. '
         'Due to insufficient data, reality is most likely to differ from the results shown here.')
st.write('6 - My name is Youenn WILSON. This is my first fully autonomus data analysis project.')


if genre == "All":
    df2 = df2
    genre_no = st.sidebar.selectbox("Which genre DON'T you want to display ?",
                                    ['I want to display all genres', 'Action', 'Adventure', 'Racing', 'Compilation',
                                     'Platformer', 'Shooter', 'Music', 'Flight', 'Strategy', 'RPG', 'Fighting',
                                     'Puzzle',
                                     'Simulation', 'Board', 'Card', 'Other', 'Pinball', 'Party', 'Sports', 'Trivia'])

    if genre_no == "I want to display all genres":
        df2 = df2
        mask_big = st.sidebar.selectbox("Do you want to mask out the 'RPG' genre ?",
                                        ['No', 'Yes'])
        mask_insinif = st.sidebar.selectbox("Do you want to mask out the 'Trivia', 'Flight', 'Pinball' and 'Party' genres ?",
                                        ['No', 'Yes'])
        if mask_big == 'Yes':
            df2 = df2[(df2["Genre"] != 'RPG')]
        if mask_insinif == "Yes":
            df2 = df2[(df2["Genre"] != "Trivia") & (df2["Genre"] != "Flight") & (df2["Genre"] != "Pinball") & (
                    df2["Genre"] != "Party")]
    else:
        df2 = df2[df2["Genre"] != genre_no]


else:
    df = df2[df2["Genre"] == genre]


hours = st.sidebar.slider(label="Select a range of hours spent on a game (step = 10,000)", min_value=0.1, max_value=float(max(df2['hours'])), value=[0.1, float(max(df2['hours']))], step=10000.0)
score = st.sidebar.slider(label="Select a range of review score", min_value=1.5, max_value=10.0, value=[1.5, 10.0], step=5000.0)

df2 = df2[(df2["Review_Month"] >= month[0]) & (df2["Review_Month"] <= month[1]) & (df["Review_Year"] >= year[0]) & (df2["Review_Year"] <= year[1])]
df2 = df2[(df2["hours"] >= hours[0]) & (df2["hours"] <= hours[1]) & (df["Scores"] >= score[0]) & (df2["Scores"] <= score[1])]

st.header('Dashboard')
st.subheader(f'Month:{month} / Year:{year} / Genre : {genre}')



st.dataframe(df2)
st.header(f'Visualisation of time spent on games according to release year {year}')
st.subheader(f'Lineplot years')
fig1, ax1 = plt.subplots()
sns.lineplot(data=df2, x="Review_Year", y="hours")
ax1.tick_params(axis='x', labelsize=7, rotation=40)
plt.xlim(1998, 2020)
st.pyplot(fig1)
st.write("This chart represent the time spent on PC video games according to the year of game releases. We may see that on average, as of 2020, the game released in 2000 and 2013 seem "
         "to be the ones players spend the most time on.")


st.header('Which genre is the most famous ?')
fig2, ax2 = plt.subplots()
sns.barplot(data=df2, x='Genre', y='hours')
ax2.tick_params(axis='x', labelsize=7, rotation=40)
ax2.tick_params(axis='y', labelsize=7, rotation=40)
st.pyplot(fig2)
st.write('On the chart, we can see that "RPG" games are, by far, the game that counts the most hours, followed by "Shooter" and "Strategy" games.')

st.write('As we see, "Trivia, Flight, "Pinball" and "Party genres are really insignificant. You can choose to mask them out. ')


st.header('Does the most famous games have the best reviews ?')
st.write('According to the scatterplot bellow, we may see that the games that are played the most have the best reviews. However, the reciprocal is not true.'
         ' (reduce the hour range for a better visualisation)'
          'Please be patient, this chart may take a few seconds to load !')
fig3, (ax3) = plt.subplots()
sns.scatterplot(data=df2, x="Scores", y='hours', hue='Name', ax=ax3)
ax3.legend(fontsize=6, ncols=4, loc='upper center', bbox_to_anchor=(0.5, -0.2))
ax3.tick_params(axis='x', labelsize=9)
st.pyplot(fig3)


#streamlit run streamlit.py
