
import streamlit as st 
from  streamlit_folium import st_folium, folium_static
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import cartiflette.s3 as s3
import folium
import contextily as ctx

from Home import DPE_data
st.set_option('deprecation.showPyplotGlobalUse', False)


st.header('**Graphic and cartographic representation of data**')

st.write("""
In this section, we will explore the data from a geographical perspective. We will generate multiple maps at different scales to highlight various variables of interest.
""")

# Conversion du dataframe en géodataframe pour l'ensmeble des represenation cartographique + supression val abérantes : 
def create_gdf(DPE_data):
    gdf = gpd.GeoDataFrame(DPE_data, geometry=gpd.points_from_xy(DPE_data['Coordonnée_cartographique_X_(BAN)'], DPE_data['Coordonnée_cartographique_Y_(BAN)']), crs='EPSG:2154')

    # Supprimer les points spécifiques
    x_point_to_remove = 700503.45
    y_point_to_remove = 1635446.01
    gdf = gdf.drop(gdf[(gdf['Coordonnée_cartographique_X_(BAN)'] == x_point_to_remove) & (gdf['Coordonnée_cartographique_Y_(BAN)'] == y_point_to_remove)].index)
    return gdf

gdf = create_gdf(DPE_data)

def carte_DPE_monde (gdf) : 
        # On commence part telecharger le fond de carte 
        france = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

        #même référentiel spatial
        gdf= gdf.to_crs(france.crs)


        # Tracer la carte
        fig, ax = plt.subplots(figsize=(10, 8))
        france.plot(ax=ax, color='lightgray')
        gdf.plot(ax=ax, color='red', marker='o', markersize=5)
        plt.title('Carte de la France avec des points géolocalisés')
        plt.xlabel('Coordonnées X (Lambert 93)')
        plt.ylabel('Coordonnées Y (Lambert 93)')
        return fig

st.pyplot(carte_DPE_monde (gdf ))


def create_folium_map(gdf):
    m = folium.Map(location=[46.6031, 1.8883], zoom_start=6)
    folium.GeoJson(gdf).add_to(m)
    return m
    
# Afficher la carte interactive dans Streamlit
st.title("Carte Interactive")
if st.button("Afficher la carte interactive 🪄 "):
    st.text("Chargement en cours...🔄")
    m = create_folium_map(gdf)
    st.write("Cliquez et faites défiler pour explorer la carte.")
    folium_static(m)
    st.text("Chargement terminé!")   


# Visulatisations rapides des données sur une carte de la france 
col1, col2 = st.columns(2)

#====================================================================================================================
#### 1ere  carte de la france seulement avce les points de la base de données : 

# carte de la france avec legende en fonction d'une variable d'interet : 
def carte_france (gdf, selected_var = 'Conso_5_usages/m²_é_finale'):
        fig,ax = plt.subplots(figsize=(13, 10))
        gdf.to_crs(3857).plot(column =selected_var,cmap='viridis',ax=ax ,alpha = 0.4, zorder=2, legend = True)

        #shp_communes.to_crs(3857).plot(ax = ax, zorder=1, edgecolor = "black", facecolor="none", color = None)
        ctx.add_basemap(ax, source = ctx.providers.OpenStreetMap.Mapnik) # fond de carte
        plt.title(f'Carte de la france ({selected_var})')
        return fig

#st.markdown("<h1 style='text-align: center;'>Quelle est votre variable d'intérêt ?</h1>", unsafe_allow_html=True)
st.markdown("# Cartes de la Fance 🗺️")
st.markdown("### Quelle sont vos variables d'intérêt ?")

col1, col2 = st.columns(2)

choix1 = col1.radio(
    'Sélectionnez votre variable d\'intérêt' , 
    ['Conso_5_usages/m²_é_finale','Emission_GES_5_usages_par_m²','Coût_total_5_usages','Surface_habitable_logement'], 
    captions = ["consommation d'énergie primaire totale rapportée à la surface (kWhep/m²/an)",
                "estimation GES totale 5 usages rapportée au m² (ecs/chauffage/climatisation/eclairage/auxiliaires)(kgCO2/m2/an)",
                "coût totale 5 usages (ecs/chauffage/climatisation/eclairage/auxiliaires)(€)"]
)
st.pyplot(carte_france (gdf, choix1))

#====================================================================================================================
#### 2nde carte de la France par département : 

# Import des départements : 
deps = gpd.read_file('DATA/departements.geojson')
gdf_dep = deps.merge(gdf, left_on = 'code', right_on = 'N°_département_(BAN)')
gdf_dep = gpd.GeoDataFrame(gdf_dep, geometry = 'geometry_x')

def Carte_France_departements (geodf,var):
    '''
    args => geodf est un geodataframe avec les polygone des régions en géométries 
         => var : le nom de la varaible d'intéret (numérique) ex : 'Qualité_isolation_murs' ou 'Conso_5_usages/m²_é_finale'
    '''
    geodf.plot(figsize = (13,5), column = var, legend = True)
    plt.title(f"Départements francais ({var})")

