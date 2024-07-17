import pandas as pd
import streamlit as st
import numpy as np
from PIL import Image
import boto3
import os
from matplotlib import pyplot as plt
import plotly.graph_objects as go
import random
import boto3
import shutil

# log text
my_file = open("./target_stream/logtext/outputlog.txt", "r")
data = my_file.read()
data_lines = data.split("\n")
data_logs = [x.split(" ")[:-1] for x in data_lines[:-1]]
data_logs_df = pd.DataFrame(data=data_logs, columns=["ActionID", "Action", "Date", "Time"])
data_logs_df["Date"] = data_logs_df["Date"]+" "+data_logs_df["Time"]
del data_logs_df["Time"]

# all images
images_dir = os.listdir("./target_stream/logimage/")


# analysis
awake_df = data_logs_df[data_logs_df["Action"]=="awake"]
drowsy_df = data_logs_df[data_logs_df["Action"]=="drowsy"]

ts_time = []
ts_awake_increament = []
ts_drowsy_increament = []

awake, drowsy = 0, 0
for aid, act, dat in zip(data_logs_df["ActionID"], data_logs_df["Action"], data_logs_df["Date"]):

    if act=="awake":
        awake+=1
        ts_awake_increament.append(awake)
        ts_drowsy_increament.append(drowsy)
        ts_time.append(dat)
    elif act=="drowsy":
        drowsy+=1
        ts_drowsy_increament.append(drowsy)
        ts_awake_increament.append(awake)
        ts_time.append(dat)

# plots
fig_bar = go.Figure([go.Bar(x=["awake", "drowsy"], y=[len(awake_df), len(drowsy_df)])])

fig = go.Figure()
fig.add_trace(go.Scatter(x=ts_time, y=ts_awake_increament, mode="lines+markers", name="Awake - Ts"))
fig.add_trace(go.Scatter(x=ts_time, y=ts_drowsy_increament, mode="lines+markers", name = "Drowsy - Ts"))
fig.update_layout(title="Time Series Activity Profile", xaxis_title="Date & Time", yaxis_title="Activity Profile")

# sidebar
st.sidebar.markdown("<h1 style='text-align: center; color: blue;'>Driver Monitoring System</h1>", unsafe_allow_html=True)
st.sidebar.markdown("<h3 style='text-align: center; color: purple;'>User Profile</h3>", unsafe_allow_html=True)
st.sidebar.image("./target_stream/logimage/"+random.choice(images_dir), caption="User")
st.sidebar.markdown("<h3 style='text-align: center; color: green;'>Activity Distribution</h3>", unsafe_allow_html=True)
st.sidebar.plotly_chart(fig_bar, use_container_width=True)




# main
st.title("Validation platform")
st.markdown("<h3 style=color: purple'>Time Series Activity Profile</h3>", unsafe_allow_html=True)
st.markdown("In the time series activity profile, we determine if the user is awake or in a drowsy state by observing the time series activity. \n"
            "If the awake activity profile (blue) of the user is higher than the drowsiness profile, that indicates the user is in an awake state. \n"
            "However, if the drowsiness activity profile exceeds the awake profile, that indicates the user is in a drowsy state for a \n"
            "longer period compared to the awake state.")
st.plotly_chart(fig, use_container_width=True)

# dataframe
st.markdown("<h3 style=color: purple'>Activity Logs</h3>", unsafe_allow_html=True)
st.markdown("In activity logs, we have specific awake/drowsiness action states and their corresponding timestamps and log snapshots. \n"
            "Using these logs, we can validate if the real-time action states are valid by using the 'ActionID' to search the relevant log image. \n"
            "By performing these validations, we can identify the false positive rates.")
ldf, rdf = st.columns(2)
ldf.markdown("Awake Logs")
ldf.dataframe(awake_df)
rdf.markdown("Drowsy Logs")
rdf.dataframe(drowsy_df)

# check logs valid
st.markdown("<h3 style=color: purple'>Validate Actions</h3>", unsafe_allow_html=True)
st.markdown("Use the ActionID from the above dataframes to validate the detection")
id_req = st.text_input("Action ID", "1")
subm = st.button("Submit")

if subm:
    cls = list(data_logs_df[data_logs_df["ActionID"]==id_req]["Action"])[0]
    st.markdown("**Detection Class -** "+" "+"**"+cls+"**")
    st.image("./target_stream/logimage/"+id_req+".jpg", caption="User")


