import requests
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import json
from PIL import Image
import streamlit as st
from streamlit_folium import folium_static
import folium
import folium.plugins as plugins

#import matplotlib as mpl
#from st_annotated_text import annotated_text

#with open(r'F:/style.css') as c:
#    st.markdown(c.read(),unsafe_allow_html=True)
#with open(r'F:/index.html') as i:
#    st.markdown(i.read(),unsafe_allow_html=True)
#with open(r'F:/script.js') as j:
#    st.markdown(j.read(),unsafe_allow_html=True)

st.markdown('<style>#MainMenu {Visibility:hidden;}footer {Visibility:hidden;} </style>',unsafe_allow_html=True)

###############################SIDEBAR#####################################
st.sidebar.title('Visual Tweak Toolbar')
pl=st.sidebar.selectbox('Select chart type:',('Area','Line')).lower()

st.sidebar.markdown('---')

st.sidebar.markdown('\
    <html>\
    <head>\
    \
    <link rel="stylesheet" type="text/css" href="https://cdn.rawgit.com/vaakash/socializer/80391a50/css/socializer.min.css">\
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">\
    \
    </head>\
    <body>\
    \
    <h3>Connect with me on </h3>\
    <div class="socializer a sr-32px sr-opacity sr-icon-dark sr-bg-none sr-pad"><span class="sr-facebook"><a href="https://www.facebook.com/sourav.nanda.528" target="_blank" title="Facebook"><i class="fa fa-facebook"></i></a></span><span class="sr-instagram"><a href="https://www.instagram.com/_sourav_nanda_/?hl=en" target="_blank" title="Instagram"><i class="fa fa-instagram"></i></a></span><span class="sr-github"><a href="https://github.com/sourav-nanda/" target="_blank" title="Github"><i class="fa fa-github"></i></a></span><span class="sr-linkedin"><a href="https://www.linkedin.com/in/sourav-nanda-31ab841aa/" target="_blank" title="LinkedIn"><i class="fa fa-linkedin"></i></a></span></div>\
    <div class="circleborder"><img class="face" src="https://instagram.fbbi1-1.fna.fbcdn.net/v/t51.2885-19/s150x150/60169341_437177673747856_6481553481608986624_n.jpg?_nc_ht=instagram.fbbi1-1.fna.fbcdn.net&_nc_ohc=QznaJuHwRWcAX9A_7eE&oh=3123e4ecb63e818c987d64b478bac5e0&oe=5F7F1267" alt="face" width="56" height="56"></div>\
    \
    <style>\
    .face {\
    border-radius: 50%;}\
    \
    .circleborder {\
    \
    border: 10px double silver;\
    border-radius: 100%;\
    display: inline-block;\
    box-shadow:  -5px -5px 20px #868686, 5px 5px 20px #fafafa;\
    }\
    <\style>\
    </body>\
    </html> \
    ',unsafe_allow_html=True)

###############################SIDEBAR#####################################

plt.style.use('ggplot')
url=r'https://api.covid19india.org/data.json'
img_path=r'F:\maxresdefault.jpg'
#coor_url=r'https://api.covid19india.com/dayone/country/India/status/confirmed'

@st.cache(suppress_st_warning=True)
def icon(name):
    st.markdown('<style>'+open(r'icons.css').read()+'</style>',unsafe_allow_html=True)
    st.markdown(f'<i class="material-icons">{name}</i>',unsafe_allow_html=True)
    
#start_date=st.date_input('Enter Start Date:')
#end_date=st.date_input('Enter End Date:')
#url = r'https://api.covidindiatracker.com/state_data.json'
#querystring = {"start_date":"2020- 08-01","end_date":"2020-08-25"}
st.cache() 
def imageloader():
    img=np.array(Image.open(img_path))
    st.image(img,use_column_width=True)

@st.cache()
def ___(url):
    response = requests.get(url).text
    response=json.loads(response)
    time_series=response['cases_time_series']
    state=response['statewise']
    tested=response['tested']
    return (time_series,state,tested)

data=___(url)

#st.write('<img src="https://i.ytimg.com/vi/PSnSo9kYlH4/maxresdefault.jpg" width="700" height="385" style="vertical-align:left">',unsafe_allow_html=True)
imageloader()

st.title('Covid-19 Dashboard')
st.header('India Overview')

st.header('Total')


regional_df=pd.DataFrame(data[1])
regional_df.columns=map(lambda x:x.capitalize(),regional_df.columns)

regional_df.drop([36],axis=0,inplace=True)
d_region=list(regional_df[regional_df.State=='Total'].drop(['Deltaconfirmed',
                                                       'Deltadeaths',
                                                       'Deltarecovered',
                                                       'Lastupdatedtime',
                                                       'Migratedother',
                                                       'State',
                                                       'Statecode',
                                                       'Statenotes'],axis=1).itertuples())