choix2 = col2.radio(
    'Sélectionnez votre variable d\'intérêt' , 
    ['Conso_5_usages/m²_é_finale','Emission_GES_5_usages_par_m²','Coût_total_5_usages','Qualité_isolation_murs'],
    captions = ["consommation d'énergie primaire totale rapportée à la surface (kWhep/m²/an)",
                "estimation GES totale 5 usages rapportée au m² (ecs/chauffage/climatisation/eclairage/auxiliaires)(kgCO2/m2/an)",
                "coût totale 5 usages (ecs/chauffage/climatisation/eclairage/auxiliaires)(€)"]
)

st.pyplot(Carte_France_departements(gdf_dep,choix2 ))

#====================================================================================================================
#### 3ème carte de la France par sélection de départements : 
st.markdown("# Cartes départementales ")
st.write("###Dans un second temps, apres avoir representé la France de manière globale nous nous interessons au découpage départemental et à la répartition des logements de notre base dans des zones spécifiquement sélectionnées")

st.markdown("### Quelle sont vos variables d'intérêt ?")

def carte_selection_dep (gdf_dep, values, selected_var = 'Conso_5_usages/m²_é_finale') : 
    '''
    return a map focus on the departemenst selected
    '''
    gdf_zone = gdf_dep[gdf_dep['code'].isin(values)]

    sorted(gdf_zone['code'].unique())
    fig, ax = plt.subplots ( figsize= (10,10))
    gdf_zone.to_crs(3857).plot(ax=ax, zorder=1 ,column = selected_var, legend = True, edgecolor = "black", linewidth=0.5)
    gdf_zone['geometry_y'].to_crs(3857).plot(ax =ax, color = 'blue',alpha = 0.5, zorder=3)

    #shp_communes.to_crs(3857).boundary.plot(ax=ax, zorder=1 , edgecolor = "black", linewidth=0.5, facecolor="none",color = None)
    ctx.add_basemap(ax, source = ctx.providers.OpenStreetMap.Mapnik, zorder=2, alpha = 0.7)
    ax.set_axis_off()
    return fig 


interest_var = st.radio(
    'Sélectionnez votre variable d\'intérêt' , 
    ['Conso_5_usages/m²_é_finale','Emission_GES_5_usages_par_m²','Coût_total_5_usages','Qualité_isolation_murs']
)

codes_dep = st.multiselect(
    'Quels départemnts souhaitez vous afficher ?',
    [str(x) for x in range(1, 96)],
    default = ['75', '93', '92', '94'],
    placeholder="Choisissez une option")

st.pyplot(carte_selection_dep (gdf_dep, codes_dep,interest_var))
st.caption(f"Carte de la sélection de départements : {codes_dep}; Variable sélectionnée : ({interest_var})")

#====================================================================================================================
st.markdown("# Cartes régionales ")
st.write("### Dans un second temps, apres avoir representé la France de manière globale nous nous interessons au découpage départemental et à la répartition des logements de notre base dans des zones spécifiquement sélectionnées")


code_regions_france = pd.read_csv('DATA/code_region_france.csv', delimiter = ';')
code_regions_france['REG'] = code_regions_france['REG'].astype(str)
gdf = gdf.merge(code_regions_france, left_on='N°_région_(BAN)', right_on='REG')

gdf = deps.merge(gdf, left_on = 'code', right_on = 'N°_département_(BAN)')
gdf = gpd.GeoDataFrame(gdf, geometry = 'geometry_x')

def carte_region (gdf, region_choisie, var='Conso_5_usages/m²_é_finale'):
    ''' /!\ le gdf doit contenir - les noms de regions
                                 - les numéros de département et leurs géométrie
    '''
    gdf_region = gdf[gdf['Nom_reg']== region_choisie]
    shp_communes = s3.download_vectorfile_url_all(
        crs = 4326,
        values = gdf_region['code'].unique(), #on obtiens tous les codes des département de la régions selectionnée
        borders="COMMUNE_ARRONDISSEMENT",
        vectorfile_format="topojson",
        filter_by="DEPARTEMENT",
        source="EXPRESS-COG-CARTO-TERRITOIRE",
        year=2022)

    #values = gdf['code'].unique()   on obtiens tous les codes des département de la régions selectionnée
    #gdf_paris = gdf_dep[gdf_dep['code'].isin(gdf['code'].unique())]

    #sorted(gdf_paris['code'].unique())
    #gdf_paris
    fig, ax = plt.subplots ( figsize= (10,10))
    gdf_region.to_crs(3857).plot(ax=ax ,column = 'Conso_5_usages/m²_é_finale', legend = True, edgecolor = "black", linewidth=0.5, zorder=2, alpha=0.5)
    gdf_region['geometry_y'].to_crs(3857).plot(ax =ax, marker='o', markersize=1, alpha=0.7,color = 'red', zorder=4)

    shp_communes.to_crs(3857).boundary.plot(ax=ax, zorder=3 , edgecolor = "black", linewidth=0.5, facecolor="none",color = None, alpha=0.5)
    ctx.add_basemap(ax, source = ctx.providers.OpenStreetMap.Mapnik, zorder=1, alpha = 1)
    plt.title (f"Carte de la région : {region_choisie}, (Conso/m²)")
    ax.set_axis_off()

