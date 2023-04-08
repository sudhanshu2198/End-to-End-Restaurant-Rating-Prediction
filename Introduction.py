import streamlit as st
import pandas as pd
import numpy as np
from matplotlib import image
import os

st.title("Restaurant Rating Prediction")
st.subheader("The main goal of this is to get insights on restaurants which people like visit and to identify the rating of the restaurant.")
st.write("Restaurant Rating has become the most commonly used parameter for judging a restaurant for any individual.\
          Rating of a restaurant depends on factors like reviews, area situated, average cost for two people, votes, \
          cuisines and the type of restaurant.")

col1,col2=st.columns(2)
with col1:
    github="https://github.com/sudhanshu2198"
    var1=st.write("Github Profile Link: {}".format(github))
with col2:
    kaggle="https://www.kaggle.com/sudhanshu2198"
    var1=st.write("Kaggle Link: {}".format(kaggle))

file_dir=os.path.dirname(os.path.abspath(__file__))
dir_of_interest = os.path.join(file_dir, "resources")
image_path= os.path.join(dir_of_interest, "image.jpg")
img = image.imread(image_path)
st.image(img)
