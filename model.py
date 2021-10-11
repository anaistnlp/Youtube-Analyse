from PIL import Image
import controller as ctrl
import os
import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objects as go
import plotly.express as px

url = {
       "linkedin" : {
           "img" : "https://img.shields.io/badge/Anaïs-0077B5?style=for-the-badge&logo=linkedin&logoColor=white&link=https://www.linkedin.com/in/anais-tonlop/",
           "url" : "https://www.linkedin.com/in/anais-tonlop/"
           } ,
       "github" : {
           "img" : "https://img.shields.io/badge/Anaïs-171B23?style=for-the-badge&logo=github&logoColor=white&link=https://github.com/anaistnlp",
           "url" : "https://github.com/anaistnlp"
           }
       }

ytb = "youtube.png"
file_name = "watch-history.json" # dataset
project_folder = os.path.dirname(__file__) # récupérer le dossier du projet
file = os.path.join(project_folder, file_name) # récupérer chemin du fichier dans le dossier du pj

ytb_logo = Image.open(os.path.join(project_folder,ytb))
df = ctrl.load_data(file)

df1 = ctrl.get_freq_mult(df, ['year', 'hour'])

df2 = df.groupby(['weekday','hour']).size().unstack()


##########################################################################################################
############################################### GRAPHS ###################################################
##########################################################################################################


# VIDEOS WATCHED THROUGH YEARS 
hist_date = px.histogram(df, 'date', title='Videos Watched through years')

hist_date.add_vline(x=pd.to_datetime('2019-06-30').date(), line_width=3, line_dash="dash", line_color="red")

hist_date.update_layout(bargap=0.2, xaxis_title="Date", yaxis_title="Number of Videos")

hist_date.add_vrect(x0="2017-01-01", x1="2019-06-30", 
              annotation_text="more than 200 videos watched", annotation_position="top right",
              fillcolor="pink", opacity=0.25, line_width=0)


# FREQUENCY OF VIDEO WATCHED BY YEAR AND HOUR ###############
year_colors={
    2017: "#727172", 
    2018: "#b2adaa",
    2019: "#afbbc9",
    2020: "#bedaf0",
    2021 : "#2d7fc5"
}

line_hour_year = px.line(df1.fillna(0),
                         x="hour",
                         y="count",
                         color='year',
                         color_discrete_map=year_colors,
                         title='Videos watched in a day through the years')

line_hour_year.update_layout(plot_bgcolor='white')
                         

# AVG OF VIDEO WATCHED BY HOUR
hist_hour = px.histogram(df1,
                         x='hour',
                         y='count',
                         title = 'Average of video watched by hour',
                         marginal='box',
                         histfunc='avg',
                         nbins=24)

hist_hour.add_trace(go.Scatter( x=[i for i in range(24)], y=df1.groupby(['year','hour']).mean()['count'],
                    mode='lines',
                    name='Trend'))


hist_hour.update_layout(bargap = .2)


# TYPE OF VIDEOS WATCHED
df3 = pd.read_csv('dataset.csv') # scrapping data 
frame = [df, df3]
f = pd.concat(frame, axis=1)
by_genre = f.groupby('type').size().to_frame().sort_values([0],ascending=False).head(7).reset_index()
by_genre.rename(columns={0:'count'}, inplace=True)

type_vid = px.pie(by_genre, values='count', names='type', 
             color_discrete_sequence=px.colors.sequential.RdBu,
             title='Type of videos watched')


# TOP 5 YOUTUBERS
mask = (f['author']!='sam zirah') & (f['author']!='Non Stop') &( f['author']!='Marie' )&( f['author']!='VDBUZZ') & (f['author']!='Bastos') # j'ai honte
truc = f[mask].groupby(['author','type']).size().to_frame().sort_values([0],ascending=False).head(5).reset_index()
truc.rename(columns={0:'count'}, inplace=True)

color={'People & Blogs':'#b2182b',
        'Entertainment':'#67001f',
        'Education':'#d1e5f0',
        'Howto & Style':'#d6604d'}

top_ytb = px.bar(truc, x='author', y='count', 
       color='type', 
       color_discrete_map=color,
       title='top 5 most watched youtubers')



# Favorite Categories comparaison
df_dataset = pd.read_csv('dataset.csv')

years = [2017, 2021]
data_y = []
for y in years :
    sub_df = ctrl.filter_df(df_dataset, year=y, nbr=6)
    bar = go.Bar(name=str(y), x=sub_df['type'], y=sub_df['count'])
    data_y.append(bar)

fav_categories = go.Figure(data=data_y)
