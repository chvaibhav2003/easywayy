from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events










import streamlit as st
import pandas as pd
import json
from streamlit.components.v1 import html
import requests
from streamlit_js_eval import streamlit_js_eval, copy_to_clipboard, create_share_link, get_geolocation
from streamlit_lottie import st_lottie
import wayPoints
import route

import numpy as np
api_key = "AIzaSyBrzyHfcq2m5-Vj61HSF2rPNlDt4RDWh_w"
R1 = ['Chiranjeev Vihar,Ghaziabad', 'MASURI,Ghaziabad', 'Panchsheel Primrose,Ghaziabad', 'Hapur_Chungi,Ghaziabad', 'ABES Crossing,Ghaziabad', 'Agrasen_Tiraha(diamond Tiraha),Ghaziabad', 'ManipalHospital,Ghaziabad', 'Vijay nagar,Ghaziabad', 'Hapur Chungi,Ghaziabad', 'Mishal Garhi,Ghaziabad', 'Shastri Nagar D-Block,Ghaziabad', 'District Court and Session Court,Ghaziabad', 'GovindPuram,Ghaziabad', 'Kavi Nagar Industrial Area,Ghaziabad', 'Sector 62,Noida', 'PandavNagar,Ghaziabad', 'Dasna,Ghaziabad', 'SunderDeep Group of Institutions,Ghaziabad', 'WaveCity,Ghaziabad', 'Aditya World City,Ghaziabad', 'Chipyana Khrud Urf Tigri,Ghaziabad', 'Bamheta,Ghaziabad', 'IMS Engineering College,Ghaziabad', 'Kavi Nagar,Ghaziabad', 'RDC,Ghaziabad', 'Harsaon Kamla Nehru Nagar,Ghaziabad', 'Lal Kuan,Ghaziabad', 'Police_Line,Ghaziabad','OTHER OPTIONS']
R2 = ['Chiranjeev Vihar,Ghaziabad', 'MASURI,Ghaziabad', 'Panchsheel Primrose,Ghaziabad', 'Hapur_Chungi,Ghaziabad', 'ABES Crossing,Ghaziabad', 'Agrasen_Tiraha(diamond Tiraha),Ghaziabad', 'ManipalHospital,Ghaziabad', 'Vijay nagar,Ghaziabad', 'Hapur Chungi,Ghaziabad', 'Mishal Garhi,Ghaziabad', 'Shastri Nagar D-Block,Ghaziabad', 'District Court and Session Court,Ghaziabad', 'GovindPuram,Ghaziabad', 'Kavi Nagar Industrial Area,Ghaziabad', 'Sector 62,Noida', 'PandavNagar,Ghaziabad', 'Dasna,Ghaziabad', 'SunderDeep Group of Institutions,Ghaziabad', 'WaveCity,Ghaziabad', 'Aditya World City,Ghaziabad', 'Chipyana Khrud Urf Tigri,Ghaziabad', 'Bamheta,Ghaziabad', 'IMS Engineering College,Ghaziabad', 'Kavi Nagar,Ghaziabad', 'RDC,Ghaziabad', 'Harsaon Kamla Nehru Nagar,Ghaziabad', 'Lal Kuan,Ghaziabad','OTHER OPTIONS....', 'Police_Line,Ghaziabad']
dataMain = get_geolocation()
try:
    lat,lon = [str(dataMain["coords"]["latitude"]),str(dataMain["coords"]["longitude"])]
except TypeError:
    st.warning("Location Not Allowed! App Will Fail")
hub_data=pd.read_excel("hub.xlsx")

