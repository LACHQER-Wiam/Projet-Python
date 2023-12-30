import streamlit as st
import fetchdata
import eda
import pandas as pd
import folium
from streamlit_folium import folium_static

def main():
    st.header('HOME PAGE')
    col1, col2 = st.columns([2, 1])
    col1.title ('Data analysis and modeling of the consumption of homes in France')
    col2.image('images/LOGO-ENSAE.png')
    st.write('Membres du groupe : \n - Wiam LACHQER , Amine RAZIG , Julien BOUDIER')
    st.write('Ce projet Python a été créé dans le but de fournir des visualisations variées des données et de mettre en place un simulateur de Diagnostic de Performance Energétique (DPE) à partir de la base de données de l\'ADEME (Agence de la Transition Écologique).\n ## Objectifs du Projet :\n 1. **Visualisations de Données :** Le projet propose différentes visualisations des données issues de la base de l\'ADEME. Ces visualisations permettent une compréhension approfondie des caractéristiques énergétiques des logements.')
    st.write('2. **Simulateur de DPE :** Un simulateur de DPE a été développé en utilisant les données de l\'ADEME. Ce simulateur permet d\'estimer la performance énergétique d\'un logement en fonction de divers paramètres.')
    st.write('Ce projet contient plusieurs parties :\n - L\'importation des données, le nettoyage et des visualisations de données.\n - L\'analyse géographique de la répartition des logements ne france.\n - La création de modèles prédictifs.')
    st.write('##### Source des données : https://www.data.gouv.fr/fr/datasets/dpe-logements-existants-depuis-juillet-2021/')

if __name__ == '__main__':
    main()

chosen_variables=['N°DPE',
                  'Etiquette_GES',
                  'Etiquette_DPE',
                  'Année_construction',
                  'Type_bâtiment',
                  'Période_construction',
                  'Hauteur_sous-plafond',
                  'Surface_habitable_logement',
                  'Classe_altitude',
                  'Zone_climatique_',
                  'Nom__commune_(BAN)',
                  'N°_département_(BAN)',
                  'Coordonnée_cartographique_X_(BAN)',     
                  'Coordonnée_cartographique_Y_(BAN)',
                  'N°_région_(BAN)',
                  'Conso_5_usages_é_finale',
                  'Conso_5_usages/m²_é_finale',
                  'Conso_chauffage_é_finale',
                  'Emission_GES_5_usages',
                  'Emission_GES_5_usages_par_m²',
                  'Conso_5_usages_é_finale_énergie_n°1',
                  'Coût_total_5_usages_énergie_n°1',
                  'Conso_5_usages_é_finale_énergie_n°2',
                  'Coût_total_5_usages_énergie_n°2',
                  'Conso_5_usages_é_finale_énergie_n°3',
                  'Coût_total_5_usages_énergie_n°3',
                  'Coût_total_5_usages',
                  'Qualité_isolation_enveloppe',
                  'Qualité_isolation_menuiseries',
                  'Qualité_isolation_murs',
                  'Qualité_isolation_plancher_bas',
                  'Type_énergie_principale_chauffage',
                  'Type_énergie_principale_ECS',
                  'Type_énergie_n°1',
                  'Type_installation_ECS',
                  'Type_installation_solaire',
                  'Surface_climatisée',               
                  'Type_ventilation']


# Affichage du tableau brut : 
DPE_data_brt = fetchdata.get_dpe(chosen_variables, size =10000)

# Creation du tableau nettoyé : 
DPE_data = fetchdata.get_dpe(chosen_variables, size = 10000)
#-------------------------------------------------------------------------------------------------------
# Suppression des lignes dans lesquelles la surface habitable est non renseignée
DPE_data=DPE_data[DPE_data["Surface_habitable_logement"].notna()]
DPE_data=DPE_data[DPE_data["Qualité_isolation_plancher_bas"].notna()]
DPE_data["Type_énergie_principale_ECS"].fillna(DPE_data["Type_énergie_n°1"], inplace = True)
DPE_data["Type_énergie_principale_chauffage"].fillna(DPE_data["Type_énergie_n°1"], inplace = True)
DPE_data['Type_énergie_principale_chauffage'] = DPE_data['Type_énergie_principale_chauffage'].replace(['Bois – Bûches','Bois – Granulés (pellets) ou briquettes', 'Bois – Plaquettes d’industrie', 'Bois – Plaquettes forestières'], 'Bois')
DPE_data['Type_énergie_principale_ECS'] = DPE_data['Type_énergie_principale_ECS'].replace(['Bois – Bûches','Bois – Granulés (pellets) ou briquettes', 'Bois – Plaquettes d’industrie', 'Bois – Plaquettes forestières'], 'Bois')

