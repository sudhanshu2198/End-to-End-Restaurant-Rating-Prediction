import streamlit as st
import pandas as pd
import numpy as np
import joblib
from matplotlib import image
import lightgbm
import os

st.title("Restaurant Rating Prediction")

file_dir=os.path.dirname(os.path.abspath(__file__))
parent_dir=os.path.join(file_dir,os.pardir)
dir_of_interest=os.path.join(parent_dir,"artifacts")

model_path=os.path.join(dir_of_interest,"model.pkl")
encoder_path=os.path.join(dir_of_interest,"encoder.pkl")
mlb_path=os.path.join(dir_of_interest,"mlb.pkl")

model = joblib.load(open(model_path, 'rb'))
encoder = joblib.load(open(encoder_path, 'rb'))
mlb = joblib.load(open(mlb_path, 'rb'))

with st.form('user_inputs'):
    City=st.selectbox("City",('Banashankari', 'Bannerghatta Road', 'Basavanagudi', 'Bellandur',
                              'Brigade Road', 'Brookefield', 'BTM', 'Church Street',
                              'Electronic City', 'Frazer Town', 'HSR', 'Indiranagar',
                              'Jayanagar', 'JP Nagar', 'Kalyan Nagar', 'Kammanahalli',
                              'Koramangala 4th Block', 'Koramangala 5th Block',
                              'Koramangala 6th Block', 'Koramangala 7th Block', 'Lavelle Road',
                              'Malleshwaram', 'Marathahalli', 'MG Road', 'New BEL Road',
                              'Old Airport Road', 'Rajajinagar', 'Residency Road',
                              'Sarjapur Road', 'Whitefield'))
    Cuisines=st.multiselect("Cuisines",('Afghani','African','American','Andhra','Arabian','Asian',
                                        'Assamese','Awadhi','BBQ','Bakery','Belgian','Bengali','Beverages',
                                        'Bihari','Biryani','Bohri','British','Burmese','Cantonese','Chettinad',
                                        'Chinese','Continental','Desserts','European','Fast Food','French','German',
                                        'Goan','Greek','Gujarati','Healthy Food','Hyderabadi','Indonesian','Iranian',
                                        'Italian','Japanese','Jewish','Kashmiri','Kebab','Kerala','Konkan','Korean',
                                        'Lebanese','Lucknowi','Maharashtrian','Malaysian','Mangalorean','Mediterranean',
                                        'Mexican','Middle Eastern','Modern Indian','Mughlai','Naga','Nepalese','North Eastern',
                                        'North Indian','Oriya','Parsi','Portuguese','Rajasthani','Russian','Seafood',
                                        'Sindhi','Singaporean','South American','South Indian','Spanish','Sri Lankan',
                                        'Tamil','Thai','Tibetan','Turkish','Vegan','Vietnamese'),
                                        default=['North Indian','South Indian','Italian'])
    Cost_Per_Person=st.slider("Cost_Per_Person", min_value=20.0, max_value=3000.0, value=100.0, step=10.0)
    No_of_Best_Sellers=st.slider("No_of_Best_Sellers", min_value=0, max_value=10, value=3, step=1)
    Delivery=st.radio("Online Ordering",(('Yes', 'No')))
    Booking=st.radio("Table Booking ",('Yes', 'No'))
    click=st.form_submit_button()

if click:
    

    df=pd.DataFrame([[Delivery,Booking,City]],columns=['Delivery', 'Booking', 'City'])
    one_hot_df=encoder.transform(df).toarray()

    No_of_Varieties=len(Cuisines)
    numeric=np.array([[No_of_Best_Sellers, No_of_Varieties, Cost_Per_Person]])

    df=pd.DataFrame([[Cuisines]],columns=['Cuisines'])
    mlb_df=mlb.transform(df)

    data=np.concatenate([numeric,mlb_df,one_hot_df],axis=1)
    rating=model.predict(data)

    if rating>=4:
        st.success(f"Restaurant Rating is: {round(rating[0],1)}")
    elif rating>=3.5:
        st.warning(f"Restaurant Rating is: {round(rating[0],1)}")
    else:
        st.error(f"Restaurant Rating is: {round(rating[0],1)}")