#css
#st.write(d_region[0])
total_status=f'<div style="padding:10px; width:180px; height:50px; background:deepskyblue; display:block; text-align:left;">\
Active'+' '+f'{d_region[0][1]}</div><div style="padding:10px; width:180px; height:50px; background:lightcoral; display:block; text-align:left;">\
Confirmed'+' '+f'{d_region[0][2]}</div></body></html><div style="padding:10px; width:180px; height:50px; background:silver;  display:block; text-align:left;">\
Deceased'+' '+f'{d_region[0][3]}</div></body></html><div style="padding:10px; width:180px; height:50px; background:lightgreen; display:block; text-align:left;">\
Recovered'+' '+f'{d_region[0][4]}</div></body></html>'


#body_color='<html><style>body {background-color: lightgray;}</style></body></html>'
st.markdown(total_status,unsafe_allow_html=True)
#st.markdown(body_color,unsafe_allow_html=True)


time_series=pd.DataFrame(data[0])
time_series.columns=map(lambda x:x.capitalize(),time_series.columns)

cm = sns.light_palette("gray", as_cmap=True)
styler=time_series.style.background_gradient(cmap=cm)

if st.checkbox('See raw data'):
    st.write('You can sort the values of the data by tapping/clicking on a column header')
    st.dataframe(styler)

time_daily=time_series[['Dailyconfirmed',
                        'Dailydeceased',
                        'Dailyrecovered',
                        'Date']].set_index('Date')

time_daily[['Dailyconfirmed','Dailydeceased','Dailyrecovered']]=time_daily[['Dailyconfirmed','Dailydeceased','Dailyrecovered']].astype('int64')

time_total=time_series.drop(['Dailyconfirmed',
                             'Dailydeceased',
                             'Dailyrecovered'],
                              axis=1).set_index('Date')

time_total[['Totalconfirmed','Totaldeceased','Totalrecovered']]=time_total[['Totalconfirmed','Totaldeceased','Totalrecovered']].astype('int64')

time_daily.plot(subplots=False,
                sharey=True,
                title='Daily Interval',
                kind=pl,
                stacked=False,
                linewidth=5,
                color=['lightcoral','silver','lightgreen'],
                figsize=(11,5),
                )
st.pyplot()

time_total.plot(title='Total Data',
                kind=pl,
                figsize=(11,5),
                subplots=False,
                linewidth=5,
                stacked=False,
                color=['lightcoral','silver','lightgreen'],
                sharey=True,
                ylabel='Cases (in millions)')
#plt.ticklabel_format(style='plain',axis='y')
st.pyplot()   


#regional_df.index=regional_df.Region

st.header('Regional Overview')
state=st.selectbox('Select a state:',regional_df.State[1:].to_list())

def state_data():
    df=regional_df[regional_df.State==state]
    return df


rdf=state_data()
#check
st.subheader('Statenotes')
for iterator in rdf.Statenotes:
    st.write(iterator,end='')
#st.write(rdf.Statenotes.to_string(index=False))


time=rdf.Lastupdatedtime.to_string(index=False)
st.subheader(f'Last Updated on {time[0:11]} at {time[12:]}')
state_rdf=rdf.drop(['Statecode',
                    'Statenotes',
                    'State',
                    'Migratedother',
                    'Lastupdatedtime',
                    'Deltaconfirmed',
                    'Deltadeaths',
                    'Deltarecovered'],axis=1).copy()

state_rdf.rename({'Deaths':'Deceased'},inplace=True,axis=1)

st.table(state_rdf.T)
state_rdf=state_rdf.astype('int64')

#Individual State Plot
state_rdf.plot(marker='*',
               color=['deepskyblue','lightcoral','silver','lightgreen'],
               title=state,
               figsize=(7,4),
               ylabel='Cases')

plt.xticks(range(len(state_rdf.index)),state_rdf.index)
st.pyplot()
 
#regional_df.plot(subplots=True,colormap='viridis',stacked=False,sort_columns=True)
clean_rdf=regional_df.drop(['Statecode',
                            'Deltaconfirmed',
                            'Deltadeaths',
                            'Deltarecovered',
                            'Statenotes',
                            'State',
                            'Migratedother',
                            'Lastupdatedtime'],axis=1).astype('int64').copy()

clean_rdf.rename({'Deaths':'Deceased'},inplace=True,axis=1)
clean_rdf=clean_rdf.iloc[1:,:]
clean_rdf.index=regional_df.State[1:]

#Overall State Data Plot
clean_rdf.plot(subplots=False,
               sharey=True,
               figsize=(11,6),
               kind=pl,               
               x_compat=True,
               xlabel='',
               linewidth=5,
               color=['deepskyblue','lightcoral','silver','lightgreen'],
               rot=82)

plt.ticklabel_format(style='plain',axis='y')
plt.xticks(range(len(clean_rdf.index)),clean_rdf.index,fontsize=11)
plt.yticks(fontsize=12)

sns.despine()
st.pyplot()


fig,ax=plt.subplots(figsize=(9,39))
clean_rdf.plot.hist(sharey=True,
                    stacked=False,
                    subplots=True,
                    sharex=False,
                    ax=ax,
                    color=['deepskyblue','lightcoral','silver','lightgreen'],
                    ylabel='States')

