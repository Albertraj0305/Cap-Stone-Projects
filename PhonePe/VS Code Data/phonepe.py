import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd
import psycopg2
import json
import requests
from PIL import Image


# data frame Creation

# SQL Creation
mydb=psycopg2.connect(host='localhost',user='postgres',port='5432',database='PhonePe',password='Password@123')
cursor = mydb.cursor()


#Aggresgated Insurance Date Frame
cursor.execute("SELECT * FROM aggr_Insurance")
mydb.commit()
table1=cursor.fetchall()


aggr_Insurance=pd.DataFrame(table1,columns=("States","Years","Quarter","Transaction_Type","Transaction_Count","Transaction_Amount"))

#Aggresgated Transaction Date Frame
cursor.execute("SELECT * FROM aggregated_Transaction")
mydb.commit()
table2=cursor.fetchall()


aggregated_Transaction=pd.DataFrame(table2,columns=("States","Years","Quarter","Transaction_Type","Transaction_Count","Transaction_Amount"))

#Aggresgated Users Date Frame
cursor.execute("SELECT * FROM aggregated_User")
mydb.commit()
table3=cursor.fetchall()


aggregated_Users=pd.DataFrame(table3,columns=("States","Years","Quarter","Brands","Transaction_Count","Percentage"))


#map Transaction Date Frame
cursor.execute("SELECT * FROM map_Trans")
mydb.commit()
table4=cursor.fetchall()


map_Transaction=pd.DataFrame(table4,columns=("States","Years","Quarter","Districts","Transaction_Count","Transaction_Amount"))


#map users Date Frame
cursor.execute("SELECT * FROM map_Users")
mydb.commit()
table5=cursor.fetchall()


map_Users=pd.DataFrame(table5,columns=("States","Years","Quarter","Districts","Register_User","App_Open"))


#map Insurance Date Frame
cursor.execute("SELECT * FROM map_Insurance")
mydb.commit()
table6=cursor.fetchall()


map_Insurance=pd.DataFrame(table6,columns=("States","Years","Quarter","Districts","Transaction_Count","Transaction_Amount"))


#top Insurance Date Frame
cursor.execute("SELECT * FROM top_Insurance")
mydb.commit()
table7=cursor.fetchall()


top_Insurance=pd.DataFrame(table7,columns=("States","Years","Quarter","Pincodes","Transaction_Count","Transaction_Amount"))

#top Transaction Date Frame
cursor.execute("SELECT * FROM top_Transaction")
mydb.commit()
table8=cursor.fetchall()


top_Transaction=pd.DataFrame(table8,columns=("States","Years","Quarter","Pincodes","Transaction_Count","Transaction_Amount"))

#top user Date Frame
cursor.execute("SELECT * FROM top_user")
mydb.commit()
table9=cursor.fetchall()


top_users=pd.DataFrame(table9,columns=("States","Years","Quarter","Pincodes","Register_User"))
# Analysis Transaction Amount using Year
def transaction_amount_count_Y(df,year):

    trans_amounta_count_Year=df[df["Years"]==year]
    trans_amounta_count_Year.reset_index(drop=True, inplace=True)

    trans_amounta_count_Year_Group=trans_amounta_count_Year.groupby("States")[["Transaction_Count","Transaction_Amount"]].sum()
    trans_amounta_count_Year_Group.reset_index(inplace=True)
    col1,col2=st.columns(2)
    with col1:

        fig_amount=px.bar(trans_amounta_count_Year_Group, x="States", y="Transaction_Amount", title=f"TRANSACTION AMOUNT - {year}",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, height=650, width=600)

        st.plotly_chart(fig_amount)

    with col2:
        fig_count=px.bar(trans_amounta_count_Year_Group, x="States", y="Transaction_Count", title=f"TRANSACTION COUNT - {year}",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height=650, width=600)


        st.plotly_chart(fig_count)

    url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response=requests.get(url)
    data1=json.loads(response.content)

    states_Name=[]
    for feature in data1["features"]:
        states_Name.append(feature["properties"]["ST_NM"])

    states_Name.sort()
    col1,col2=st.columns(2)
    with col1:
        fig_india_1=px.choropleth(trans_amounta_count_Year_Group, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                color="Transaction_Amount", color_continuous_scale="Rainbow",
                                range_color=(trans_amounta_count_Year_Group["Transaction_Amount"].min(), trans_amounta_count_Year_Group["Transaction_Amount"].max()),
                                hover_name="States",title=f"TRANSACTION AMOUNT - {year}" , fitbounds="locations", height=600, width=600)
        

        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)
    with col2:
        fig_india_2=px.choropleth(trans_amounta_count_Year_Group, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                color="Transaction_Count", color_continuous_scale="Rainbow",
                                range_color=(trans_amounta_count_Year_Group["Transaction_Count"].min(), trans_amounta_count_Year_Group["Transaction_Count"].max()),
                                hover_name="States",title=f"TRANSACTION COUNT - {year}" , fitbounds="locations", height=600, width=600)
        
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)

    return trans_amounta_count_Year


