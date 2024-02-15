import streamlit as st
import pandas as pd

def upload_file():
    st.file_uploader(label="Mettez votre CSV",type="csv",accept_multiple_files=False)

upload_file()