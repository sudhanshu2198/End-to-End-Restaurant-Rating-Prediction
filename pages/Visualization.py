import streamlit as st 
import pandas as pd
import numpy as np
import os
from matplotlib import image
import plotly.express as px

file_dir=os.path.dirname(os.path.abspath(__file__))
parent_dir=os.path.join(file_dir,os.pardir)
dir_of_interest=os.path.join(parent_dir,"resources")
data_path=os.path.join(dir_of_interest,"display.csv")
data=pd.read_csv(data_path)

col=['Afghani', 'African', 'American', 'Andhra', 'Arabian', 'Asian',
       'Assamese', 'Awadhi', 'BBQ', 'Bakery', 'Belgian', 'Bengali',
       'Beverages', 'Bihari', 'Bohri', 'British', 'Burmese', 'Cantonese',
       'Chettinad', 'Chinese', 'Continental', 'Desserts', 'European',
       'Fast Food', 'French', 'German', 'Goan', 'Greek', 'Gujarati',
       'Healthy Food', 'Hyderabadi', 'Indonesian', 'Iranian', 'Italian',
       'Japanese', 'Jewish', 'Kashmiri', 'Kerala', 'Konkan', 'Korean',
       'Lebanese', 'Lucknowi', 'Maharashtrian', 'Malaysian',
       'Mangalorean', 'Mediterranean', 'Mexican', 'Middle Eastern',
       'Modern Indian', 'Mughlai', 'Naga', 'Nepalese', 'North Eastern',
       'North Indian', 'Oriya', 'Parsi', 'Portuguese', 'Rajasthani',
       'Russian', 'Seafood', 'Sindhi', 'Singaporean', 'South American',
       'South Indian', 'Spanish', 'Sri Lankan', 'Tamil', 'Thai',
       'Tibetan', 'Turkish', 'Vegan', 'Vietnamese']

#Choose City
st.subheader('City Restaurant Analysis')
City=st.selectbox("City",('Banashankari', 'Bannerghatta Road', 'Basavanagudi', 'Bellandur',
                          'Brigade Road', 'Brookefield', 'BTM', 'Church Street',
                          'Electronic City', 'Frazer Town', 'HSR', 'Indiranagar',
                          'Jayanagar', 'JP Nagar', 'Kalyan Nagar', 'Kammanahalli',
                          'Koramangala 4th Block', 'Koramangala 5th Block',
                          'Koramangala 6th Block', 'Koramangala 7th Block', 'Lavelle Road',
                          'Malleshwaram', 'Marathahalli', 'MG Road', 'New BEL Road',
                          'Old Airport Road', 'Rajajinagar', 'Residency Road',
                          'Sarjapur Road', 'Whitefield'))
df=data[data["City"]==City]

#Distribution graph of feature variable
st.subheader('Distribution graph of feature variable')
col1,col2=st.columns(2,gap="medium")
with col1:
    var=st.selectbox("Pie Chart",("Delivery","Booking","Category","Price_Category"))
    inter=df[var].value_counts()
    fig = px.pie(values=inter.values, names=inter.index)
    st.plotly_chart(fig,use_container_width=True)
with col2:
    var=st.selectbox("Histogram",( 'No_of_Varieties','Cost_Per_Person', 'Rating','Category','Price_Category'))
    fig = px.histogram(df, x=var)
    st.plotly_chart(fig,use_container_width=True)

#dataframe of count of restaurant type and popular cuisine among them.
st.subheader('Numbers of different restaurant type, with most popular cuisine among them')
inter=df.groupby(["Type"])[col].sum()
dicton={}

for i in range(len(inter)):
    index=inter.columns
    val=inter.iloc[i].values.T.flatten()
    series=pd.Series(val,index)
    vall=list(series.sort_values(ascending=False).head().index)
    dicton[inter.index[i]]=vall
    
frame=pd.DataFrame(dicton,index=['1st','2nd','3rd','4th','5th'])
frame=frame.T

inter=df.groupby("Type")["Type"].count().sort_values(ascending=False)
sol=pd.merge(left=inter,right=frame.loc[inter.index,:],on=inter.index)
sol.rename(columns={"key_0":"Restauant Type","Type":"Numbers"},inplace=True)
st.write(sol)

#Barplot showing numbers of restaurant with top five famous cuisine

cols=df["Type"].unique()
idf=pd.DataFrame()
inter=df.groupby("Type")[col].sum().T