# Analysis Transaction Amount using year and Quater
def transaction_amount_count_Y_Q(df,quarter):

    trans_amounta_count_Year=df[df["Quarter"]==quarter]
    trans_amounta_count_Year.reset_index(drop=True, inplace=True)

    trans_amounta_count_Year_Group=trans_amounta_count_Year.groupby("States")[["Transaction_Count","Transaction_Amount"]].sum()
    trans_amounta_count_Year_Group.reset_index(inplace=True)
    col1,col2=st.columns(2)
    with col1:
        fig_amount=px.bar(trans_amounta_count_Year_Group, x="States", y="Transaction_Amount", title=f"{trans_amounta_count_Year['Years'].unique()} YEAR {quarter} QUATER TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, height=650, width=600)

        st.plotly_chart(fig_amount)

    with col2:
        fig_count=px.bar(trans_amounta_count_Year_Group, x="States", y="Transaction_Count", title=f"{trans_amounta_count_Year['Years'].unique()} YEAR {quarter} QUATER TRANSACTION COUNT",
                            color_discrete_sequence=px.colors.sequential.Bluered_r, height=650, width=600)

        st.plotly_chart(fig_count)

    url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response=requests.get(url)
    data1=json.loads(response.content)

    states_Name=[]
    for feature in data1["features"]:
        states_Name.append(feature["properties"]["ST_NM"])

    states_Name.sort()
    col1,col2=st.columns(2)
    with col1:
        fig_india_1=px.choropleth(trans_amounta_count_Year_Group, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                color="Transaction_Amount", color_continuous_scale="Rainbow",
                                range_color=(trans_amounta_count_Year_Group["Transaction_Amount"].min(), trans_amounta_count_Year_Group["Transaction_Amount"].max()),
                                hover_name="States",title=f"{trans_amounta_count_Year['Years'].unique()} YEAR {quarter} QUATER TRANSACTION AMOUNT" , fitbounds="locations", height=600, width=600)
        

        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)
    with col2:
        fig_india_2=px.choropleth(trans_amounta_count_Year_Group, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                color="Transaction_Count", color_continuous_scale="Rainbow",
                                range_color=(trans_amounta_count_Year_Group["Transaction_Count"].min(), trans_amounta_count_Year_Group["Transaction_Count"].max()),
                                hover_name="States",title=f"{trans_amounta_count_Year['Years'].unique()} YEAR {quarter} QUATER TRANSACTION COUNT" , fitbounds="locations", height=600, width=600)
        
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)


    return trans_amounta_count_Year

# Analysis Transaction Type using year and State
def Agg_trans_TranType(Agg_tran_tac_Y, state):
    trans_amounta_count_Year=Agg_tran_tac_Y[Agg_tran_tac_Y["States"]==state]
    trans_amounta_count_Year.reset_index(drop=True, inplace=True)

    trans_amounta_count_Year_Group=trans_amounta_count_Year.groupby("Transaction_Type")[["Transaction_Count","Transaction_Amount"]].sum()
    trans_amounta_count_Year_Group.reset_index(inplace=True)
    col1,col2=st.columns(2)
    with col1:
        fig_pie_1=px.pie(data_frame= trans_amounta_count_Year_Group,names= "Transaction_Type", values= "Transaction_Amount",
                            width=600, title=f" TRANSACTION AMOUNT - {state} ", hole= 0.6)

        st.plotly_chart(fig_pie_1)
    with col2:
        fig_pie_2=px.pie(data_frame= trans_amounta_count_Year_Group,names= "Transaction_Type", values= "Transaction_Count",
                            width=600, title=f" TRANSACTION COUNT - {state} ", hole= 0.6)

        st.plotly_chart(fig_pie_2)



# Aggregated User Analysis_1
def Aggr_User_plot_1(df, year):
    Aguy=df[df["Years"]==year]
    Aguy.reset_index(inplace=True, drop=True)
    Aguy_group=pd.DataFrame(Aguy.groupby("Brands")["Transaction_Count"].sum())
    Aguy_group.reset_index(inplace=True)

    fig_bar_1=px.bar(Aguy_group, x="Brands", y="Transaction_Count", title=f"BRAND WISE TRANSACTION COUNT - {year}", 
                        width=600, color_discrete_sequence=px.colors.sequential.haline, hover_name="Brands")
    st.plotly_chart(fig_bar_1)

    return Aguy

#Aggregated User Plot based on Brands and Transaction count

def Aggr_user_plot_Quater(df, Quarter):
    AguyQ=df[df["Quarter"]==Quarter]
    AguyQ.reset_index(inplace=True, drop=True)
    AguyQ_group= pd.DataFrame(AguyQ.groupby("Brands")["Transaction_Count"].sum())
    AguyQ_group.reset_index(inplace=True)
    fig_bar_2=px.bar(AguyQ_group, x="Brands", y="Transaction_Count", title=f"{Quarter}rd QUARTER, BRAND WISE TRANSACTION COUNT ", 
                            width=600, color_discrete_sequence=px.colors.sequential.haline, hover_name="Brands")
    st.plotly_chart(fig_bar_2)

    return AguyQ

#Aggregated User Plot based on States and Transaction count

