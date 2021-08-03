# Create a function to merge all the csv in one
import os, glob
import pandas as pd


def union_csv(carpeta='data'):
    all_files = glob.glob(os.path.join(carpeta, "*.csv"))
    df_from_each_file = (pd.read_csv(f) for f in all_files)
    df_merged   = pd.concat(df_from_each_file, ignore_index=True)
    filepath = os.path.join(carpeta, f'merge_{carpeta}.csv')
    df_merged.to_csv(filepath)


union_csv(carpeta='data_imdb')