import numpy as np
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join("./scripts/")))
from logger import logger

class CleanTelco:
    
    def convert_to_datetime(self, df: pd.DataFrame, col_name) -> pd.DataFrame:
        try:
            #Converts col_name's type to datetime 
            df[col_name] = pd.to_datetime(df[col_name], errors='coerce')
            logger.info('Converted to datetime')
        except Exception as e:
            logger.error(e)
        return df
    
    def convert_to_integer(self, df: pd.DataFrame, col_name)-> pd.DataFrame:
        try:
            #Converts col_name's type to int
            df[col_name] = df[col_name].astype("int64")
            logger.info('Converted to integer')
        except Exception as e:
            logger.error(e)
        return df
    
    def convert_to_string(self,  df: pd.DataFrame, col_name) -> pd.DataFrame:
        try:
            #Converts col_name's type to string
            df[col_name] = df[col_name].astype("string")
            logger.info('Converted to string')
        except Exception as e:
            logger.error(e)
        return df

    def drop_duplicate(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            #Drop duplicate rows
            df = df.drop_duplicates()
            logger.info('Dropped duplicates')
        except Exception as e:
            logger.error(e)
        return df

    def drop_column(self, df: pd.DataFrame, col_name) -> pd.DataFrame:
        try:
            #Drop column 'col_name'
            df.drop([col_name], axis=1, inplace=True)
            logger.info('Drop column')
        except Exception as e:
            logger.error(e)
        return df

    def get_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            #Get Missing value percentage of columns
            percent_missing = df.isnull().sum() * 100 / len(df)
            missing_value_df = pd.DataFrame({'column_name': df.columns,
                                            'percent_missing': percent_missing})

            missing_value_df.sort_values('percent_missing', inplace=True)
            logger.info('Get missing values')
        except Exception as e:
            missing_value_df = None
            logger.error(e)
        return missing_value_df

    def fix_missing_ffill(self,  df: pd.DataFrame, col_name) -> pd.DataFrame:
        try:
            #Fill missing values using forward filling method
            df[col_name] = df[col_name].fillna(method='ffill')
            logger.info('ffil fix missing')
        except Exception as e:
            logger.error(e)
        return df

    def fix_missing_bfill(self,  df: pd.DataFrame, col_name) -> pd.DataFrame:
        try:
            #Fill missing values using backward filling method
            df[col_name] = df[col_name].fillna(method='bfill')
            logger.info('bfill fix missing')
        except Exception as e:
            logger.error(e)
        return df

    def fix_missing_value(self,  df: pd.DataFrame, col_name, value) -> pd.DataFrame:
        try:
            #Fill missing values with a given value
            df[col_name] = df[col_name].fillna(value)
            logger.info('Fix missing value')
        except Exception as e:
            logger.error(e)
        return df

    def fix_missing_median(self,  df: pd.DataFrame, col_name) -> pd.DataFrame:
        try:
            #Fill missing values using col_name's median
            df[col_name] = df[col_name].fillna(df[col_name].median())
            logger.info('Fixed with median')
        except Exception as e:
            logger.error(e)
        return df

    def get_row_nan_percentage(self,  df: pd.DataFrame) -> pd.DataFrame:
        try:
            #Get Nan Row Percentage
            rows_with_nan = [index for index,
                            row in df.iterrows() if row.isnull().any()]
            percentage = (len(rows_with_nan) / df.shape[0]) * 100
            logger.info('Row nan percentage')
        except Exception as e:
            percentage = None
            logger.error(e)
        return percentage

    def fix_outliers(self, df: pd.DataFrame):
        try:
            #Replace Outlier values
            for col in df.select_dtypes('float64').columns.tolist():
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower = Q1 - (IQR * 1.5)
                upper = Q3 + (IQR * 1.5)

                df[col] = np.where(df[col] > upper, upper, df[col])
                df[col] = np.where(df[col] < lower, lower, df[col])
                logger.info('Fix outliers')
        except Exception as e:
            logger.error(e)
        return df





