import numpy as np
import pandas as pd


class CleanTelco:
    
    def convert_to_datetime(self, df: pd.DataFrame, col_name) -> pd.DataFrame:
        #Converts col_name's type to datetime 
        df[col_name] = pd.to_datetime(df[col_name], errors='coerce')
        
        return df
    
    def convert_to_integer(self, df: pd.DataFrame, col_name)-> pd.DataFrame:
        #Converts col_name's type to int
        df[col_name] = df[col_name].astype("int64")
        
        return df
    
    def convert_to_string(self,  df: pd.DataFrame, col_name) -> pd.DataFrame:
        #Converts col_name's type to string
        df[col_name] = df[col_name].astype("string")

        return df

    def drop_duplicate(self, df: pd.DataFrame) -> pd.DataFrame:
        #Drop duplicate rows
        df = df.drop_duplicates()

        return df

    def drop_column(self, df: pd.DataFrame, col_name) -> pd.DataFrame:
        #Drop column 'col_name'
        df.drop([col_name], axis=1, inplace=True)

        return df

    def get_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        #Get Missing value percentage of columns
        percent_missing = df.isnull().sum() * 100 / len(df)
        missing_value_df = pd.DataFrame({'column_name': df.columns,
                                         'percent_missing': percent_missing})

        missing_value_df.sort_values('percent_missing', inplace=True)
        
        return missing_value_df

    def fix_missing_ffill(self,  df: pd.DataFrame, col_name) -> pd.DataFrame:
        #Fill missing values using forward filling method
        df[col_name] = df[col_name].fillna(method='ffill')
        
        return df

    def fix_missing_bfill(self,  df: pd.DataFrame, col_name) -> pd.DataFrame:
        #Fill missing values using backward filling method
        df[col_name] = df[col_name].fillna(method='bfill')
        
        return df

    def fix_missing_value(self,  df: pd.DataFrame, col_name, value) -> pd.DataFrame:
        #Fill missing values with a given value
        df[col_name] = df[col_name].fillna(value)
        
        return df

    def fix_missing_median(self,  df: pd.DataFrame, col_name) -> pd.DataFrame:
        #Fill missing values using col_name's median
        df[col_name] = df[col_name].fillna(df[col_name].median())
        
        return df

    def get_row_nan_percentage(self,  df: pd.DataFrame) -> pd.DataFrame:
        #Get Nan Row Percentage
        rows_with_nan = [index for index,
                         row in df.iterrows() if row.isnull().any()]
        percentage = (len(rows_with_nan) / df.shape[0]) * 100
        
        return percentage

    def fix_outliers(self, df: pd.DataFrame):
        #Replace Outlier values
        for col in df.select_dtypes('float64').columns.tolist():
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - (IQR * 1.5)
            upper = Q3 + (IQR * 1.5)

            df[col] = np.where(df[col] > upper, upper, df[col])
            df[col] = np.where(df[col] < lower, lower, df[col])

        return df