plt.rc('legend',fontsize=15)
plt.rc('axes',labelsize=12)
ax.set_title('Statewise Distribution of Cases', fontsize=30)
plt.yticks(range(len(clean_rdf.index)),clean_rdf.index,)
ax.set_ylabel('Frequency')
#plt.ticklabel_format(style='plain',axis='y')
st.pyplot()



#tested_df=pd.DataFrame(data[2])
#tested_df.columns=map(lambda x:x.capitalize(),tested_df.columns)
#tested_df.Updatetimestamp=tested_df.Updatetimestamp.astype('datetime64')
#tested_df.Testspermillion=tested_df.Testspermillion.astype('int64')

#st.dataframe(tested_df)

#@st.cache(suppress_st_warning=True)


@st.cache()
def country_data():
    u='https://pomber.github.io/covid19/timeseries.json'
    try:
        r=requests.get(u,verify=False).text
    except ConnectionError:
        st.write('It seems theres a connnection error :confused: not your fault though :smiley:, just refresh the page.',Unsafe_allow_html=True)
    finally:
        r=json.loads(r)
        da=pd.DataFrame(r)
        return (da,r)
country_df,r=country_data()

#return (df,r)

#########################Map_#######################################
#ind=pd.read_json(r'C:\Users\Saroj\Downloads\in.json')
#ind.rename({'lng':'lon'},inplace=True,axis=1)
#coords_grp=ind.groupby('admin').median()

tiles=['CartoDB positron','Stamen Terrain','Stamen Toner','Stamen Watercolor','OpenStreetMap','CartoDB dark_matter']

m=folium.Map([20.5937, 78.9629],zoom_start=5)

stat=state_rdf.to_string(index=False)

lat=[19.300229,10.959789,16.630049,14.805643,28.625976,27.598203,23.255716,25.429921,18.1124,22.291606,26.404705,26.452103,20.397666,29.153938,11.666667,9.494647,31.187630,34.147328,23.347768,21.233333,30.324427,15.498289,23.836049,11.933812,24.808053,31.104423,25.674673,27.102349,23.254688,34.17,30.736292,20.564715,25.573987,27.325739,23.736701,10.566667]
lon=[75.346739,78.151884,79.793588,76.738056,77.215747,79.040305,88.363044,85.245790,79.0193,72.587265,92.798934,75.138671,85.326136,76.853736,77.402892,76.331108,75.753327,74.631323,86.185448,81.633333,78.033922,73.824541,91.279386,79.829792,93.944203,77.166623,94.110988,93.692047,92.750000,77.58,76.788398,71.910156,91.896807,88.612155,92.714596,72.616667]

html=folium.Html('<div style="padding:10px; width:180px; height:50px; background:deepskyblue; display:block; text-align:left;">{stat}</div>',script=True)

#Dropping state unassigned
state_list=regional_df.State[1:].to_list()


for coordinates,state in zip(zip(lat,lon),state_list):
    rdf=regional_df[regional_df.State==state]
    stat=rdf.drop(['Statecode',
                    'Statenotes',
                    'State',
                    'Migratedother',
                    'Lastupdatedtime',
                    'Deltaconfirmed',
                    'Deltadeaths',
                    'Deltarecovered'],axis=1).to_html(classes='table table-striped table-hover table-condensed table-responsive',index=False)
    
    folium.Marker(coordinates,tooltip=state,icon=folium.Icon(color='blue',
                                                      icon_color='white',
                                                      icon='info',
                                                      prefix='fa'),popup=stat).add_to(m)

for tile in tiles:
    folium.raster_layers.TileLayer(tiles=tile).add_to(m)

folium.LayerControl().add_to(m)
plugins.Fullscreen(position='bottomright').add_to(m)
#icon('map')

folium_static(m)

#########################Map#######################################

st.header('Other Countries Overview')
cou=st.selectbox('Select a country',country_df.columns)
country_df=pd.DataFrame(r[cou])


country_df.index=country_df.date
#country_df.rename([{'deaths':'Deceased'},{confirmed':''}],inplace=True,axis=1)
country_df.columns=['0','Confirmed','Deceased','Recovered']
fig,axes=plt.subplots()
country_df.plot(figsize=(10,5),
                stacked=False,
                kind=pl,
                linewidth=5,
                color=['deepskyblue','silver','lightgreen'],
                ax=axes)


axes.ticklabel_format(style='plain',axis='y')
plt.legend()
axes.set_xlabel('Dates')
axes.set_ylabel('Cases')
st.pyplot()

if st.button('About'):
    st.write('I am an undergrad student pursuing the field of Data Science so I don\'t have much time on hand for hobby projects but still I took a pause from the machine learning and deep learning stuff and devoted some time towards this project.Although this project involves some minimal data manipulation including but not limited to preprocessing but still it isn\'t something that I should actively spend my time on so there will be very minor updates in the forthcoming future.')
    
    st.markdown('Give me a :star: on github if you like the app')

if st.button('Spoiler'):
    st.markdown('I am thinking of adding a section which provides some future insights into the pandemic by predicting the covid statistics upto one week from present or more depending upon the robustness of the model. As I am still relatively new to time series forecasting it will take some time so I can\'t promise anything :wink:')
