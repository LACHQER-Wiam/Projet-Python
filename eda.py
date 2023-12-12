import pandas as pd
import seaborn as sns

def correlation(df):
    corr = df.corr()
    corr.style.background_gradient(cmap='coolwarm')
    return corr

def scatterplot(data,x,y,var):
    sns.scatterplot(data=data, x=x, y=y, hue=var)

def histplot(data,x,bins=30,binwidth=3):
    sns.histplot(data=data, x=x, bins=bins, binwidth=binwidth)

#def lineplot(data, colonnes):
     
def boxplot(data, variables):
    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(15, 8))
    axes = axes.flatten()
    for i in range(len(variables)):
        sns.boxplot(x=data[variables[i]], ax=axes[i], color='skyblue')
        #axes[i].set_title(variables[i])
    # Masquer le subplot vide 
    if len(axes) > 5:
        for i in range(5, len(axes)):
            fig.delaxes(axes[i])
    plt.tight_layout()
    plt.show()



#Fonction qui permet d’explorer les données
def create_unique(df):       
    df_unique = pd.DataFrame(columns=['Column_name','Data_type', 'Number_of_unique','Number_of_missing', 'Unique_values'])
    for col in df.columns:
        num_unique = df[col].nunique()
        if num_unique <= 15:
            unique_vals = list(df[col].unique())
        else:
            unique_vals = "More than 15 unique values"
        data_type = df[col].dtype
        num_missing = df[col].isnull().sum()
        df_unique = pd.concat([df_unique,pd.DataFrame([{'Column_name': col, 'Number_of_unique': num_unique, 'Unique_values': unique_vals, 'Data_type':
                                      data_type, 'Number_of_missing': num_missing}])])
    return df_unique
