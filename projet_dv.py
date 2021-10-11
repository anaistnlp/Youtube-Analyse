import streamlit as st
import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objects as go
import plotly.express as px
import controller as ctrl
import model
from model import url


def chart_inline(graph):
    ncol = len(graph)

    cols = st.columns(ncol)

    for i in range(len(graph)):
        cols[i].plotly_chart(graph[i], use_container_width=True)


st.title('\U0001F50D Analysing my Youtube data \U0001F50E')
st.image(model.ytb)

st.sidebar.title("""
    Anaïs TONLOP
    Data Visualization Project, 2021""")

st.sidebar.header("\U0001F517 Find me!")
st.sidebar.write(f"[![Connect]({url['linkedin']['img']})]({url['linkedin']['url']})&nbsp[![Connect]({url['github']['img']})]({url['github']['url']})")



st.markdown("""
    ##### **Let me tell you a story about my experience with streaming platforms and how it influenced my consumption of YouTube.**

    ##### **For the most of us we spend 1000 hours on YouTube but let me tell you that it is not the case for everyone**
""")

st.plotly_chart(model.hist_date)
st.markdown("""
    As we can see, **July 2019** was a crucial date in my consumption of this platform.

    Previously I used to consume **more than 200 videos** while today as we can see this trend is **decreasing over the years**

""")

st.markdown("###### **let's try to look out some other graph to get more insights so we can understand why it is decreasing that much.**")
st.write('\n')

chart_inline([model.line_hour_year, model.hist_hour])

st.markdown("""
    The line graph shows that during all these days, my daily video consumption has **decreased dramatically since my admission at EFREI in 2018**.

    On the histogram, it is clear that, even if my consumption decreased over the years, it **did not affect the time slot during which I watch my videos**.

    ###### **So now, we can wonder, “has my consumption decreased because I don't have time to watch youtube anymore” or “is it because I don't find it interesting anymore”?**

    ##### Comparison of favorite categories
""")

st.plotly_chart(model.fav_categories)

st.markdown("""
    A very interesting graph is when we look at the comparison of the categories I watch the most between 2017 and 2021.

    The bar plot shows that, even if the order changed, it is still the same categories that I watch the most.

    It shows that there is no correlation between my use of the platform and my interest in it.
""")

chart_inline([model.type_vid, model.top_ytb])

st.markdown("""
    The bar chart displays the youtuber I watch the most. We can see that **they all belong to my favorite categories**. However, they are **not** my favorite youtubers.

    If we assume that a youtuber is my favorite according to the number of videos I watch of him, it is not relevant in my case because **my favorite youtubers are not necessarily those who make the most videos.**

    **Other parameters can come in consideration**, such as the quality of the video or the concepts and ideals developed.

    ##### **My way of consuming the platform is still the same over the years, it's just that the time spent on youtube has decreased a lot.**

    ##### **But the thing I didn't tell you is that I started using new streaming platforms like Netflix.**

    ##### **The arrival of new competitors has strongly influenced my youtube consumption.**
""")
