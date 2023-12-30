import pandas as pd
import seaborn as sns
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler


def correlation(df):
    corr = df.corr()
    corr.style.background_gradient(cmap='coolwarm')
    return corr


def linreg_marg_dist(df,x,y):
    sns.set_theme(style="darkgrid")

    sns.jointplot(x=x, y=y, data=df,
                    kind="reg", truncate=False,
                    color="m", height=7,
                    scatter_kws={'alpha': 0.3})


def one_hot_encode(data, columns_to_encode):
    """
    Cette fonction encode des variables spécifiques.

    args : 
        => df (pd.Dataframe) : base de données
        => columns_to_encode (list) : liste des variables à encoder
    return : 
        => df(pd.Dataframe) : la base de données initiale avec des colonnes supplémentaires
    """
    return pd.get_dummies(data, columns=columns_to_encode, drop_first=True)


def label_encode(data, columns_to_encode):
    le = LabelEncoder()
    for column in columns_to_encode:
        data[column] = le.fit_transform(data[column])
    return data


def impute_missing_values(data, strategy='mean'):
    imputer = SimpleImputer(strategy=strategy)
    imputed_data = imputer.fit_transform(data)
    return pd.DataFrame(imputed_data, columns=data.columns)


def remove_outliers(data, contamination=0.01):
    model = IsolationForest(contamination=contamination, random_state=42)
    model.fit(data)
    outliers = model.predict(data)
    inliers_mask = outliers == 1
    cleaned_data = data[inliers_mask]
    return cleaned_data



# Tracer les boites à moustache de plusieurs variables
def boxplot(data, variables):
    fig, axes = plt.subplots(nrows=4, ncols=3, figsize=(15, 8))
    axes = axes.flatten()
    for i in range(len(variables)):
        sns.boxplot(x=data[variables[i]], ax=axes[i], color='skyblue')
        #axes[i].set_title(variables[i])
    # Masquer le subplot vide 
    if len(axes) > 9:
        for i in range(9, len(axes)):
            fig.delaxes(axes[i])
    plt.tight_layout()
    plt.show()


# Détecter des outliers
def Outliers(df, columns):
    outliers = pd.DataFrame(columns=['variable','nombre_val_aberrantes'])
    for column in columns:
        q1 = df[column].quantile(0.25)
        q3 = df[column].quantile(0.75)
        iqr = q3 - q1
        seuil_inf = q1 - 3.5 * iqr
        seuil_sup = q3 + 3.5 * iqr
        valeurs_aberrantes = df[(df[column] < seuil_inf) | (df[column] > seuil_sup)]
        outliers = pd.concat([outliers,pd.DataFrame([{'variable':column,'nombre_val_aberrantes':len(valeurs_aberrantes)}])] )
    return outliers



def remplacer_outliers(df,columns):
    for column in columns:
        q1 = df[column].quantile(0.25)
        q3 = df[column].quantile(0.75)
        iqr = q3 - q1
        if iqr>0:
            seuil_inf = q1 - 3.5 * iqr
            seuil_sup = q3 + 3.5 * iqr
            df.loc[df[column] < seuil_inf, column] = seuil_inf
            df.loc[df[column] > seuil_sup, column] = seuil_sup
    return (df)



# Standardisation
def standardisation (df, columns):
    scaler = StandardScaler()
    data_standardized = pd.DataFrame()
    data_standardized[columns]= scaler.fit_transform(df[columns])
    return data_standardized

def occurrence(df,column):
    occurrence = df[column].value_counts()
    return occurrence

################################################### GRAPHIQUES / 
import pandas as pd 
from sklearn.preprocessing import LabelEncoder
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import plotly.offline as pyo #permet d'afficher les graphes interactives direct dans le notebook 



