import streamlit as st
import pandas as pd
import numpy as np
from matplotlib import image
import os

st.title("Restaurant Rating Prediction")
st.write("Build an appropriate Machine Learning Model that will help various Restaurants to predict\
          their respective Ratings based on certain features,get insights about the type of cuisine\
         price range,important factors that determines Restaurant Ratings")

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