if st.button("Afficher une carte régionale selon vos préferences ! "):
    
    region_choix = st.selectbox("Liste des régions", gdf['Nom_reg'].unique())
    st.text("Chargement en cours...🔄") 
    st.pyplot(carte_region(gdf, region_choix))

#====================================================================================================================

Noms_regions = pd.read_csv("DATA/anciennes-nouvelles-regions.csv", delimiter=';')
Noms_regions['Nouveau Code'] = Noms_regions['Nouveau Code'].astype(str)
DPE_data = DPE_data.merge(Noms_regions, left_on = 'N°_région_(BAN)', right_on= 'Nouveau Code').drop('Nouveau Code',  axis=1)

st.title('Graphiques de consommation par région')
import plotly.graph_objects as go
def graphiques_conso_reg(DPE_data):
    # Diagramme circulaire
    st.subheader('Répartition des logements par zone climatique')
    st.write("""
        La France compte 3 zones climatiques définies sur base des températures hivernales et estivales des régions qui les composent :

        - La zone climatique **H1** est la zone la plus étendue. C’est là que sont relevées les températures les plus froides. L’hiver y est long. Les pluies sont fréquentes. Elle couvre toute la moitié nord-est de la France et descend jusqu’à Lyon.

        - La zone climatique **H2** correspond au reste de la France, de la zone nord-ouest à sud-ouest, à l’exception du bassin méditerranéen. Les températures y sont plus douces et l’hiver moins marqué. Les pluies peuvent être importantes tout au long de l’année.

        - La zone climatique **H3** constitue une bande sur le pourtour méditerranéen du sud-est de la France. C’est la zone avec les températures les plus chaudes et un hiver très doux. Les pluies y sont rares et brèves. Elle englobe également les DOM-TOM.

        [Source](https://www.effy.fr/aide-energetique/zoom-sur-les-zones-climatiques-de-france)
        """)
    val_zone_climatique = DPE_data['Zone_climatique_'].value_counts().sort_index()
    colors = px.colors.sequential.Viridis[:len(val_zone_climatique)]
    fig1 = px.bar(val_zone_climatique, x=val_zone_climatique.index, y=val_zone_climatique.values, color=val_zone_climatique.index, color_discrete_sequence=colors)
    fig1.update_layout(title='Répartition des logements par zone climatique')
    st.plotly_chart(fig1)

    # Répartition des logements par région
    st.subheader('Répartition des logements par région')
    val_region = DPE_data['Nouveau Nom'].value_counts().sort_index()
    fig2 = px.bar(val_region, x=val_region.index, y=val_region.values, labels={'x':'Région', 'y':'Count'}, color=val_region.index)
    fig2.update_layout(title='Number of residences per regions.', xaxis_tickangle=-45)
    

    # Classement des régions par consommation
    st.subheader('Classement des régions par consommation')
    comptage_conso_region = DPE_data.groupby('Nouveau Nom')['Conso_5_usages_é_finale'].sum()
    fig3 = px.bar(comptage_conso_region, x=comptage_conso_region.index, y=comptage_conso_region.values, labels={'x':'Région', 'y':'Sum of consomation'}, color=comptage_conso_region.index)
    fig3.update_layout(title='Sum of consomation by Region', xaxis_tickangle=-45)
    
    tab1_nblogements, tab2_conso = st.tabs(["Répartition des logements par région", "Classement des régions par consommation"]) 
    tab1_nblogements.subheader("Répartition des logements par région ")
    tab1_nblogements.plotly_chart(fig2)
    tab2_conso.subheader("Classement des régions par consommation")
    tab2_conso.plotly_chart(fig3)

    # Consommation moyenne d'un logement par région
    st.subheader('Consommation moyenne d\'un logement par région')

    df_conso_regions = pd.merge(comptage_conso_region, val_region, on='Nouveau Nom')
    df_conso_regions['conso_moyenne'] = df_conso_regions['Conso_5_usages_é_finale'] / df_conso_regions['count']

    fig = go.Figure() #go.Scatterpolar pour créer un graphique radar
    fig.add_trace(go.Scatterpolar(r=df_conso_regions['conso_moyenne'],
                                    theta=df_conso_regions.index,
                                    fill='toself',
                                    line=dict(color='seagreen')))

    fig.update_layout( polar=dict(radialaxis=dict(visible=True)),
                       title='Radar Chart of Mean Consumption', height=600)

    st.plotly_chart(fig)

# Appel de la fonction
graphiques_conso_reg(DPE_data)