for i in cols:
    ser=inter[i].sort_values(ascending=False).head()
    df_inter=pd.DataFrame(ser)
    df_inter.reset_index(inplace=True)
    df_inter.rename(columns={i:"Count","index":"Cuisine"},inplace=True)
    df_inter["Type"]=i
    idf=pd.concat([idf,df_inter],axis=0)
    
fig = px.bar(idf,x="Type",y="Count",color="Cuisine")
st.plotly_chart(fig)

#Plot showing the no of varieties served at restaurants
st.subheader('Plot showing relationship between no of varieties and no of best sellers')

inter=df.groupby(['No_of_Best_Sellers', 'No_of_Varieties'])[["Menu"]].count()
inter.rename(columns={"Menu":"Count"},inplace=True)
inter.reset_index(inplace=True)
fig = px.bar(inter,x="No_of_Varieties",y="Count",color="No_of_Best_Sellers",barmode="group")
st.plotly_chart(fig)

#boxplot showing price for different type,further categorized by their rating
st.subheader("Plot showing relationship between price and rating for different Restaurant type")
fig=px.box(df,x="Type",y="Cost_Per_Person",color="Category")
st.plotly_chart(fig)

#Most Popular Cuisine Varieties in City's Restaurant

st.subheader("Most Popular Cuisine Varieties in City's Restaurant")
inter=df.groupby(["City"])[col].sum()
index=inter.columns
val=inter.values.T.flatten()
series=pd.Series(val,index)
idf=series.sort_values(ascending=False).head()
fig = px.bar(idf,x=idf.index,y=idf.values)
st.plotly_chart(fig)

#Most Popular Cuisine Varieties in City's Restaurant Types

type=st.selectbox("Restaurant Type",df["Type"].unique())

col1,col2=st.columns([2,1],gap="medium")
with col1:
    inter=df.groupby(["Type"])[col].sum()
    inter=inter.T
    inter=inter[type]
    idf=inter.sort_values(ascending=False).head()
    fig = px.bar(idf,y=idf.index,x=idf.values)
    st.plotly_chart(fig,use_container_width=True)
with col2:
    inter=df[df['Type']==type]
    ser=inter.groupby('Name')[['Rating']].max()
    sol=ser.sort_values(by='Rating',ascending=False).head(10)
    st.write(sol,use_container_width=True)
   
#Plot showcasing price and quality of top most famous cuisine in City
st.subheader("Plot showcasing price and quality analysis of top most famous cuisine in City")
inter=df.groupby(["City"])[col].sum()
index=inter.columns
val=inter.values.T.flatten()
series=pd.Series(val,index)
sel=series.sort_values(ascending=False).head().index

##1
idf=pd.DataFrame()

for i in sel:
    inter=df[df[i]==1]
    inter=inter.groupby(["Price_Category"])[["Menu"]].count()
    inter=inter.reset_index()
    inter.rename(columns={"Menu":"Count"},inplace=True)
    inter["Cuisine_Type"]=i
    idf=pd.concat([idf,inter],axis=0)


fig = px.bar(x=idf["Cuisine_Type"], y=idf["Count"], color=idf["Price_Category"],barmode="group")
st.plotly_chart(fig)

##2
idf=pd.DataFrame()

for i in sel:
    inter=df[df[i]==1]
    inter=inter.groupby(["Category"])[["Menu"]].count()
    inter=inter.reset_index()
    inter.rename(columns={"Menu":"Count"},inplace=True)
    inter["Cuisine_Type"]=i
    idf=pd.concat([idf,inter],axis=0)


fig = px.bar(x=idf["Cuisine_Type"], y=idf["Count"], color=idf["Category"],barmode="group")
st.plotly_chart(fig)

#Plot comparing pricing and quality of Cuisine, plus displaying best rated restaurant
st.subheader("Best Restaurant for a Cuisine Type")
Cuisine=st.selectbox("Cuisine",col,index=53)

col1,col2=st.columns([2,1],gap="medium")
with col1:
    inter=df[(df[Cuisine]==1)]
    inter=inter.groupby(["Price_Category","Category"])[["Menu"]].count()
    inter=inter.reset_index()
    inter.rename(columns={"Menu":"Count"},inplace=True)
    fig = px.bar(inter,x="Price_Category", y="Count", color="Category",barmode="group")
    st.plotly_chart(fig,use_container_width=True)
with col2:
    inter=df[df[Cuisine]==1]
    ser=inter.groupby('Name')[['Rating']].max()
    sol=ser.sort_values(by='Rating',ascending=False).head(10)
    st.write(sol,use_container_width=True)