def hub_finder(df,lon2,lat2):

    def haversine_vectorize(lon1, lat1, lon2, lat2):

        lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

        newlon = lon2 - lon1
        newlat = lat2 - lat1
        
        haver_formula = np.sin(newlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(newlon/2.0)**2

        dist = 2 * np.arcsin(np.sqrt(haver_formula ))
        km = 6367 * dist #6367 for distance in KM for miles use 3958
        return km

    df['dist_km'] = haversine_vectorize(df['Longitude'],df['Latitude'],lon2,lat2)
    df=df.sort_values('dist_km')
    df['cost_RS']=np.ceil(df['dist_km']/3)*10
    temp_df = (df.loc[:3])
    return temp_df

def load_lottie(filepath:str):
    with open(filepath,"r") as f:
        return json.load(f)
lottie_login = load_lottie("login.json")
lottie_city1 = load_lottie("city1.json")
lottie_city2 = load_lottie("city2.json")
lottie_arrow = load_lottie("arrow.json")
lottie_rickshaw = load_lottie("rickshaw.json")
lottie_driver = load_lottie("driver.json")
lottie_register = load_lottie("register.json")


def fetchUserStats(inital,final):
    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    headers = {"origins":"{}".format(inital),
    "destinations":"{}".format(final),
    "key":"{}".format(api_key)}
    data = requests.get(url,params=headers).json()
    print(data)
    st.write("### The Total Distance From Your Current Location and Passenger is ".format(final.title())+data["rows"][0]["elements"][0]["distance"]["text"]+" and it will take about "+data["rows"][0]["elements"][0]["duration"]["text"])
    return data["rows"][0]["elements"][0]["distance"]["text"]
def drawMap(initial,final):
    pureHTML="""
        <style>#googleMap{{
                width: 100%;
                height: 1000px;
            }} 
        </style>
        <div id="googleMap">
        </div>
        <script src="https://maps.googleapis.com/maps/api/js?key={}&libraries=places"></script>
        <script>
            var mylatlng = {{lat:28.6785357
                            ,lng:77.5106955}};
    var mapOptions = {{
        center : mylatlng,
        zoom:18,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    }}
    var map = new google.maps.Map(document.getElementById("googleMap"), mapOptions);
    var directionsService = new google.maps.DirectionsService();
    var directionsDisplay = new google.maps.DirectionsRenderer();
    directionsDisplay.setMap(map);
    function calcRoute(){{
        var request = {{
            origin:"{}",
            destination:"{}",
            travelMode : google.maps.TravelMode.DRIVING,
            unitSystem : google.maps.UnitSystem.IMPERIAL
        }}
        directionsService.route(request,(result,status)=>{{
            if (status == google.maps.DirectionsStatus.OK){{
                directionsDisplay.setDirections(result);

            }}else{{
                directionsDisplay.setDirections({{routes:[]}})
                map.setCenter(mylatlng);
            }}
        }});
    }}
    calcRoute();
        </script>
    """.format(api_key,initial,final)
    html(pureHTML,height=500)


def drawMapWayPoints(initial,final,waypoint):
    print(waypoint)
    pureHTML="""
        <style>#googleMap{{
                width: 100%;
                height: 1000px;
            }} 
        </style>
        <div id="googleMap">
        </div>
        <script src="https://maps.googleapis.com/maps/api/js?key={}&libraries=places"></script>
        <script>
            var mylatlng = {{lat:28.6785357
                            ,lng:77.5106955}};
    var mapOptions = {{
        center : mylatlng,
        zoom:18,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    }}
    var waypoints = [
        {}
    ];
    var map = new google.maps.Map(document.getElementById("googleMap"), mapOptions);
    var directionsService = new google.maps.DirectionsService();
    var directionsDisplay = new google.maps.DirectionsRenderer();
    directionsDisplay.setMap(map);
    function calcRoute(){{
        var request = {{
            origin:"{}",
            destination:"{}",
            waypoints: waypoints,
            travelMode : google.maps.TravelMode.DRIVING,
            unitSystem : google.maps.UnitSystem.IMPERIAL
        }}
        directionsService.route(request,(result,status)=>{{
            if (status == google.maps.DirectionsStatus.OK){{
                directionsDisplay.setDirections(result);

            }}else{{
                directionsDisplay.setDirections({{routes:[]}})
                map.setCenter(mylatlng);
            }}
        }});
    }}
    calcRoute();
        </script>
    """.format(api_key,waypoint,initial,final)
    html(pureHTML,height=500)




def selector(choose):
    c3.execute('SELECT DISTINCT lat,lon FROM onlinetable WHERE username = "{}"'.format(choose))
    data = c3.fetchall()
    return data
def getCurrentLocation():
    return ([lat,lon])
# Security
#passlib,hashlib,bcrypt,scrypt
import hashlib
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()
def check_hashes(password,hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False
# DB Management for normal users
import sqlite3 
conn = sqlite3.connect('user.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username,password):
    c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
    conn.commit()

def login_user(username,password):
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
    data = c.fetchall()
    return data


def view_all_users():
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
    return data

#DB management for autoricksaw owners
conn2 = sqlite3.connect('auto.db')
c2 = conn2.cursor()
# DB  Functions
def create_usertable2():
    c2.execute('CREATE TABLE IF NOT EXISTS autotable(username TEXT,password TEXT,phoneNo TEXT)')


def fetchPhoneNumber():
    c2.execute('SELECT username,phoneNo from autotable')
    data = c2.fetchall()
    return data

def add_userdata2(username,password,phoneNo):
    c2.execute('INSERT INTO autotable(username,password,phoneNo) VALUES (?,?,?)',(username,password,phoneNo))
    conn2.commit()

def login_user2(username,password):
    c2.execute('SELECT * FROM autotable WHERE username =? AND password = ?',(username,password))
    data = c2.fetchall()
    return data


def view_all_users2():
    c2.execute('SELECT * FROM autotable')
    data = c2.fetchall()
    return data

#DB management for online Users
conn3 = sqlite3.connect('online.db')
c3 = conn3.cursor()
# DB  Functions
def create_usertable3():
    conn3.execute('CREATE TABLE IF NOT EXISTS onlinetable(username TEXT,password TEXT,lat TEX,lon TEXT)')


def add_userdata3(username,password,lat,lon):
    c3.execute('INSERT INTO onlinetable(username,password,lat,lon) VALUES (?,?,?,?)',(username,password,lat,lon))
    conn3.commit()

def view_all_users3():
    c3.execute('SELECT username,lat,lon FROM onlinetable')
    data = c3.fetchall()
    return data

def go_offline(username):
    c3.execute('DELETE FROM onlinetable WHERE username = ?',(username))
    data =  c3.fetchall()
    return data
def main():
    """Easy Way"""

    st.title("Easy Way")
    menu = ["Home","Login As User","Login As Autoricksaw","SignUp","SignUp As Autoricksaw "]
    choice = st.sidebar.selectbox("Menu",menu)
    if choice == "Home":
        st.subheader("Home")
        # data = get_geolocation()
        st_lottie(
            lottie_arrow,
            height = 200,
            width = 600
        )
        col1,col2,col3 = st.columns(3)
        with col1:
            st_lottie(
                lottie_rickshaw,
                height = 200,
                width = 200
            )
        with col2:
            st_lottie(
                lottie_city1,
                height = 200,
                width = 200
            )
        with col3:
            st_lottie(
                lottie_city2,
                height = 200,
                width = 200
            )


    elif choice == "Login As User":
        col1 ,col2 = st.columns(2)
        with col1:
            st.subheader("Login Section")
        with col2:
            st_lottie(
                lottie_login,
                height = 300,
                width = 300
            )
        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password",type='password')
        if st.sidebar.checkbox("Login-Logout"):
            create_usertable()
            hashed_pswd = make_hashes(password)
            result = login_user(username,check_hashes(password,hashed_pswd))
            if result:
                col1,col2 = st.columns(2)
                with col1:
                    st.success("Logged In as {}".format(username))
                task = st.selectbox("Task",["Get Nearby Hubs","Get Path","Go Online","Reserve Auto"])
                if task == "Get Nearby Hubs":
                    st.subheader("Add Your Post")
                    try:
                        lat,lon=getCurrentLocation()
                    except TypeError:
                        pass
                    btn_2 = st.button("Send Location")
                    if btn_2:
                        temp_df = hub_finder(hub_data,float(lon),float(lat))
                        st.dataframe(temp_df)
                elif task == "Get Path":
                    initial = st.selectbox("Mark Current Position ",R1)
                    if initial == "OTHER OPTIONS":
                        initial = st.text_input("Current Position Here :")
                    final = st.selectbox("Mark Destination ",R2)
                    if final == "OTHER OPTIONS....":
                        final = st.text_input("Custom Destination Here :")
                    btn = st.button('Search')
                    data = route.locator(initial,final)
                    waypoint = wayPoints.wayPoints(data)
                    if btn:
                        statsInKM = fetchUserStats(initial,final)
                        km=float(statsInKM.split()[0])
                        cost=str(int(np.ceil(km/3)*10))+" INR"
                        st.write("#### The Estimated Cost is About "+cost)
                        if data == []:
                            drawMap(initial,final)
                        else:
                            drawMapWayPoints(initial,final,waypoint)
                elif task == "Go Online":
                    st.subheader("Your Location Will Be Shared With Nearby Autorickshaw")
                    create_usertable3()
                    try:
                        lat,lon = getCurrentLocation()
                        btn = st.button("Send Location")
                        if btn:
                            st.success("### Location Sent Successfully!")
                            add_userdata3(username,password,lat,lon)
                    except TypeError:
                        st.warning("Please Share Location First")
                elif task == "Reserve Auto":
                    initial = st.text_input("Enter Your Location")
                    final = st.text_input("Enter your Destination")
                    btn = st.button('Search')
                    if btn:
                        statsInKM = fetchUserStats(initial,final)
                        km=float(statsInKM.split()[0])
                        cost=str(int(np.ceil(km/3)*10))+" INR"
                        st.write("#### The Estimated Cost is About "+cost)
                        drawMap(initial,final)
                        data = fetchPhoneNumber()
                        st.dataframe(pd.DataFrame(data,columns=["driver","phone"]))

            else:
                st.warning("Incorrect Username/Password")
    elif choice == "Login As Autoricksaw":
        col1 ,col2 = st.columns(2)
        with col1:
            st.subheader("Login Section")
        with col2:
            st_lottie(
                lottie_driver,
                height = 400,
                width = 400
            )
        username = st.sidebar.text_input("Auto-Owner Name")
        password = st.sidebar.text_input("Password",type='password')
        if st.sidebar.checkbox("Login/Logout"):
            create_usertable2()
            hashed_pswd = make_hashes(password)
            result = login_user2(username,check_hashes(password,hashed_pswd))
            if result:
                st.success("Logged In as {}".format(username))
                task = st.selectbox("Task",["See Online Users"])
                if task == "See Online Users":
                    st.subheader("Online Users")
                    user_result = view_all_users3()
                    clean_db=pd.DataFrame(user_result,columns=["Username","lon","lat"])
                    data_username = list(set(clean_db["Username"].values.tolist()))
                    choosed = st.selectbox("You Selected: ",data_username)
                    btn = st.button("Submit")
                    if btn:
                        x = selector(choosed)
                        lat_ln = pd.DataFrame(x,columns=["lon","lat"])
                        lat_ln_str = str(lat_ln["lon"].values.tolist()[0])+","+str(lat_ln["lat"].values.tolist()[0])
                        loc = getCurrentLocation()
                        drawMap(loc[0]+","+loc[1],lat_ln_str)
                        fetchUserStats(loc[0]+","+loc[1],lat_ln_str)
            else:
                st.warning("Incorrect Username/Password")
    elif choice == "SignUp":
        st.subheader("Create New Account(USER)")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password",type='password')
        if st.button("Signup"):
            
            st_lottie(
                lottie_register,
                height = 400,
                width = 400
            )
            create_usertable()
            add_userdata(new_user,make_hashes(new_password))
            st.success("You have successfully created a valid Account")
            st.info("Go to Login Menu to login")
    elif choice == "SignUp As Autoricksaw ":
        st.subheader("Create New Account(AutoRickshaw)")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password",type='password')
        new_phoneNo = st.text_input("PhoneNumber")
        if st.button("Signup"):
            
            st_lottie(
                lottie_register,
                height = 400,
                width = 400
            )
            create_usertable2()
            add_userdata2(new_user,make_hashes(new_password),new_phoneNo)
            st.success("You have successfully created a valid Account")
            st.info("Go to Login Menu to login")
main()