def create_unique(df):
    """
    This function aims to explore the dataframe's composition. It's a usful function to show how many missing values each variable counts. 
    It is a general function adaptative with any panda dataframe. 

    args : 
        => df (pd.Dataframe) : the input data base
    return : 
        => df_unique (pd.Dataframe) : a data frame of all the input variables and their composition in term of missing values. \n

                                     'Column_name'  'Data_type'  'Number_of_unique'  'Number_of_missing'  'Unique_values' \n

                            Var1        ---             ---             ---                 ----                ---\n
                            Var2        ---             ---             ---                 ---                 ---\n
                            ...\n
                            Varn        ---             ---             ---                 ---                 ---\n
    """
        
    df_unique = pd.DataFrame(columns=['Column_name','Data_type', 'Number_of_unique','Number_of_missing', 'Percentage_of_missing', 'Unique_values'])

    # loop through the columns in the other dataframe
    for col in df.columns:
        # get the number of unique values in the column
        num_unique = df[col].nunique()

        # add the unique values as a list to the 'Unique_values' column if num_unique <= 5
        if num_unique <= 15:
            unique_vals = list(df[col].unique())
        else:
            unique_vals = "More than 15 unique values"

        # get the data type of the column
        data_type = df[col].dtype

        # count the number of missing values in the column
        num_missing = df[col].isnull().sum()

        # we calculate the percentage of missing value in each varaible
        percent_missing = num_missing / df.shape[0]

        # append a row to the empty dataframe with the column name, number of unique values, unique values, and data type
        df_unique = pd.concat([df_unique,pd.DataFrame([{'Column_name': col, 'Number_of_unique': num_unique, 'Unique_values': unique_vals, 'Data_type':
                                      data_type, 'Number_of_missing': num_missing , 'Percentage_of_missing' : percent_missing}])], ignore_index= True)
    
    return df_unique




def clean_na (df) : 
    """
    This function aims to clean our working dataframe from variable that we considere not useful for our exploration and duplicates. 
    For instance because of a large number of missing value. Moreover, we convert non numeric variable to encoded.
    
    args : 
        > df (pandas dataframe) : original datframe
    output :
        > df_clean (pandas dataframe) 

    """
    df_unique = create_unique(df)
    drop_list = []
    for index, row in df_unique.iterrows():

        label_encoder = LabelEncoder()
        colname = str(row['Column_name'])

        # Suppression des colonnes avec plus de 60% des valeurs manquantes
        if row['Percentage_of_missing'] > 0.6 : 
            try:
                df.drop(colname, axis=1, inplace=True)
                drop_list.append(colname)

            except KeyError:
                print(f"Column '{colname}' not found in DataFrame.")

        elif df[colname].dtype == 'O':  # Check if the dtype is 'object' (non-numeric)
            colname = str(row['Column_name'])
            df[str(colname) + '_encoded'] = label_encoder.fit_transform(df[colname].astype(str))

    print ('The list of variables deleted is : ' + str(drop_list))
    
    df = df.drop_duplicates(subset='N°DPE')

    return df





def create_energy_plots(dataframe, x_variable, y_variable):
    ''' fonction permettant de creer plusieurs graphiques pour la description d'une variable'''
    sns.set(style="whitegrid")
    fig, axes = plt.subplots(2, 2, figsize=(10, 9))

    # Graphique 1: Histogramme avec estimation de la densité
    sns.histplot(dataframe[x_variable], kde=True, color='skyblue', ax=axes[0, 0])
    axes[0, 0].set_title(f'Distribution de {x_variable}')

    # Graphique 2: Boîte à moustaches (Boxplot)
    sns.boxplot(x=dataframe[x_variable], color='lightblue', ax=axes[0, 1])
    axes[0, 1].set_title(f'Boîte à moustaches de {x_variable}')

    # Graphique 3: Violin Plot
    sns.violinplot(x=dataframe[x_variable], color='lightgreen', ax=axes[1, 0])
    axes[1, 0].set_title(f'Violin Plot de {x_variable}')

    # Graphique 4: Diagramme de dispersion avec régression linéaire
    sns.regplot(x=dataframe[x_variable], y=dataframe[y_variable], scatter_kws={'alpha': 0.3}, color='salmon', ax=axes[1, 1])
    axes[1, 1].set_title(f'Relation entre {x_variable} et {y_variable}')

    plt.tight_layout()
    plt.show()





