import pandas as pd
import seaborn as sns

def correlation(df):
    corr = df.corr()
    corr.style.background_gradient(cmap='coolwarm')
    return corr

def scatterplot(data,x,y,var):
    sns.set(rc={"figure.figsize":(5, 5)})
    sns.scatterplot(data=data, x=x, y=y, hue=var)

def histplot(data,x,bins=30,binwidth=3):
    sns.histplot(data=data, x=x, bins=bins, binwidth=binwidth)

#Fonction qui permet d’explorer les données
def create_unique(df):       
    df_unique = pd.DataFrame(columns=['Column_name','Data_type', 'Number_of_unique','Number_of_missing', 'Unique_values'])
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
        # append a row to the empty dataframe with the column name, number of unique values, unique values, and data type
        df_unique = pd.concat([df_unique,pd.DataFrame([{'Column_name': col, 'Number_of_unique': num_unique, 'Unique_values': unique_vals, 'Data_type':
                                      data_type, 'Number_of_missing': num_missing}])])
    return df_unique