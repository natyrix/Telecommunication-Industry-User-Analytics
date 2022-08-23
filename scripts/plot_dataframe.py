import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class PlotDataFrame:
    def plotly_pie(self, df, column, limit=None):
        a = pd.DataFrame({'count': df.groupby([column]).size()}).reset_index()
        a = a.sort_values("count", ascending=False)
        if limit:
            a.loc[a['count'] < limit, column] = f'Other {column}s'
        fig = px.pie(a, values='count', names=column, title=f'Distribution of {column}s', width=800, height=500)
        fig.show()

    def plotly_hist(self, df, column, color=['cornflowerblue']):
        fig = px.histogram(
                df,
                x=column,
                marginal='box',
                color_discrete_sequence=color,
                title=f'Distribution of {column}')
        fig.update_layout(bargap=0.01)
        fig.show()
    
    def hist(self, df:pd.DataFrame, column:str, color:str='cornflowerblue')->None:
        sns.displot(data=df, x=column, color=color, kde=True, height=6, aspect=2)
        plt.title(f'Distribution of {column}', size=20, fontweight='bold')
        plt.show()

    def count(self, df:pd.DataFrame, column:str) -> None:
        plt.figure(figsize=(12, 7))
        sns.countplot(data=df, x=column)
        plt.title(f'Distribution of {column}', size=20, fontweight='bold')
        plt.show()

    def bar(self, df:pd.DataFrame, x_col:str, y_col:str, title:str, xlabel:str, ylabel:str)->None:
        plt.figure(figsize=(12, 7))
        sns.barplot(data = df, x=x_col, y=y_col)
        plt.title(title, size=20)
        plt.xticks(rotation=75, fontsize=14)
        plt.yticks( fontsize=14)
        plt.xlabel(xlabel, fontsize=16)
        plt.ylabel(ylabel, fontsize=16)
        plt.show()

    def plotly_multi_hist(self, sr, rows, cols, title_text, subplot_titles):
        fig = make_subplots(rows=rows, cols=cols, subplot_titles=subplot_titles)
        for i in range(rows):
            for j in range(cols):
                x = ["-> " + str(i) for i in sr[i+j].index]
                fig.add_trace(go.Bar(x=x, y=sr[i+j].values ), row=i+1, col=j+1)
        fig.update_layout(showlegend=False, title_text=title_text)
        fig.show()

    def plotly_scatter(self, df, x_col, y_col, marker_size, hover=[]):
        fig = px.scatter(
                df,
                x=x_col,
                y=y_col,
                opacity=0.8,
                hover_data=hover,
                title=f'{x_col} vs. {y_col}')
        fig.update_traces(marker_size=marker_size)
        fig.show()

    

    def scatter(self, df: pd.DataFrame, x_col: str, y_col: str) -> None:
        plt.figure(figsize=(12, 7))
        sns.scatterplot(data = df, x=x_col, y=y_col)
        plt.title(f'{x_col} Vs. {y_col}\n', size=20)
        plt.xticks(fontsize=14)
        plt.yticks( fontsize=14)
        plt.show()

    def p_hist(sr):
        x = ["Id: " + str(i) for i in sr.index]
        fig = px.histogram(x=x, y=sr.values)
        fig.show()
    
    def heatmap(self, df:pd.DataFrame, title:str, cmap='Reds')->None:
        plt.figure(figsize=(13, 7))
        sns.heatmap(df, annot=True, cmap=cmap, vmin=0, vmax=1, fmt='.2f', linewidths=.7, cbar=True )
        plt.title(title, size=18, fontweight='bold')
        plt.show()

    def box(self, df:pd.DataFrame, x_col:str, title:str) -> None:
        plt.figure(figsize=(12, 7))
        sns.boxplot(data = df, x=x_col)
        plt.title(title, size=20)
        plt.xticks(rotation=75, fontsize=14)
        plt.show()

    def box_multi(self, df:pd.DataFrame, x_col:str, y_col:str, title:str) -> None:
        plt.figure(figsize=(12, 7))
        sns.boxplot(data = df, x=x_col, y=y_col)
        plt.title(title, size=20)
        plt.xticks(rotation=75, fontsize=14)
        plt.yticks( fontsize=14)
        plt.show()

    