import numpy as np
from selenium import webdriver
from bs4 import BeautifulSoup
from mplsoccer import Radar, FontManager, grid, PyPizza,add_image
import matplotlib.pyplot as plt
from mplsoccer import Radar, FontManager, grid
from selenium.webdriver.chrome.service import Service
from scipy import stats
import math
import streamlit as st
from selenium.webdriver.chrome.options import Options

    
@st.cache_data 
def get_att_data():
    from selenium.webdriver.chrome.options import Options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run browser in headless mode
    chrome_options.add_argument("--disable-gpu")  # Disable GPU for headless
    chrome_options.add_argument("--no-sandbox")  # For compatibility
    chrome_options.add_argument("--disable-dev-shm-usage")  # To prevent resource issues
    service=Service()
    
    driver = webdriver.Chrome(service=service,options=chrome_options)
    driver.get("https://fbref.com/en/comps/9/stats/Premier-League-Stats")

    # Get the page source
    html = driver.page_source

    # Parse with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Find the table
    table = soup.find('table', {'id': 'stats_standard'})

    # Convert to DataFrame
    df = pd.read_html(str(table))[0]


    driver.quit()
    
    att_df = df.copy()
    
    att_df = att_df.loc[:, att_df.columns.get_level_values(0) != 'Performance']
    att_df = att_df.loc[:, att_df.columns.get_level_values(0) != 'Expected'] 
    
    att_df.columns = [att_df.columns[i][1]  for i in range(len(att_df.columns))]
    
    att_df = att_df[att_df['Player'] != 'Player']
    att_df['Nation'] = att_df['Nation'].str.split().str[1]
    att_df['Age'] = att_df['Age'].str.split("-").str[0]
    
    driver = webdriver.Chrome(service=service,options=chrome_options)
    driver.get("https://fbref.com/en/comps/9/passing/Premier-League-Stats")

    # Get the page source
    html = driver.page_source

    # Parse with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Find the table
    table = soup.find('table', {'id': 'stats_passing'})

    # Convert to DataFrame
    pass_df = pd.read_html(str(table))[0]


    driver.quit()
    
    pass_df = pass_df.loc[:, pass_df.columns.get_level_values(0) != 'Total']
    pass_df = pass_df.loc[:, pass_df.columns.get_level_values(0) != 'Short']
    pass_df = pass_df.loc[:, pass_df.columns.get_level_values(0) != 'Medium']
    pass_df = pass_df.loc[:, pass_df.columns.get_level_values(0) != 'Long']
    pass_df = pass_df.loc[:, pass_df.columns.get_level_values(0) != 'Unnamed: 23_level_0']
    pass_df = pass_df.loc[:, pass_df.columns.get_level_values(0) != 'Expected']
    
    pass_df.columns = [pass_df.columns[i][1]  for i in range(len(pass_df.columns))]
    pass_df = pass_df[pass_df['Player'] != 'Player']
    pass_df['Nation'] = pass_df['Nation'].str.split().str[1]
    pass_df['Age'] = pass_df['Age'].str.split("-").str[0]
    
    pass_df['KP'] = pd.to_numeric(pass_df['KP'], errors='coerce')
    pass_df['CrsPA'] = pd.to_numeric(pass_df['CrsPA'], errors='coerce')
    pass_df['90s'] = pd.to_numeric(pass_df['90s'], errors='coerce')
    pass_df['Key_Passes'] = np.where(pass_df['90s'] != 0, pass_df['KP'] / pass_df['90s'], 0)
    pass_df['Crosses_Completed'] = np.where(pass_df['90s'] != 0, pass_df['CrsPA'] / pass_df['90s'], 0)
    
    pass_df = pass_df.drop(['Player','Nation','Pos','Squad','Age','Born','90s','Ast','KP','1/3','PPA','CrsPA','PrgP','Matches'],axis=1)
    
    stats_df = pd.merge(att_df, pass_df, on='Rk', how='inner')
    
    from selenium import webdriver
    from bs4 import BeautifulSoup
    import pandas as pd
    from selenium.webdriver.chrome.options import Options

    # Set up Selenium
    driver = webdriver.Chrome(service=service,options=chrome_options)
    driver.get("https://fbref.com/en/comps/9/passing_types/Premier-League-Stats")

    # Get the page source
    html = driver.page_source

    # Parse with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Find the table
    table = soup.find('table', {'id': 'stats_passing_types'})

    # Convert to DataFrame
    df = pd.read_html(str(table))[0]


    driver.quit()
    
    type_df = df.copy()
    
    type_df = type_df.loc[:, type_df.columns.get_level_values(0) != 'Corner Kicks']
    type_df = type_df.loc[:, type_df.columns.get_level_values(0) != 'Outcomes']
    type_df = type_df.loc[:, type_df.columns.get_level_values(0) != 'Unnamed: 23_level_0']

    type_df.columns = [type_df.columns[i][1]  for i in range(len(type_df.columns))]
    type_df = type_df[type_df['Player'] != 'Player']
    type_df['Nation'] = type_df['Nation'].str.split().str[1]
    type_df['Age'] = type_df['Age'].str.split("-").str[0]
    
    type_df['TB'] = pd.to_numeric(type_df['TB'], errors='coerce')
    type_df['90s'] = pd.to_numeric(type_df['90s'], errors='coerce')
    type_df['Through_Balls'] = np.where(type_df['90s'] != 0, type_df['TB'] / type_df['90s'], 0)    
    
    type_df = type_df.drop(['Player','Nation','Pos','Squad','Age','Born','90s','Att','Live','Dead','FK','TB','Sw','Crs','TI','CK'],axis=1)
    
    stats_df = pd.merge(stats_df, type_df, on='Rk', how='inner')
    

    # Set up Selenium
    driver = webdriver.Chrome(service=service,options=chrome_options)
    driver.get("https://fbref.com/en/comps/9/gca/Premier-League-Stats")

    # Get the page source
    html = driver.page_source

    # Parse with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Find the table
    table = soup.find('table', {'id': 'stats_gca'})

    # Convert to DataFrame
    df = pd.read_html(str(table))[0]


    driver.quit()
    
    gca_df = df.copy()
    
    gca_df = gca_df.loc[:, gca_df.columns.get_level_values(0) != 'SCA Types']
    gca_df = gca_df.loc[:, gca_df.columns.get_level_values(0) != 'GCA Types']


    gca_df.columns = [gca_df.columns[i][1]  for i in range(len(gca_df.columns))] 
    
    gca_df = gca_df[gca_df['Player'] != 'Player']
    gca_df['Nation'] = gca_df['Nation'].str.split().str[1]
    gca_df['Age'] = gca_df['Age'].str.split("-").str[0]
    
    gca_df = gca_df.drop(['Player','Nation','Pos','Squad','Age','Born','90s','SCA','GCA','Matches'],axis=1)
    
    stats_df = pd.merge(stats_df, gca_df, on='Rk', how='inner')
    
    driver = webdriver.Chrome(service=service,options=chrome_options)
    driver.get("https://fbref.com/en/comps/9/possession/Premier-League-Stats")

    # Get the page source
    html = driver.page_source

    # Parse with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Find the table
    table = soup.find('table', {'id': 'stats_possession'})

    # Convert to DataFrame
    df = pd.read_html(str(table))[0]


    driver.quit()   

    poss_df = df.copy()
    
    poss_df = poss_df.loc[:, poss_df.columns.get_level_values(0) != 'Carries']
    poss_df = poss_df.loc[:, poss_df.columns.get_level_values(0) != 'Receiving']


    poss_df.columns = [poss_df.columns[i][1]  for i in range(len(poss_df.columns))]
    poss_df = poss_df[poss_df['Player'] != 'Player']
    poss_df['Nation'] = poss_df['Nation'].str.split().str[1]
    poss_df['Age'] = poss_df['Age'].str.split("-").str[0]    

    poss_df['Succ%']=poss_df['Succ%'].fillna(0.0)
    
    poss_df = poss_df.drop(['Player','Nation','Pos','Squad','Age','Born','90s','Touches', 'Def Pen', 'Def 3rd', 'Mid 3rd', 'Att 3rd','Matches','Live', 'Att', 'Succ', 'Tkld', 'Tkld%'],axis=1)
    poss_df.rename(columns={'Att Pen': 'Touches_in_Box', 'Succ%': 'Succ Dribbles%'}, inplace=True)
    stats_df = pd.merge(stats_df, poss_df, on='Rk', how='inner')
    stats_df=stats_df.drop(['Born','Starts','Matches','Min','PrgR','G+A','Gls','G+A-PK','xG+xAG','npxG+xAG','xG'],axis=1)
    stats_df.rename(columns={'G-PK': 'NPG'}, inplace=True)
    
    stats_df['90s'] = pd.to_numeric(stats_df['90s'], errors='coerce')
    stats_df['PrgC'] = pd.to_numeric(stats_df['PrgC'], errors='coerce')
    stats_df['PrgP'] = pd.to_numeric(stats_df['PrgP'], errors='coerce')
    stats_df['Ast'] = pd.to_numeric(stats_df['Ast'], errors='coerce')
    stats_df['NPG'] = pd.to_numeric(stats_df['NPG'], errors='coerce')
    stats_df['xAG'] = pd.to_numeric(stats_df['xAG'], errors='coerce')
    stats_df['npxG'] = pd.to_numeric(stats_df['npxG'], errors='coerce')
    stats_df['Key_Passes'] = pd.to_numeric(stats_df['Key_Passes'], errors='coerce')
    stats_df['Crosses_Completed'] = pd.to_numeric(stats_df['Crosses_Completed'], errors='coerce')
    stats_df['Through_Balls'] = pd.to_numeric(stats_df['Through_Balls'], errors='coerce')
    stats_df['SCA90'] = pd.to_numeric(stats_df['SCA90'], errors='coerce')
    stats_df['GCA90'] = pd.to_numeric(stats_df['GCA90'], errors='coerce')
    stats_df['Touches_in_Box'] = pd.to_numeric(stats_df['Touches_in_Box'], errors='coerce')
    stats_df['Succ Dribbles%'] = pd.to_numeric(stats_df['Succ Dribbles%'], errors='coerce')
    
    int_columns = stats_df.select_dtypes(include='int').columns
    stats_df[int_columns] = stats_df[int_columns].astype(float)
    
    return stats_df


