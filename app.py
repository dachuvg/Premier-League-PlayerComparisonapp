import streamlit as st
from gk import get_gk_data,gkcompare,gkpizza
from att import get_att_data,attcompare,attpizza
from defence import get_def_data,defcompare,defpizza
import pandas as pd

gk_df = pd.read_csv("gk_data.csv")
def_df = pd.read_csv("def_data.csv")
att_df = pd.read_csv("att_data.csv")

col1, col2 = st.columns([2, 2])

with col2:
    st.title('Premier League Player Stats Comparison 2024/25')


with col1:
    st.image('logos/pl.png', use_container_width='auto') 
st.subheader('A comparison of Premier League players across various performance metrics')

if 'placeholders_shown' not in st.session_state:
    st.session_state.placeholders_shown = False

s1=st.selectbox("What kind of stats do you want to compare?",options=['Select any one','Goalkeeping','Defending','Attacking'])

if s1=='Select any one':
    st.text("Pick one please!!")
elif s1=='Goalkeeping':
    col1,col2=st.columns(2)
        
    with col1:
        player1=st.selectbox("Pick a player",options=gk_df['Player'].values)
        st.write(f"Age: {gk_df.loc[gk_df['Player'] == player1, 'Age'].values[0]}")
        st.write(f"Club: {gk_df.loc[gk_df['Player'] == player1, 'Squad'].values[0]}")
        st.write(f"Nationality: {gk_df.loc[gk_df['Player'] == player1, 'Nation'].values[0]}")
        st.write(f"Minutes Played: {gk_df.loc[gk_df['Player'] == player1, '90s'].values[0]*90}")
    with col2:    
        player2=st.selectbox("Pick another player",options=gk_df['Player'].values)
        st.write(f"Age: {gk_df.loc[gk_df['Player'] == player2, 'Age'].values[0]}")
        st.write(f"Club: {gk_df.loc[gk_df['Player'] == player2, 'Squad'].values[0]}")
        st.write(f"Nationality: {gk_df.loc[gk_df['Player'] == player2, 'Nation'].values[0]}")
        st.write(f"Minutes Played: {gk_df.loc[gk_df['Player'] == player2, '90s'].values[0]*90}")
            
        
    fig = gkcompare(gk_df, player1, player2)
    st.pyplot(fig)
    st.write(" ")
    st.write(" ")    
    fig = gkpizza(gk_df, player1, player2)
    st.pyplot(fig)
        
elif s1 == 'Defending':
    col1,col2=st.columns(2)
        
    with col1:
            player1=st.selectbox("Pick a player",options=def_df['Player'].values,key="player1")
            st.write(f"Age: {def_df.loc[def_df['Player'] == player1, 'Age'].values[0]}")
            st.write(f"Club: {def_df.loc[def_df['Player'] == player1, 'Squad'].values[0]}")
            st.write(f"Nationality: {def_df.loc[def_df['Player'] == player1, 'Nation'].values[0]}")
            st.write(f"Minutes Played: {gk_df.loc[gk_df['Player'] == player1, '90s'].values[0]*90}")
    with col2:    
            player2=st.selectbox("Pick a player",options=def_df['Player'].values,key="player2")
            st.write(f"Age: {def_df.loc[def_df['Player'] == player2, 'Age'].values[0]}")
            st.write(f"Club: {def_df.loc[def_df['Player'] == player2, 'Squad'].values[0]}")
            st.write(f"Nationality: {def_df.loc[def_df['Player'] == player2, 'Nation'].values[0]}")
            st.write(f"Minutes Played: {gk_df.loc[gk_df['Player'] == player1, '90s'].values[0]*90}")
            
        
    fig = defcompare(def_df, player1, player2)
    st.pyplot(fig)
    st.write(" ")
    st.write(" ")    
    fig = defpizza(def_df, player1, player2)
    st.pyplot(fig)
        
else:
    col1,col2=st.columns(2)
    with col1:
            player1 = st.selectbox("Pick a player", options=att_df['Player'].values,key="player1")
            st.write(f"Age: {att_df.loc[att_df['Player'] == player1, 'Age'].values[0]}")
            st.write(f"Club: {att_df.loc[att_df['Player'] == player1, 'Squad'].values[0]}")
            st.write(f"Nationality: {att_df.loc[att_df['Player'] == player1, 'Nation'].values[0]}")
            st.write(f"Minutes Played: {gk_df.loc[gk_df['Player'] == player1, '90s'].values[0]*90}")

    with col2:
            player2 = st.selectbox("Pick a player", options=att_df['Player'].values,key="player2")
            st.write(f"Age: {att_df.loc[att_df['Player'] == player2, 'Age'].values[0]}")
            st.write(f"Club: {att_df.loc[att_df['Player'] == player2, 'Squad'].values[0]}")
            st.write(f"Nationality: {att_df.loc[att_df['Player'] == player2, 'Nation'].values[0]}")
            st.write(f"Minutes Played: {gk_df.loc[gk_df['Player'] == player1, '90s'].values[0]*90}")
            
    fig= attcompare(att_df,player1,player2)
    st.pyplot(fig)
    st.write(" ")
    st.write(" ")     
    fig = attpizza(att_df,player1,player2)
    st.pyplot(fig) 
    
     



    
      







