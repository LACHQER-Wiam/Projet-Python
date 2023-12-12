import pandas as pd
import seaborn as sns
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer

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