# La simulation portera uniquement sur les maisons et les appartements, on supprime les immeubles
DPE_data=DPE_data[DPE_data["Type_bâtiment"]!="immeuble"]
DPE_data = pd.get_dummies(DPE_data, columns=['Type_bâtiment'])

# NETTOYAGE GENERALE ( valeurs manquantes)
DPE_data = eda.clean_na(DPE_data)
DPE_data = DPE_data.dropna() # on termine par suprimmer les lignes avec des valeusr manquantes 


def pieplot_chauffages (bd_dpe):
    comptage_type_energie = bd_dpe['Type_énergie_principale_chauffage'].value_counts()
    pourcentages_chauffage = (comptage_type_chauffage / len(bd_dpe)) * 100
    pourcentages_ECS = (comptage_type_ECS / len(bd_dpe)) * 100
    seuil = 3
    autres_chauffage = pourcentages_chauffage[pourcentages_chauffage < seuil].sum()
    autres_ECS = pourcentages_ECS[pourcentages_ECS < seuil].sum()

    nouveaux_pourcentages_chauffage = pourcentages_chauffage[pourcentages_chauffage >= seuil]
    nouveaux_pourcentages_chauffage['Autres'] = autres_chauffage
    nouveaux_pourcentages_ECS = pourcentages_ECS[pourcentages_ECS >= seuil]
    nouveaux_pourcentages_ECS['Autres'] = autres_ECS

    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(14, 6))
    # Graphique pour le chauffage
    axes[0].pie(x=nouveaux_pourcentages_chauffage, labels=nouveaux_pourcentages_chauffage.index, startangle=45,
                colors=sns.color_palette('pastel', len(nouveaux_pourcentages_chauffage)), autopct='%1.1f%%')
    axes[0].set_title('Répartition types d\'énergies pour chauffage des logements')

    # Graphique pour l'ECS
    axes[1].pie(x=nouveaux_pourcentages_ECS, labels=nouveaux_pourcentages_ECS.index, startangle=45,
                colors=sns.color_palette('pastel', len(nouveaux_pourcentages_ECS)), autopct='%1.1f%%')
    axes[1].set_title('Répartition types d\'énergies pour ECS des logements')

    plt.show()

def barplot_chauffages(bd_dpe): 
    # Comptage pour 'Type_énergie_principale_chauffage'
    comptage_type_chauffage = bd_dpe['Type_énergie_principale_chauffage'].value_counts()
    colors_chauffage = sns.color_palette('Set1')[0:len(comptage_type_chauffage)]

    # Comptage pour 'type_principale_energie_ECS'
    comptage_type_ECS = bd_dpe['Type_énergie_principale_ECS'].value_counts()
    colors_ECS = sns.color_palette('Set2')[0:len(comptage_type_ECS)]

    plt.figure(figsize=(10, 6))
    bar_width = 0.35
    index = range(len(comptage_type_chauffage))
    # Barres pour 'Type_énergie_principale_chauffage'
    plt.bar(index, comptage_type_chauffage, bar_width, color=colors_chauffage, label='Chauffage')
    # Barres pour 'type_principale_energie_ECS'
    plt.bar(index, comptage_type_ECS, bar_width, color=colors_ECS, label='ECS', alpha=0.7)

    # Ajout des labels, titres, et légende
    plt.xlabel('Types d\'énergies')
    plt.ylabel('Nombre d\'occurrences')
    plt.title('Répartition des types d\'énergies pour chauffage et ECS des logements')
    plt.xticks(index, comptage_type_chauffage.index)
    plt.legend()

    # Affichage du graphique
    plt.show()

