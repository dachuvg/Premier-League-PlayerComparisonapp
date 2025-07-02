import pandas as pd
import numpy as np
from selenium import webdriver
from bs4 import BeautifulSoup
from mplsoccer import Radar, FontManager, grid, PyPizza,add_image
import matplotlib.pyplot as plt
from mplsoccer import Radar, FontManager, grid
from selenium.webdriver.chrome.options import Options
from scipy import stats
import math
import streamlit as st
from selenium.webdriver.chrome.service import Service

@st.cache_data 
def get_gk_data():
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    # Scrape stats_keeper data
    chrome_options = Options()
    
    chrome_options.add_argument("--headless")  # Run without opening a browser window
    chrome_options.add_argument("--no-sandbox")  # For compatibility on some environments
    chrome_options.add_argument("--disable-dev-shm-usage")  # To avoid resource issues
    chrome_options.add_argument("--disable-gpu")  # Disable GPU for headless
    chrome_options.add_argument("--remote-debugging-port=9222")  # Optional: enables debugging
    service = Service()

    driver = webdriver.Chrome(service=service,options=chrome_options)
    driver.get("https://fbref.com/en/comps/9/keepers/Premier-League-Stats")
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', {'id': 'stats_keeper'})
    df1 = pd.read_html(str(table))[0]
    # driver.quit()

    # Scrape stats_keeper_adv data
    # driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://fbref.com/en/comps/9/keepersadv/Premier-League-Stats")
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', {'id': 'stats_keeper_adv'})
    df2 = pd.read_html(str(table))[0]
    driver.quit()
    
    gk2_df=df2.copy()
    gk2_df = gk2_df.loc[:, gk2_df.columns.get_level_values(0) != 'Goal Kicks']
    gk2_df = gk2_df.loc[:, gk2_df.columns.get_level_values(0) != 'Passes']
    gk2_df = gk2_df.loc[:, gk2_df.columns.get_level_values(0) != 'Goals']
    
    gk2_df.columns = [gk2_df.columns[i][1]  for i in range(len(gk2_df.columns))]
    gk2_df=gk2_df.drop(['Player','Nation','Pos','Squad','Age','Born','90s','Matches'],axis=1)
    
    gk1_df=df1.copy()
    gk1_df.columns = [gk1_df.columns[i][1]  for i in range(len(gk1_df.columns))]
    gk1_df=gk1_df.fillna(0)
    
    gk_df = pd.merge(gk1_df, gk2_df, on='Rk', how='inner')
    
    gk_df['Nation'] = gk_df['Nation'].str.split().str[1]
    gk_df['Age'] = gk_df['Age'].str.split("-").str[0]
    gk_df = gk_df[gk_df['Player'] != 'Player']
    
    # drop born,mp,starts,min,save%,w,d,l,cs,pka,pkm,matches,psxgall,

    gk_df= gk_df.drop(['Born', 'MP', 'Starts','Min','Save%', 'W', 'D', 'L','CS','PKA','PKm','Matches', 'PSxG',
       'PSxG/SoT', 'PSxG+/-', '/90', 'Cmp', 'Att', 'Cmp%', 'Opp', 'Stp',
       'Stp%', '#OPA','AvgDist'],axis=1) 
    
    gk_df.rename(columns={'#OPA/90': 'OPA/90'}, inplace=True)
    
    gk_df['GA'] = pd.to_numeric(gk_df['GA'], errors='coerce')
    gk_df['GA90'] = pd.to_numeric(gk_df['GA90'], errors='coerce')
    gk_df['SoTA'] = pd.to_numeric(gk_df['SoTA'], errors='coerce')
    gk_df['Saves'] = pd.to_numeric(gk_df['Saves'], errors='coerce')
    gk_df['CS%'] = pd.to_numeric(gk_df['CS%'], errors='coerce')
    gk_df['PKatt'] = pd.to_numeric(gk_df['PKatt'], errors='coerce')
    gk_df['PKsv'] = pd.to_numeric(gk_df['PKsv'], errors='coerce')
    gk_df['OPA/90'] = pd.to_numeric(gk_df['OPA/90'], errors='coerce')
    gk_df['90s'] = pd.to_numeric(gk_df['90s'], errors='coerce')
    
    
    gk_df['Save%'] = (((gk_df['SoTA'] - gk_df['GA']) / gk_df['SoTA'])*100).round(2)
    gk_df['PKSave%'] = ((gk_df['PKsv']/gk_df['PKatt'])*100).round(2)
    gk_df['PKSave%']=gk_df['PKSave%'].fillna(0.0)
    
    return gk_df
    
       
