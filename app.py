import streamlit as st
from gk import get_gk_data,gkcompare,gkpizza
from att import get_att_data,attcompare,attpizza
from defence import get_def_data,defcompare,defpizza

placeholder = st.empty()
try:
    with st.spinner(''):
        placeholder.markdown(
                """
                <style>
                        .highlight1 {
                            font-weight: bold;
                            font-size: 18px;
                            color: #D9534F; /* Highlighted color, you can change this */
                        }
                        
                        .endnote {
                            font-weight: bold;
                            font-size: 20px;
                        }
                        
                        .highlight2 {
                            font-weight: bold;
                            font-size: 18px;
                            color: aqua; 
                        }
                </style>
                <h1>Premier League Player Stats Comparison 2024/25</h1>
                <p class="highlight1">Did you know?</p>
                <p>Alan Shearer scored and missed the most penalties in the Premier League. 
                The all-time highest goalscorer scored 56 and missed 11, bringing his conversion rate to 83.58%.</p>
                <br>
                <p class="highlight2">Did you know?</p> 
                Players cannot be called offside if they receive the ball directly from a throw-in. It’s a rare and strategic loophole used by some teams.</p>
                <br>
                <p class="endnote">Your data is dribbling past defenders… closing in on goal!</p>
                """, 
                unsafe_allow_html=True
            )
        gk_df = get_gk_data()
    
    placeholder.empty()
    
    with st.spinner(''):
        placeholder.markdown(
                """
                
                <style>
                .highlight1 {
                    font-weight: bold;
                    font-size: 18px;
                    color: #D9534F; /* Highlighted color, you can change this */
                }
                
                .endnote {
                    font-weight: bold;
                    font-size: 20px;
                }
                
                .highlight2 {
                    font-weight: bold;
                    font-size: 18px;
                    color: aqua; 
                }
                </style>
                <h1>Premier League Player Stats Comparison 2024/25</h1>
                <p class = "highlight1">Did you know? </p>
                <p>Shane Long set the Premier League record for the fastest goal on April 23, 2019, scoring just 7.69 seconds into Southampton’s match against Watford by intercepting a misplaced clearance by defender Craig Cathcart and calmly chipping the ball over goalkeeper Ben Foster. This incredible moment broke the previous record of 9.82 seconds held by Ledley King since 2000.</p>
                <br>
                <p class = "highlight2">Did you know?</p>
                <p> Arsenal went an entire Premier League season unbeaten in 2003-2004, finishing with 26 wins and 12 draws. They became the first team in English football history to go a whole league season unbeaten, earning the nickname "The Invincibles".</p>
                <br>
                <p class="endnote">Your results are in the final third… preparing to score!</p>
                """, 
                unsafe_allow_html=True
                )              
        att_df = get_att_data()
    
    placeholder.empty()
    
    
    with st.spinner(''):
        placeholder.markdown(
        """
        <style>
            .highlight {
                font-weight: bold;
                font-size: 18px;
                color: #D9534F; /* Highlighted color, you can change this */
            }
            
            .endnote {
                font-weight: bold;
                font-size: 20px;
            }
        </style>
        <h1>Premier League Player Stats Comparison 2024/25</h1>
        <p class="highlight">Did you know?</p>
        <p>The fastest goal scored by a goalkeeper was by Asmir Begović, who scored from his own penalty area against Stoke City in a Premier League match in 2013, with the ball traveling 91.9 meters.</p>
        <br>
        <p class="endnote">Checking for offside… just a few more seconds!</p>
        """,
        unsafe_allow_html=True
        ) 
        
        
        def_df = get_def_data()
        
    placeholder.empty()
    col1, col2 = st.columns([2, 2])

    with col2:
        st.title('Premier League Player Stats Comparison 2024/25')


    with col1:
        st.image('logos/pl.png', use_column_width='auto') 
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
            st.write(f"90s: {gk_df.loc[gk_df['Player'] == player1, '90s'].values[0]}")
        with col2:    
            player2=st.selectbox("Pick another player",options=gk_df['Player'].values)
            st.write(f"Age: {gk_df.loc[gk_df['Player'] == player2, 'Age'].values[0]}")
            st.write(f"Club: {gk_df.loc[gk_df['Player'] == player2, 'Squad'].values[0]}")
            st.write(f"Nationality: {gk_df.loc[gk_df['Player'] == player2, 'Nation'].values[0]}")
            st.write(f"90s: {gk_df.loc[gk_df['Player'] == player2, '90s'].values[0]}")
            
        
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
            st.write(f"90s: {def_df.loc[def_df['Player'] == player1, '90s'].values[0]}")
        with col2:    
            player2=st.selectbox("Pick a player",options=def_df['Player'].values,key="player2")
            st.write(f"Age: {def_df.loc[def_df['Player'] == player2, 'Age'].values[0]}")
            st.write(f"Club: {def_df.loc[def_df['Player'] == player2, 'Squad'].values[0]}")
            st.write(f"Nationality: {def_df.loc[def_df['Player'] == player2, 'Nation'].values[0]}")
            st.write(f"90s: {def_df.loc[def_df['Player'] == player2, '90s'].values[0]}")
            
        
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
            st.write(f"90s: {att_df.loc[att_df['Player'] == player1, '90s'].values[0]}")

        with col2:
            player2 = st.selectbox("Pick a player", options=att_df['Player'].values,key="player2")
            st.write(f"Age: {att_df.loc[att_df['Player'] == player2, 'Age'].values[0]}")
            st.write(f"Club: {att_df.loc[att_df['Player'] == player2, 'Squad'].values[0]}")
            st.write(f"Nationality: {att_df.loc[att_df['Player'] == player2, 'Nation'].values[0]}")
            st.write(f"90s: {att_df.loc[att_df['Player'] == player2, '90s'].values[0]}")
            
        fig= attcompare(att_df,player1,player2)
        st.pyplot(fig)
        st.write(" ")
        st.write(" ")     
        fig = attpizza(att_df,player1,player2)
        st.pyplot(fig) 
    
except ValueError:
    st.error("Please reload and try again.")        



    
      