def Aggr_user_plot_State(df, state):
    Aggr_user_year_Qua_State=df[df["States"]==state]
    Aggr_user_year_Qua_State.reset_index(inplace=True, drop=True)

    fig_line_1=px.line(Aggr_user_year_Qua_State, x="Brands", y="Transaction_Count", hover_data="Percentage",
                        title=f"TRANSACTION COUNT AND PERCENTAGE BASED ON BRANDS in {state.upper()}", color_discrete_sequence=px.colors.sequential.Aggrnyl, 
                        width=1000, markers=True)
    st.plotly_chart(fig_line_1)

#Map Insurance District wise
def map_insu_District(df, state):
    trans_amou_count_Year=df[df["States"]==state]
    trans_amou_count_Year.reset_index(drop=True, inplace=True)

    trans_amounta_count_Year_Group=trans_amou_count_Year.groupby("Districts")[["Transaction_Count","Transaction_Amount"]].sum()
    trans_amounta_count_Year_Group.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:

        fig_bar_1=px.bar(trans_amounta_count_Year_Group, x= "Transaction_Amount" , y="Districts", orientation="h", 
                         title=f"{state} wise TRANSACTION AMOUNT WITH DISTRICTS", 
                         color_discrete_sequence=px.colors.sequential.Redor_r, height=600)
        st.plotly_chart(fig_bar_1)
    with col2:
        fig_bar_2=px.bar(trans_amounta_count_Year_Group, x= "Transaction_Count" , y="Districts", 
                         orientation="h", title=f"{state} wise TRANSACTION COUNT WITH DISTRICTS", 
                         color_discrete_sequence=px.colors.sequential.Bluered, height=600)
        st.plotly_chart(fig_bar_2)

# Map User Year wise register user and app open
def map_user_plot_1(df, year):
    muy=df[df["Years"]==year]
    muy.reset_index(inplace=True, drop=True)
    map_us_group=pd.DataFrame(muy.groupby("States")[["Register_User","App_Open"]].sum())
    map_us_group.reset_index(inplace=True)

    fig_line_1=px.line(map_us_group, x="States", y=["Register_User","App_Open"], 
                            title=f"REGISTER USER AND APP OPEN IN STATE WISE - {year}", 
                            width=1000, height=800,markers=True)
    
    st.plotly_chart(fig_line_1)
    
    return muy

# Map User quarter wise register user and app open
def map_user_plot_2(df, quarter):
    muyQ=df[df["Quarter"]==quarter]
    muyQ.reset_index(inplace=True, drop=True)
    map_us_group=pd.DataFrame(muyQ.groupby("States")[["Register_User","App_Open"]].sum())
    map_us_group.reset_index(inplace=True)

    
    fig_line_2=px.line(map_us_group, x="States", y=["Register_User","App_Open"], 
                            title=f'REGISTER USER AND APP OPEN IN THE YEAR OF {df["Years"].unique()} AND QUARTER OF - {quarter}',
                            color_discrete_sequence=px.colors.sequential.Rainbow,
                            width=1000, height=800,markers=True)
    
    st.plotly_chart(fig_line_2)
    
    return muyQ


# Map user Registered User and App open Details district wise
def map_user_plot_3(df, state):
    muyQS=df[df["States"]==state]
    muyQS.reset_index(inplace=True, drop=True)

    col1,col2=st.columns(2)
    with col1:
        fig_bar_1=px.bar(muyQS, x="Register_User", y="Districts", orientation="h",
                        title=f"REGISTERED USER DETAILS DISTRICT WISE - {state}", height=800, color_discrete_sequence=px.colors.sequential.Agsunset)
        st.plotly_chart(fig_bar_1)
    with col2:
        fig_bar_2=px.bar(muyQS, x="App_Open", y="Districts", orientation="h",
                        title=f"App_Open DETAILS DISTRICT WISE - {state}", height=800, color_discrete_sequence=px.colors.sequential.amp_r)
        st.plotly_chart(fig_bar_2)



#Top Insurance Quater wise Transaction Amount
def top_ins_plot_1(df, state):
    top_ins_Y=df[df["States"]=="West Bengal"]
    top_ins_Y.reset_index(inplace=True, drop=True)
    col1,col2=st.columns(2)
    with col1:
        top_ins_fig_bar_1=px.bar(top_ins_Y, x="Quarter", y="Transaction_Amount", hover_data="Pincodes",
                            title=f"TRANSACTION AMOUNT PINCODE WISE", height=600,width=650, color_discrete_sequence=px.colors.sequential.BuPu_r)
        st.plotly_chart(top_ins_fig_bar_1)
    with col2:
        top_ins_fig_bar_2=px.bar(top_ins_Y, x="Quarter", y="Transaction_Count", hover_data="Pincodes",
                            title=f"TRANSACTION COUNT PINCODE WISE", height=600, width=650, color_discrete_sequence=px.colors.sequential.Blackbody_r)
        st.plotly_chart(top_ins_fig_bar_2)