def gkcompare(df,player1,player2):
    URL1 = ('https://raw.githubusercontent.com/googlefonts/SourceSerifProGFVersion/main/fonts/'
        'SourceSerifPro-Regular.ttf')
    serif_regular = FontManager(URL1)
    URL2 = ('https://raw.githubusercontent.com/googlefonts/SourceSerifProGFVersion/main/fonts/'
            'SourceSerifPro-ExtraLight.ttf')
    serif_extra_light = FontManager(URL2)
    URL3 = ('https://raw.githubusercontent.com/google/fonts/main/ofl/rubikmonoone/'
            'RubikMonoOne-Regular.ttf')
    rubik_regular = FontManager(URL3)
    URL4 = 'https://raw.githubusercontent.com/googlefonts/roboto/main/src/hinted/Roboto-Thin.ttf'
    robotto_thin = FontManager(URL4)
    URL5 = ('https://raw.githubusercontent.com/google/fonts/main/apache/robotoslab/'
            'RobotoSlab%5Bwght%5D.ttf')
    robotto_bold = FontManager(URL5)
    
    params = ['CS%','Save%','PKSave%','PKsv','GA90','OPA/90']
    

    low=[]
    high=[]
    player1_val=[]
    player2_val=[]
    
    for i in range(len(params)):
        player1_val.append(df.loc[df['Player'] == player1, params[i]].values[0])
        player2_val.append(df.loc[df['Player'] == player2, params[i]].values[0])
        l=min(player1_val[i],player2_val[i])
        if(l-(l*0.2) < 0):
            low.append(0)
        else:
            low.append(l-(l*0.2))

        h = max(player1_val[i],player2_val[i])   
        if h==0:
            high.append(100)
        else:    
            high.append(h+(h*0.2))
    # print(player1_val)
    # print(player2_val)
    # print(low)
    # print(high)
    lower_is_better = ['GA90']
    radar = Radar(params, low, high,
              lower_is_better=lower_is_better,
              # whether to round any of the labels to integers instead of decimal places
              round_int=[False]*len(params),
              num_rings=4,  # the number of concentric circles (excluding center circle)
              # if the ring_width is more than the center_circle_radius then
              # the center circle radius will be wider than the width of the concentric circles
              ring_width=1, center_circle_radius=1)
    
    fig, axs = grid(figheight=14, grid_height=0.915, title_height=0.06, endnote_height=0.025,
                title_space=0, endnote_space=0, grid_key='radar', axis=False)

    # plot radar
    # radar.setup_axis(ax=axs['radar'])  # format axis as a radar
    # rings_inner = radar.draw_circles(ax=axs['radar'], facecolor='#ffb2b2', edgecolor='#fc5f5f')
    radar.setup_axis(ax=axs['radar'], facecolor='None')
    rings_inner = radar.draw_circles(ax=axs['radar'], facecolor='#28252c', edgecolor='#39353f', lw=1.5)
    
    radar_output = radar.draw_radar_compare(player1_val, player2_val, ax=axs['radar'],
                                            kwargs_radar={'facecolor': '#d0667a', 'alpha': 0.6},
                                            kwargs_compare={'facecolor': '#1d537f', 'alpha': 0.6})
    radar_poly, radar_poly2, vertices1, vertices2 = radar_output
    # range_labels = radar.draw_range_labels(ax=axs['radar'], fontsize=25,
    #                                        fontproperties=robotto_thin.prop)
    # param_labels = radar.draw_param_labels(ax=axs['radar'], fontsize=25,
    #                                        fontproperties=robotto_thin.prop)
    range_labels = radar.draw_range_labels(ax=axs['radar'], fontsize=25, color='#fcfcfc',
                                       fontproperties=robotto_thin.prop)
    param_labels = radar.draw_param_labels(ax=axs['radar'], fontsize=25, color='#fcfcfc',
                                       fontproperties=robotto_thin.prop)
    axs['radar'].scatter(vertices1[:, 0], vertices1[:, 1],
                         c='#00f2c1', edgecolors='#6d6c6d', marker='o', s=150, zorder=2)
    axs['radar'].scatter(vertices2[:, 0], vertices2[:, 1],
                         c='#d80499', edgecolors='#6d6c6d', marker='o', s=150, zorder=2)

    endnote_text = axs['endnote'].text(0.99, 0.5, 'Reference: MPL Soccer/Statsbomb', fontsize=15,
                                       color='#fcfcfc',fontproperties=robotto_thin.prop, ha='right', va='center')
    endnote2_text = axs['endnote'].text(0.5, 0.5, '**OPA - Defensive actions outside penalty area(FBref)', fontsize=20,
                                       color='#fcfcfc',fontproperties=robotto_thin.prop, ha='right', va='center')
    title1_text = axs['title'].text(0.01, 0.65, player1, fontsize=25, color='#01c49d',
                                    fontproperties=robotto_bold.prop, ha='left', va='center')
    title2_text = axs['title'].text(0.01, 0.25,df.loc[df['Player'] == player1, 'Squad'].values[0], fontsize=20,
                                    fontproperties=robotto_thin.prop,
                                    ha='left', va='center', color='#01c49d')
    title3_text = axs['title'].text(0.99, 0.65, player2, fontsize=25,
                                    fontproperties=robotto_bold.prop,
                                    ha='right', va='center', color='#d80499')
    title4_text = axs['title'].text(0.99, 0.25,df.loc[df['Player'] == player2, 'Squad'].values[0], fontsize=20,
                                    fontproperties=robotto_thin.prop,
                                    ha='right', va='center', color='#d80499')

    fig.set_facecolor('#121212') 
    
    return fig 


