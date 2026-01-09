import pandas as pd
import matplotlib.pyplot as plt
from clean import labels

"""
her verður transform/ pivot, csv, plot
"""
def create_pivot_and_export(df):
    df['Breyta_text'] = df['Breyta'].map(labels)
    df_pivot = df.pivot(index='Ár', columns='Breyta_text', values='value')
    df_pivot.to_csv('upplysingataekni_2008-2024.csv')
    return df_pivot

def plot_revenue_trend(df_pivot):
    df_pivot['Rekstrartekjur (mkr)'].plot(title='Rekstrartekjur í upplýsingageiranum')
    plt.savefig('trend.png')
    plt.close()
