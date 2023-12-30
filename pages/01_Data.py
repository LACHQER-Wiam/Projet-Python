import streamlit as st 
import pandas as pd
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px

from Home import DPE_data, DPE_data_brt, chosen_variables
import fetchdata 
import eda

st.subheader('Import de données et premières manipulations')
st.markdown('#### Mise en place de la base de données exploitable.\n L\'objectif est de selectionner et de modifier certaines variables afin qu\'elles puissent etre utilisées efficacement dans nos analyses.')
st.write("**Pour avoir une description d'une variable vous pouvez la sélectionner dans la liste déroulante :** ")
selected_option = st.selectbox("Liste des varibles", chosen_variables)
desc_variables = pd.read_excel('DATA/DPE_data_descrption.xlsx')

st.write(f"Vous avez sélectionné *{selected_option}*, \n",
        f"description : **:blue[{desc_variables[desc_variables['Nom_champ'] == selected_option]['Description'].values[0]}]**")
# Importataion des données 

# Affichage du tableau brut
st.write("Nous avons réalisé un outil qui permet d'extraire les données de la base de données de manière rapide et modulaire depuis l'API de l'Ademe en Open Access. cela nous permet de choisir le nombre d'observations et les variables")
st.write("**Voici un premier aperçu des données 'brutes' à notre dispostion :**")
nb_obs, nb_col = DPE_data_brt.shape
st.dataframe(DPE_data_brt.head(5)) 
st.caption(f'Données relatives au dépenses énergétiques des logements en France. Nombre d\'observation : **{nb_obs}** et nombre de variables : **{nb_col}**.')
st.write('L\'enjeux à présent et de manipuler les données, observer et rectifier les erreurs, supprimer les variables incomplete ou inutilisables.')
st.write('Pour ce faire, nous utilisons dans un premier temps une fonction que nous avons developpé afin d\'effectuer un audit rapides des variables de notres base')
st.write( 'Voici un audit rapide des données afin de mettre en évidence les problème de données de notre base : ')

tab_recap_NA = eda.create_unique(DPE_data_brt) 
st.dataframe(tab_recap_NA)

#-------------------------------------------------------------------------------------------------------
st.write('###### Pre-traitement des données :') 
st.dataframe(DPE_data.head(5))
nb_obs, nb_col = DPE_data.shape
st.caption(f'Nombre d\'obsrevations : **{nb_obs}** et nombre de colonnes : **{nb_col}**')


#-------------------------------------------------------------------------------------------------------
st.write('### Analyse descriptive de la base de donnée : ')
st.write("## Quels sont les types d'énergies utilisées en France ?  ")



col1, col2 = st.columns(2)

def pieplot_chauffage_interact(bd_dpe):

    comptage_type_chauffage = bd_dpe['Type_énergie_principale_chauffage'].value_counts()
    comptage_type_ECS = bd_dpe['Type_énergie_principale_ECS'].value_counts()

    pourcentages_chauffage = (comptage_type_chauffage / len(bd_dpe)) * 100
    pourcentages_ECS = (comptage_type_ECS / len(bd_dpe)) * 100

    seuil = 3
    autres_chauffage = pourcentages_chauffage[pourcentages_chauffage < seuil].sum()
    autres_ECS = pourcentages_ECS[pourcentages_ECS < seuil].sum()

    nouveaux_pourcentages_chauffage = pourcentages_chauffage[pourcentages_chauffage >= seuil]
    nouveaux_pourcentages_chauffage['Autres'] = autres_chauffage

    nouveaux_pourcentages_ECS = pourcentages_ECS[pourcentages_ECS >= seuil]
    nouveaux_pourcentages_ECS['Autres'] = autres_ECS

    # Graphiques
    fig_chauffage = go.Figure(go.Pie(labels=nouveaux_pourcentages_chauffage.index,
                                    values=nouveaux_pourcentages_chauffage,
                                    marker=dict(colors=px.colors.qualitative.Pastel1),
                                    hole=0.3,
                                    textinfo='label+percent'))

    fig_ECS = go.Figure(go.Pie(labels=nouveaux_pourcentages_ECS.index,
                            values=nouveaux_pourcentages_ECS,
                            marker=dict(colors=px.colors.qualitative.Pastel1),
                            hole=0.3,
                            textinfo='label+percent'))

    # Mise en page
    fig_chauffage.update_layout(title_text='Répartition types d\'énergies pour chauffage des logements', width = 1000)
    fig_ECS.update_layout(title_text='Répartition types d\'énergies pour ECS des logements', width = 1000)

    return (fig_chauffage, fig_ECS)


def barplot_chauffage_inter(bd_dpe): 

    # Comptage pour 'Type_énergie_principale_chauffage'
    comptage_type_chauffage = bd_dpe['Type_énergie_principale_chauffage'].value_counts()

    # Créer une figure interactive Plotly pour 'Type_énergie_principale_chauffage'
    fig_chauffage = px.bar(
        x=comptage_type_chauffage.index,
        y=comptage_type_chauffage,
        color=comptage_type_chauffage.index,
        labels={'x': 'Types d\'énergies', 'y': 'Nombre d\'occurrences'},
        title='Répartition des types d\'énergies pour chauffage'
    )
    fig_chauffage.update_layout(xaxis=dict(tickangle=-20, tickmode='array', tickvals=list(comptage_type_chauffage.index)))

    # Comptage pour 'type_principale_energie_ECS'
    comptage_type_ECS = bd_dpe['Type_énergie_principale_ECS'].value_counts()

    # Créer une figure interactive Plotly pour 'type_principale_energie_ECS'
    fig_ECS = px.bar(
        x=comptage_type_ECS.index,
        y=comptage_type_ECS,
        color=comptage_type_ECS.index,
        labels={'x': 'Types d\'énergies', 'y': 'Nombre d\'occurrences'},
        title='Répartition des types d\'énergies pour ECS'
    )
    fig_ECS.update_layout(xaxis=dict(tickangle=-45, tickmode='array', tickvals=list(comptage_type_ECS.index)))

    return (fig_chauffage, fig_ECS)


tab1_chauffage, tab2_chauffage = st.tabs(["📈 Pieplot", "📊 Barplot"]) # POUR ENERGIE CHUAFFAGE

tab1_chauffage.subheader("Un onglet sur l'énergie de chauffage (Pieplot)")
tab1_chauffage.plotly_chart(pieplot_chauffage_interact(DPE_data)[0])
tab2_chauffage.subheader("Un onglet sur l'énergie de chauffage (Barplot)")
tab2_chauffage.plotly_chart(barplot_chauffage_inter(DPE_data)[0])


tab1_ECS, tab2_ECS = st.tabs(["📊 Barplot","📈 Pieplot"]) # POUR ENERGIE ECS

tab1_ECS.subheader("Un onglet sur l'énergie ECS (Barplot)")
tab1_ECS.plotly_chart(barplot_chauffage_inter(DPE_data)[1])
tab2_ECS.subheader("Un onglet sur l'énergie ECS (Pieplot)")
tab2_ECS.plotly_chart(pieplot_chauffage_interact(DPE_data)[1])