#Top User Register User plot using States and Quater
def top_register_Plot_1(df, year):
    top_user_Y=df[df["Years"]==year]
    top_user_Y.reset_index(inplace=True, drop=True)

    top_user_Y_G=pd.DataFrame(top_user_Y.groupby(["States", "Quarter"])["Register_User"].sum())
    top_user_Y_G.reset_index(inplace=True)


    top_user_fig_plot_1=px.bar(top_user_Y_G, x="States", y="Register_User", color="Quarter", width=1000, height=800,
                            color_discrete_sequence=px.colors.sequential.Rainbow, hover_name="States")
    st.plotly_chart(top_user_fig_plot_1)

    return top_user_Y

#top user plot for register user based on Quarter and Pincode
def top_user_plot_2(df, states):
    tuyS=df[df["States"]==states]
    tuyS.reset_index(inplace=True, drop=True)

    top_fig_Plot_2=px.bar(tuyS, x="Quarter" , y="Register_User", title=f"REGISTERED USER BASED ON QUARTER", 
                        width=1000, height=800, color="Register_User", hover_name="Pincodes", 
                        color_discrete_sequence=px.colors.sequential.Magenta_r)
    st.plotly_chart(top_fig_Plot_2)



# Maximum, Minimum and Average amounts
def top_chart_transaction_amount(tablename):
    mydb=psycopg2.connect(host='localhost',
                        user='postgres',
                        port='5432',
                        database='PhonePe',
                        password='Password@123')

    cursor = mydb.cursor()

    #Top 10 Maxmimum Transaction Amount and States
    query_1= f'''select states, SUM(transaction_amount) as transaction_amount 
                from {tablename}
                GROUP BY states
                ORDER BY transaction_amount DESC
                LIMIT 10;'''

    cursor.execute(query_1)
    table_1 = cursor.fetchall()
    mydb.commit()

    df_dataframe_1=pd.DataFrame(table_1, columns=("states", "transaction_amount"))

    col1,col2=st.columns(2)
    with col1:
        fig_bar_1=px.bar(df_dataframe_1, x="states", y="transaction_amount", title=f"STATE WISE MAXIMUM TOP 10 TRANSACTION AMOUNT", 
                            height=650, width=600, color_discrete_sequence=px.colors.sequential.haline, hover_name="states")
        st.plotly_chart(fig_bar_1)



    #Top 10 Minimum Transaction Amount and States
    query_2= f'''select states, SUM(transaction_amount) as transaction_amount 
                from {tablename}
                GROUP BY states
                ORDER BY transaction_amount
                LIMIT 10;'''

    cursor.execute(query_2)
    table_2 = cursor.fetchall()
    mydb.commit()

    df_dataframe_2=pd.DataFrame(table_2, columns=("states", "transaction_amount"))

    with col2:
        fig_bar_2=px.bar(df_dataframe_2, x="states", y="transaction_amount", title=f"STATE WISE MINIMUM TOP 10 TRANSACTION AMOUNT", 
                            height=650, width=600, color_discrete_sequence=px.colors.sequential.Oranges_r, hover_name="states")
        st.plotly_chart(fig_bar_2)



    #Average Transaction Amount and States
    query_3= f'''select states, AVG(transaction_amount) as transaction_amount 
                from {tablename}
                GROUP BY states
                ORDER BY transaction_amount;'''

    cursor.execute(query_3)
    table_3 = cursor.fetchall()
    mydb.commit()

    df_dataframe_3=pd.DataFrame(table_3, columns=("states", "transaction_amount"))


    fig_bar_3=px.bar(df_dataframe_3, y="states", x="transaction_amount", title=f"AVERAGE OF TRANSACTION AMOUNT", orientation="h",
                        height=800, width=1000, color_discrete_sequence=px.colors.sequential.Brwnyl_r, hover_name="states")
    st.plotly_chart(fig_bar_3)



# Maximum, Minimum and Average amounts
def top_chart_transaction_count(tablename):
    mydb=psycopg2.connect(host='localhost',
                        user='postgres',
                        port='5432',
                        database='PhonePe',
                        password='Password@123')

    cursor = mydb.cursor()



    #Top 10 Maxmimum Transaction count and States
    query_1= f'''select states, SUM(transaction_count) as transaction_count 
                from {tablename}
                GROUP BY states
                ORDER BY transaction_count DESC
                LIMIT 10;'''

    cursor.execute(query_1)
    table_1 = cursor.fetchall()
    mydb.commit()

    df_dataframe_1=pd.DataFrame(table_1, columns=("states", "transaction_count"))
    col1,col2=st.columns(2)
    with col1:

        fig_bar_1=px.bar(df_dataframe_1, x="states", y="transaction_count", title=f"STATE WISE MAXIMUM TOP 10 TRANSACTION COUNT", 
                            height=650, width=600, color_discrete_sequence=px.colors.sequential.haline, hover_name="states")
        st.plotly_chart(fig_bar_1)



    #Top 10 Minimum Transaction count and States
    query_2= f'''select states, SUM(transaction_count) as transaction_count 
                from {tablename}
                GROUP BY states
                ORDER BY transaction_count
                LIMIT 10;'''

    cursor.execute(query_2)
    table_2 = cursor.fetchall()
    mydb.commit()

    df_dataframe_2=pd.DataFrame(table_2, columns=("states", "transaction_count"))

    with col2:
        fig_bar_2=px.bar(df_dataframe_2, x="states", y="transaction_count", title=f"STATE WISE MINIMUM TOP 10 TRANSACTION COUNT", 
                            height=650, width=600, color_discrete_sequence=px.colors.sequential.Oranges_r, hover_name="states")
        st.plotly_chart(fig_bar_2)

    #Average Transaction count and States
    query_3= f'''select states, AVG(transaction_count) as transaction_count 
                from {tablename}
                GROUP BY states
                ORDER BY transaction_count;'''

    cursor.execute(query_3)
    table_3 = cursor.fetchall()
    mydb.commit()

    df_dataframe_3=pd.DataFrame(table_3, columns=("states", "transaction_count"))


    fig_bar_3=px.bar(df_dataframe_3, y="states", x="transaction_count", title=f"AVERAGE OF TRANSACTION COUNT", orientation="h",
                        height=800, width=1000, color_discrete_sequence=px.colors.sequential.Brwnyl_r, hover_name="states")
    st.plotly_chart(fig_bar_3)