def pieplot_chauffage_interact(bd_dpe):
    ''' Cette fonction permet de tracer un digramme ciruclaire interactif des types d'energies : 
            - pour le chauffage
            - pour les ECS'''

    comptage_type_chauffage = bd_dpe['Type_énergie_principale_chauffage'].value_counts()
    comptage_type_ECS = bd_dpe['Type_énergie_principale_ECS'].value_counts()

    pourcentages_chauffage = (comptage_type_chauffage / len(bd_dpe)) * 100
    pourcentages_ECS = (comptage_type_ECS / len(bd_dpe)) * 100

    seuil = 3
    autres_chauffage = pourcentages_chauffage[pourcentages_chauffage < seuil].sum()
    autres_ECS = pourcentages_ECS[pourcentages_ECS < seuil].sum()

    # Création de nouveaux tableaux pour le graphique avec "Autres"
    nouveaux_pourcentages_chauffage = pourcentages_chauffage[pourcentages_chauffage >= seuil]
    nouveaux_pourcentages_chauffage['Autres'] = autres_chauffage

    nouveaux_pourcentages_ECS = pourcentages_ECS[pourcentages_ECS >= seuil]
    nouveaux_pourcentages_ECS['Autres'] = autres_ECS

    # Création des graphiques
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

    fig_chauffage.update_layout(title_text='Répartition types d\'énergies pour chauffage des logements',width = 1000 )
    fig_ECS.update_layout(title_text='Répartition types d\'énergies pour ECS des logements',width = 1000 )

    fig_chauffage.show()
    fig_ECS.show()




def pieplot_chauffage(bd_dpe):
    """ Cette fonction permet de tracer un digramme ciruclaire interactif des types d'energies : 
        - pour le chauffage
        - pour les ECS 
    """
    
    # répartition des types d'energies de chauffage  des logements : 
    comptage_type_chauffage = bd_dpe['Type_énergie_principale_chauffage'].value_counts()
    comptage_type_ECS = bd_dpe['Type_énergie_principale_ECS'].value_counts() 

    ### REPRESENTATION GRAPHIQUE 
    # Calcul des pourcentages pour chaque type d'énergie
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




def barplot_chauffage(bd_dpe): 
    """
    Fonction qui permet d'afficher un graphique en barre des types d'énergies
    """
    # Comptage pour 'Type_énergie_principale_chauffage'
    comptage_type_chauffage = bd_dpe['Type_énergie_principale_chauffage'].value_counts()
    colors_chauffage = sns.color_palette('Set1')[0:len(comptage_type_chauffage)]

    # Comptage pour 'type_principale_energie_ECS'
    comptage_type_ECS = bd_dpe['Type_énergie_principale_ECS'].value_counts()
    colors_ECS = sns.color_palette('Set2')[0:len(comptage_type_ECS)]

    # Création de la figure avec deux sous-graphiques côte à côte
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Barres pour 'Type_énergie_principale_chauffage'
    ax1.bar(comptage_type_chauffage.index, comptage_type_chauffage, color=colors_chauffage, label='Chauffage')
    ax1.set_title('Répartition des types d\'énergies pour chauffage')
    ax1.set_xticklabels(comptage_type_chauffage.index, rotation=45, ha='right')  # Incliner les noms

    # Barres pour 'type_principale_energie_ECS'
    ax2.bar(comptage_type_ECS.index, comptage_type_ECS, color=colors_ECS, label='ECS', alpha=0.7)
    ax2.set_title('Répartition des types d\'énergies pour ECS')
    ax2.set_xticklabels(comptage_type_ECS.index, rotation=45, ha='right')  # Incliner les noms


    # Ajustements de la mise en page
    plt.tight_layout()

    # Affichage de la figure
    plt.show()


def barplot_chauffage_inter(bd_dpe): 
    """ barplot interactif avec ploty"""

    comptage_type_chauffage = bd_dpe['Type_énergie_principale_chauffage'].value_counts()

    #figure interactive Plotly pour 'Type_énergie_principale_chauffage'
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

    #figure interactive Plotly pour 'type_principale_energie_ECS'
    fig_ECS = px.bar(
        x=comptage_type_ECS.index,
        y=comptage_type_ECS,
        color=comptage_type_ECS.index,
        labels={'x': 'Types d\'énergies', 'y': 'Nombre d\'occurrences'},
        title='Répartition des types d\'énergies pour ECS'
    )
    fig_ECS.update_layout(xaxis=dict(tickangle=-45, tickmode='array', tickvals=list(comptage_type_ECS.index)))
    pyo.init_notebook_mode(connected=True)
    pyo.iplot(fig_chauffage)
    pyo.iplot(fig_ECS)
