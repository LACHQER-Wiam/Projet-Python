import pandas as pd
import seaborn as sns
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
import matplotlib.pyplot as plt


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
    return pd.get_dummies(data, columns=columns_to_encode)


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