def gkpizza(df,player1,player2):
    
    params = ['CS%','Save%','PKSave%','PKsv','GA90','OPA/90']
    df.fillna(0.0)
 
    values2= []
    values1 = []
    params_offset = []
    for i in range(len(params)):
        column = df[params[i]]
        player1_stat = df.loc[df['Player'] == player1, params[i]].values[0]
        player2_stat = df.loc[df['Player'] == player2, params[i]].values[0]
        # Compute percentile rank
        rank1 = stats.percentileofscore(column, player1_stat)
        rank2 = stats.percentileofscore(column, player2_stat)
    
        # Invert percentile if needed 
        if params[i] in ['GA90']:  
            rank1 = 100 - rank1
            rank2 = 100 - rank2
    
        values1.append(math.floor(rank1))
        values2.append(math.floor(rank2))
        diff = abs(rank1-rank2)
        params_offset.append(diff<10)

        
    
    

    baker = PyPizza(
        params=params,                  # list of parameters
        background_color="#0f0101",
        straight_line_color="#FCFCFC",  # color for straight lines
        straight_line_lw=1,             # linewidth for straight lines
        last_circle_lw=1,               # linewidth of last circle
        last_circle_color="#FCFCFC",
        other_circle_lw=1,              # linewidth for other circles
        other_circle_ls="-.",           # linestyle for other circles
        other_circle_color="#FCFCFC"
    )
    
    # plot pizza
    fig, ax = baker.make_pizza(
        values1,
        compare_values=values2, #list of values
        figsize=(8, 8),      # adjust figsize according to your need
        param_location=110,  # where the parameters will be added
        kwargs_slices=dict(
            facecolor="red", edgecolor="#FCFCFC",
            zorder=2, linewidth=1
        ),
        kwargs_compare=dict(
            facecolor="#00FFFF", edgecolor="#FCFCFC",
            zorder=2, linewidth=1
        ),
# values to be used when plotting slices
        kwargs_params=dict(
            color="#FCFCFC", fontsize=12,
             va="center"
        ),                   # values to be used when adding parameter
        kwargs_values=dict(
            color="white", fontsize=12,
            zorder=3,
            bbox=dict(
                edgecolor="#FCFCFC", facecolor="black",
                boxstyle="round,pad=0.2", lw=1
            )
        ),
        kwargs_compare_values=dict(
            color="black", fontsize=12, zorder=3,
            bbox=dict(edgecolor="#000000", facecolor="#00FFFF", boxstyle="round,pad=0.2", lw=1)
        ) # values to be used when adding parameter-values
    )

    baker.adjust_texts(params_offset, offset=-0.17, adj_comp_values=True)
    
    # add title
    # fig.text(
    #     0.515, 0.97, f"{player1} vs {player2}", size=18,
        
    #     ha="center", color="#000000"
    # ) 
    fig.text(
        0.495, 0.97,
        f"{player1} ", size=18, color="red", ha="right"
    )
    fig.text(
        0.515, 0.97,
        f"vs", size=18, color="#FCFCFC", ha="center"
    )
    fig.text(
        0.535, 0.97,
        f"{player2} ", size=18, color="#00FFFF", ha="left"
    )


    
    # add subtitle
    fig.text(
        0.515, 0.942,
        "Percentile Rank vs Premier League Players | Season 2024-25",
        size=15,
        ha="center", color="#FCFCFC"
    )
    
    # add credits
    CREDIT_1 = "credits : mplsoccer & fbref(data)"
    
    fig.text(
        0.99, 0.005, f"{CREDIT_1}", size=9,
        color="#FCFCFC",
        ha="right"
    )
    fig.set_facecolor('#121212') 
    return fig
