import streamlit as st
import pandas as pd
import numpy as np
from ydata_profiling import ProfileReport
import missingno as msno
import matplotlib.pyplot as plt
import streamlit_extras
import Utils.Utils as u

u.init_page("Encodage_Standardisation")

def Encodage_Standardisation():

    st.title('Encodage et Standardisation des données')

    