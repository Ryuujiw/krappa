import pandas as pd

data = pd.read_csv('data.csv')

data.head()

krappa = data['reactions']
candidates = data.loc[krappa == krappa.max()]