def attcompare(df,player1,player2):
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
    
    params = [ 'PrgC',
       'PrgP', 'Ast', 'NPG', 'xAG', 'npxG', 'Key_Passes', 'Crosses_Completed',
       'Through_Balls', 'SCA90', 'GCA90', 'Touches_in_Box', 'Succ Dribbles%']

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
    lower_is_better = ['Errors']
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

    

    
    # adding the endnote and title text (these axes range from 0-1, i.e. 0, 0 is the bottom left)
    # Note we are slightly offsetting the text from the edges by 0.01 (1%, e.g. 0.99)
    endnote_text = axs['endnote'].text(0.99, 0.5, 'Reference: MPL Soccer/Statsbomb', fontsize=15,
                                       color='#fcfcfc',fontproperties=robotto_thin.prop, ha='right', va='center')
    endnote_text = axs['endnote'].text(0.99, 0.5, 'Reference: MPL Soccer/Statsbomb', fontsize=15,
                                       color='#fcfcfc', fontproperties=robotto_thin.prop, ha='right', va='center')
    endnote_text2 = axs['endnote'].text(0.2, 0.5, 'GCA - Goal Creating Actions per 90', fontsize=15,
                                        color='#fcfcfc', fontproperties=robotto_thin.prop, ha='right', va='center')
    endnote_text3 = axs['endnote'].text(0.2, 1, 'SCA - Shot Creating Actions per 90', fontsize=15,
                                        color='#fcfcfc', fontproperties=robotto_thin.prop, ha='right', va='center')
    endnote_text4 = axs['endnote'].text(0.2,1.5, 'NPG - Non Penalty Goals', fontsize=15,
                                        color='#fcfcfc', fontproperties=robotto_thin.prop, ha='right', va='center')
    endnote_text5 = axs['endnote'].text(0.2, 2, 'NPxG - Non Penalty Expected Goals', fontsize=15,
                                        color='#fcfcfc', fontproperties=robotto_thin.prop, ha='right', va='center')
    endnote_text6 = axs['endnote'].text(0.2, 2.5, 'PrgC and PrgP - Progressive Carries and Passes', fontsize=15,
                                        color='#fcfcfc', fontproperties=robotto_thin.prop, ha='right', va='center')

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

def attpizza(df,player1,player2):
    
    params = [ 'PrgC',
           'PrgP', 'Ast', 'NPG', 'xAG', 'npxG', 'Key_Passes', 'Crosses_Completed',
           'Through_Balls', 'SCA90', 'GCA90', 'Touches_in_Box', 'Succ Dribbles%']
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
    
        # # Invert percentile if needed 
        # if params[i] in ['Errors']:  
        #     rank1 = 100 - rank1
        #     rank2 = 100 - rank2
    
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