# Registred user from map users
def top_chart_regitered_User(tablename, state):
    mydb=psycopg2.connect(host='localhost',
                        user='postgres',
                        port='5432',
                        database='PhonePe',
                        password='Password@123')

    cursor = mydb.cursor()

    #Top 10 Maxmimum Transaction Amount and States
    query_1= f'''SELECT districts, sum(register_user) as registereduser
                FROM {tablename} 
                WHERE states='{state}'
                GROUP BY districts
                ORDER BY registereduser DESC 
                LIMIT 10;'''

    cursor.execute(query_1)
    table_1 = cursor.fetchall()
    mydb.commit()

    df_dataframe_1=pd.DataFrame(table_1, columns=("districts", "register_user"))

    col1,col2=st.columns(2)
    with col1:
        fig_bar_1=px.bar(df_dataframe_1, x="districts", y="register_user", title=f"DISTRICT WISE TOP 10 REGISTERED USER", 
                            height=650, width=600, color_discrete_sequence=px.colors.sequential.haline, hover_name="districts")
        
        st.plotly_chart(fig_bar_1)



    #Top 10 Minimum Transaction Amount and States
    query_2= f'''SELECT districts, sum(register_user) as registereduser
                FROM {tablename} 
                WHERE states='{state}'
                GROUP BY districts
                ORDER BY registereduser 
                LIMIT 10;'''

    cursor.execute(query_2)
    table_2 = cursor.fetchall()
    mydb.commit()

    df_dataframe_2=pd.DataFrame(table_2, columns=("districts", "registereduser"))

    with col2:
        fig_bar_2=px.bar(df_dataframe_2, x="districts", y="registereduser", title=f"DISTRICT WISE LEAST 10 REGISTERED USER", 
                            height=650, width=600, color_discrete_sequence=px.colors.sequential.Oranges_r, hover_name="districts")
        st.plotly_chart(fig_bar_2)



    #Average Transaction Amount and States
    query_3= f'''SELECT districts, AVG(register_user) as registereduser
                FROM  {tablename}  
                WHERE states='{state}'
                GROUP BY districts
                ORDER BY registereduser;'''

    cursor.execute(query_3)
    table_3 = cursor.fetchall()
    mydb.commit()

    df_dataframe_3=pd.DataFrame(table_3, columns=("districts", "registereduser"))


    fig_bar_3=px.bar(df_dataframe_3, y="districts", x="registereduser", title=f"AVERAGE OF REGISTER USER", orientation="h",
                        height=800, width=1000, color_discrete_sequence=px.colors.sequential.Brwnyl_r, hover_name="districts")
    st.plotly_chart(fig_bar_3)




# app opens details from map user
def top_chart_app_opens(tablename, state):
    mydb=psycopg2.connect(host='localhost',
                        user='postgres',
                        port='5432',
                        database='PhonePe',
                        password='Password@123')

    cursor = mydb.cursor()

    #Top 10 Maxmimum Transaction Amount and States
    query_1= f'''SELECT districts, sum(app_open) as app_open
                FROM {tablename} 
                WHERE states='{state}'
                GROUP BY districts
                ORDER BY app_open DESC 
                LIMIT 10;'''

    cursor.execute(query_1)
    table_1 = cursor.fetchall()
    mydb.commit()

    df_dataframe_1=pd.DataFrame(table_1, columns=("districts", "app_open"))

    col1,col2=st.columns(2)
    with col1:
        fig_bar_1=px.bar(df_dataframe_1, x="districts", y="app_open", title=f"DISTRICT WISE TOP 10 APP OPEN", 
                            height=650, width=600, color_discrete_sequence=px.colors.sequential.haline, hover_name="districts")
        st.plotly_chart(fig_bar_1)



    #Top 10 Minimum Transaction Amount and States
    query_2= f'''SELECT districts, sum(app_open) as app_open
                FROM {tablename} 
                WHERE states='{state}'
                GROUP BY districts
                ORDER BY app_open 
                LIMIT 10;'''

    cursor.execute(query_2)
    table_2 = cursor.fetchall()
    mydb.commit()

    df_dataframe_2=pd.DataFrame(table_2, columns=("districts", "app_open"))

    with col2:
        fig_bar_2=px.bar(df_dataframe_2, x="districts", y="app_open", title=f"DISTRICT WISE LEAST 10 APP OPEN", 
                            height=650, width=600, color_discrete_sequence=px.colors.sequential.Oranges_r, hover_name="districts")
        st.plotly_chart(fig_bar_2)



    #Average Transaction Amount and States
    query_3= f'''SELECT districts, AVG(app_open) as app_open
                FROM  {tablename}  
                WHERE states='{state}'
                GROUP BY districts
                ORDER BY app_open;'''

    cursor.execute(query_3)
    table_3 = cursor.fetchall()
    mydb.commit()

    df_dataframe_3=pd.DataFrame(table_3, columns=("districts", "app_open"))


    fig_bar_3=px.bar(df_dataframe_3, y="districts", x="app_open", title=f"AVERAGE OF APP OPEN", orientation="h",
                        height=800, width=1000, color_discrete_sequence=px.colors.sequential.Brwnyl_r, hover_name="districts")
    st.plotly_chart(fig_bar_3)


