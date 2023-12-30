import streamlit as st 
from Home import DPE_data
import eda


st.subheader("Création d'un modèle de prédiction de consommation")


fig1 = eda.create_energy_plots(DPE_data, 'Conso_5_usages/m²_é_finale', 'Emission_GES_5_usages_par_m²')
fig2 = eda.create_energy_plots(DPE_data,  'Emission_GES_5_usages_par_m²','Conso_5_usages/m²_é_finale')

st.write ('Analyse inivarié de la variable : Conso_5_usages/m²_é_finale')
st.pyplot(fig1)


st.write ('Analyse inivarié de la variable : Emission_GES_5_usages_par_m²')
st.pyplot(fig2)