# Register user data from top users
def top_chart_regitered_User_data(tablename):
    mydb=psycopg2.connect(host='localhost',
                        user='postgres',
                        port='5432',
                        database='PhonePe',
                        password='Password@123')

    cursor = mydb.cursor()

    #Top 10 Maxmimum Transaction Amount and States
    query_1= f'''select states, sum(register_user) as register_user
                from {tablename}
                GROUP BY states
                ORDER BY register_user DESC
                LIMIT 10;'''

    cursor.execute(query_1)
    table_1 = cursor.fetchall()
    mydb.commit()

    df_dataframe_1=pd.DataFrame(table_1, columns=("states", "register_user"))
    col1,col2=st.columns(2)
    with col1:

        fig_bar_1=px.bar(df_dataframe_1, x="states", y="register_user", title=f"STATE WISE TOP 10 REGISTERED USER", 
                            height=650, width=600, color_discrete_sequence=px.colors.sequential.haline, hover_name="states")
    
        st.plotly_chart(fig_bar_1)


    #Top 10 Minimum Transaction Amount and States
    query_2= f'''select states, sum(register_user) as register_user
                from {tablename}
                GROUP BY states
                ORDER BY register_user
                LIMIT 10;'''

    cursor.execute(query_2)
    table_2 = cursor.fetchall()
    mydb.commit()

    df_dataframe_2=pd.DataFrame(table_2, columns=("states", "register_user"))
    
    with col2:

        fig_bar_2=px.bar(df_dataframe_2, x="states", y="register_user", title=f"STATE WISE LEAST 10 REGISTERED USER", 
                            height=650, width=600, color_discrete_sequence=px.colors.sequential.Oranges_r, hover_name="states")
        
        st.plotly_chart(fig_bar_2)



    #Average Transaction Amount and States
    query_3= f'''select states, AVG(register_user) as register_user
                from {tablename}
                GROUP BY states
                ORDER BY register_user
                LIMIT 10;'''

    cursor.execute(query_3)
    table_3 = cursor.fetchall()
    mydb.commit()

    df_dataframe_3=pd.DataFrame(table_3, columns=("states", "register_user"))


    fig_bar_3=px.bar(df_dataframe_3, y="states", x="register_user", title=f"STATE WISE AVERAGE OF REGISTER USER", orientation="h",
                        height=700, width=1000, color_discrete_sequence=px.colors.sequential.Brwnyl_r, hover_name="states")
    
    st.plotly_chart(fig_bar_3)













# streamlit Part
st.set_page_config(layout='wide')

st.title('PHONEPE DATA VISULIZATION AND EXPLORATION')


with st.sidebar: 
    
    select = option_menu("Main Menu", ["HOME", "DATA EXPLORATION", "TOP CHART",])

if select=="HOME":
    
    col1,col2= st.columns(2)

    with col1:
        st.header("PHONEPE")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("PhonePe  is an Indian digital payments and financial technology company")
        st.write("****FEATURES****")
        st.write("****Credit & Debit card linking****")
        st.write("****Bank Balance check****")
        st.write("****Money Storage****")
        st.write("****PIN Authorization****")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
    with col2:
        st.video("https://youtu.be/mMch1jF6JB8")

    col3,col4= st.columns(2)
    
    with col3:
        st.image(Image.open(r"E:\GUVI\Capstone Project\PhonePe\Images\phonepe1.png"), width=450)

    with col4:
        st.write("****Easy Transactions****")
        st.write("****One App For All Your Payments****")
        st.write("****Your Bank Account Is All You Need****")
        st.write("****Multiple Payment Modes****")
        st.write("****PhonePe Merchants****")
        st.write("****Multiple Ways To Pay****")
        st.write("****1.Direct Transfer & More****")
        st.write("****2.QR Code****")
        st.write("****Earn Great Rewards****")

    col5,col6= st.columns(2)

    with col5:
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.write("****No Wallet Top-Up Required****")
        st.write("****Pay Directly From Any Bank To Any Bank A/C****")
        st.write("****Instantly & Free****")

    with col6:
        st.image(Image.open(r"E:\GUVI\Capstone Project\PhonePe\Images\phonepe4.png"), width=450)
        # st.video("https://youtu.be/QG6iEwlnPoE")



elif select=="DATA EXPLORATION":

    tab1, tab2, tab3 = st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])

    with tab1:
        method1=st.radio("Select Method",["Aggregated_Insurance", "Aggregated_Transaction", "Aggregated_User"])

        if method1 =="Aggregated_Insurance":

            col1,col2=st.columns(2)
            with col1:
                years=st.selectbox("Select The Years",aggr_Insurance["Years"].unique())
                #years=st.slider("Select Years", aggr_Insurance["Years"].min(),aggr_Insurance["Years"].max())
            tac_Y=transaction_amount_count_Y(aggr_Insurance,years)
            
            col1,col2=st.columns(2)
            with col1:
                 Quater=st.selectbox("Select The Quater",tac_Y["Quarter"].unique())
            transaction_amount_count_Y_Q(tac_Y,Quater)

        elif method1=="Aggregated_Transaction":

            col1,col2=st.columns(2)
            with col1:
                years=st.selectbox("Select The Years",aggregated_Transaction["Years"].unique())
                #years=st.slider("Select Years", aggr_Insurance["Years"].min(),aggr_Insurance["Years"].max())
            Agg_tran_tac_Y=transaction_amount_count_Y(aggregated_Transaction,years)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select The States for Year:", Agg_tran_tac_Y["States"].unique())
            Agg_trans_TranType(Agg_tran_tac_Y,states)

            col1,col2=st.columns(2)
            with col1:
                 Quater=st.selectbox("Select The Quater",Agg_tran_tac_Y["Quarter"].unique())
            Agg_tran_tac_Y_Q=transaction_amount_count_Y_Q(Agg_tran_tac_Y,Quater)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select The States for Quarter:", Agg_tran_tac_Y_Q["States"].unique())
            Agg_trans_TranType(Agg_tran_tac_Y_Q,states)

        elif method1=="Aggregated_User":
            col1,col2=st.columns(2)
            with col1:
                #years=st.selectbox("Select The Years",aggregated_Transaction["Years"].unique())
                years=st.slider("Select Years", aggregated_Users["Years"].min(),aggregated_Users["Years"].max())
            Aggr_User_Year=Aggr_User_plot_1(aggregated_Users,years)

            col1,col2=st.columns(2)
            with col1:
                 Quater=st.selectbox("Select The Quater",Aggr_User_Year["Quarter"].unique())
            Aggr_User_Year_Quarter=Aggr_user_plot_Quater(Aggr_User_Year,Quater)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select The States for Brands:", Aggr_User_Year_Quarter["States"].unique())
            Aggr_user_plot_State(Aggr_User_Year_Quarter,states)


    with tab2:
        method2=st.radio("Select Method",["Map_Insurance", "Map_Transaction", "Map_User"])

        if method2 =="Map_Insurance":

            col1,col2=st.columns(2)
            with col1:
                #years=st.selectbox("Select The Years",aggregated_Transaction["Years"].unique())
                years=st.slider("Select Years For Getting Map Insurance Values:", map_Insurance["Years"].min(),map_Insurance["Years"].max())
            map_insura_Year=transaction_amount_count_Y(map_Insurance,years)

            col1,col2=st.columns(2)
            with col1:
                #years=st.selectbox("Select The Years",aggregated_Transaction["Years"].unique())
                states=st.selectbox("Select The States for Getting Transaction Values:", map_insura_Year["States"].unique())
            map_insu_District(map_insura_Year,states)

            col1,col2=st.columns(2)
            with col1:
                 Quater=st.selectbox("Select The Quater for getting Transaction Details",map_insura_Year["Quarter"].unique())
            map_insu_tac_Y_Q=transaction_amount_count_Y_Q(map_insura_Year,Quater)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select The States for getting Quarter wise Details:", map_insu_tac_Y_Q["States"].unique())
            map_insu_District(map_insu_tac_Y_Q,states)

                        
        elif method2=="Map_Transaction":

            col1,col2=st.columns(2)
            with col1:
                #years=st.selectbox("Select The Years",aggregated_Transaction["Years"].unique())
                years=st.slider("Select Years For Getting Map Insurance Values:", map_Insurance["Years"].min(),map_Insurance["Years"].max())
            map_tran_tac_Y=transaction_amount_count_Y(map_Insurance,years)

            col1,col2=st.columns(2)
            with col1:
                #years=st.selectbox("Select The Years",aggregated_Transaction["Years"].unique())
                states=st.selectbox("Select The States for Getting Transaction Values:", map_tran_tac_Y["States"].unique())
            map_insu_District(map_tran_tac_Y,states)

            col1,col2=st.columns(2)
            with col1:
                 Quater=st.selectbox("Select The Quater for getting Transaction Details",map_tran_tac_Y["Quarter"].unique())
            map_trans_tac_Y_Q=transaction_amount_count_Y_Q(map_tran_tac_Y,Quater)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select The States for getting Quarter wise Details:", map_trans_tac_Y_Q["States"].unique())
            map_insu_District(map_trans_tac_Y_Q,states)

        elif method2=="Map_User":
            
            col1,col2=st.columns(2)
            with col1:
                #years=st.selectbox("Select The Years",aggregated_Transaction["Years"].unique())
                years=st.slider("Select Years for getting Regiter user and App open:", map_Users["Years"].min(),map_Users["Years"].max())
            map_user_Y=map_user_plot_1(map_Users,years)

            col1,col2=st.columns(2)
            with col1:
                 Quater=st.selectbox("Select The Quater for getting Transaction Details",map_user_Y["Quarter"].unique())
            Map_user_Y_Q=map_user_plot_2(map_user_Y,Quater)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select The States for getting District wise Details:", Map_user_Y_Q["States"].unique())
            map_user_plot_3(Map_user_Y_Q,states)
    
    with tab3:
        method3=st.radio("Select Method",["Top_Insurance", "Top_Transaction", "Top_User"])

        if method3 =="Top_Insurance":
            
            col1,col2=st.columns(2)
            with col1:
                #years=st.selectbox("Select The Years",aggregated_Transaction["Years"].unique())
                years=st.slider("Select Years For Getting Top Insurance Values:", top_Insurance["Years"].min(),top_Insurance["Years"].max())
            top_insu_tac_Y=transaction_amount_count_Y(top_Insurance,years)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select The States for getting Pincode wise Insurance Amount:", top_insu_tac_Y["States"].unique())
            top_ins_plot_1(top_insu_tac_Y,states)

            col1,col2=st.columns(2)
            with col1:
                 Quater=st.selectbox("Select The Quater for getting Insurance Details in Top Insurance:",top_insu_tac_Y["Quarter"].unique())
            top_insu_tac_Y_Q=transaction_amount_count_Y_Q(top_insu_tac_Y,Quater)

        elif method3=="Top_Transaction":
            
            col1,col2=st.columns(2)
            with col1:
                #years=st.selectbox("Select The Years",aggregated_Transaction["Years"].unique())
                years=st.slider("Select Years For Getting Top Transaction Values:", top_Transaction["Years"].min(),top_Transaction["Years"].max())
            top_trans_tac_Y=transaction_amount_count_Y(top_Transaction,years)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select The States for getting Pincode wise Transaction Amount:", top_trans_tac_Y["States"].unique())
            top_ins_plot_1(top_trans_tac_Y,states)

            col1,col2=st.columns(2)
            with col1:
                 Quater=st.selectbox("Select The Quater for getting Transaction Details in Top Transaction:",top_trans_tac_Y["Quarter"].unique())
            top_insu_tac_Y_Q=transaction_amount_count_Y_Q(top_trans_tac_Y,Quater)

        elif method3=="Top_User":
            
            col1,col2=st.columns(2)
            with col1:
                #years=st.selectbox("Select The Years",aggregated_Transaction["Years"].unique())
                years=st.slider("Select Years For Getting Top Transaction Values:", top_Transaction["Years"].min(),top_Transaction["Years"].max())
            top_us_Y=top_register_Plot_1(top_users,years)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select The States for getting Pincode wise Register User:", top_us_Y["States"].unique())
            top_user_plot_2(top_us_Y,states)

elif select=="TOP CHART":
    
    question=st.selectbox("Select The Question",["1. Transaction Amount and Count of Aggregated Insurance",
                                                    "2. Transaction Amount and Count of Map Insurance",
                                                    "3. Transaction Amount and Count of Top Insurance",
                                                    "4. Transaction Amount and Count of Aggregated Transaction",
                                                    "5. Transaction Amount and Count of Map Transaction",
                                                    "6. Transaction Amount and Count of Top Transaction",
                                                    "7. Transaction Count of Aggregated User",
                                                    "8. Registered User of Map User",
                                                    "9. App Opens of Map User",
                                                    "10. Registered Users of Top User"])
    
    if question == "1. Transaction Amount and Count of Aggregated Insurance":
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggr_Insurance")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggr_Insurance")

    elif question == "2. Transaction Amount and Count of Map Insurance":
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggr_Insurance")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggr_Insurance")

    elif question == "3. Transaction Amount and Count of Top Insurance":
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_Insurance")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_Insurance")

    elif question == "3. Transaction Amount and Count of Top Insurance":
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_Insurance")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_Insurance")

    elif question == "4. Transaction Amount and Count of Aggregated Transaction":
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_Transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_Transaction")

    elif question == "5. Transaction Amount and Count of Map Transaction":
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_Trans")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_Trans")

    elif question == "6. Transaction Amount and Count of Top Transaction":
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_Transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_Transaction")

    elif question == "7. Transaction Count of Aggregated User":
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_User")

    elif question == "8. Registered User of Map User":

        col1,col2=st.columns(2)
        with col1:
            states=st.selectbox("Select The States from Register User:", map_Users["States"].unique())
        st.subheader("REGISTRERED USER")
        top_chart_regitered_User("map_Users", states)

    elif question == "9. App Opens of Map User":

        col1,col2=st.columns(2)
        with col1:
            states=st.selectbox("Select The States from Register User:", map_Users["States"].unique())
        st.subheader("APP OPENS")
        top_chart_app_opens("map_Users", states)

    elif question == "10. Registered Users of Top User":

        st.subheader("REGISTER USER")
        top_chart_regitered_User_data("top_user")