import math
import sys
import copy

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib import colors as mcolors
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.model_selection import RepeatedStratifiedKFold

#
from sklearn.model_selection import train_test_split
import numpy as np
#

#from src.reader.columns import symptoms_name_dict
#from src.reader.dir import LEUKEMIA_MASTER_PATH

sys.path.append('C:/Users/writh/Desktop/leukemia-knn/src')
from reader.columns import symptoms_name_dict
from reader.dir import LEUKEMIA_MASTER_PATH

leukemia_data = pd.read_csv(LEUKEMIA_MASTER_PATH)
leukimia_full = pd.read_csv(LEUKEMIA_MASTER_PATH)
#print(leukimia_full)

leukemia_data.drop('class', axis=1, inplace=True)
leukemia_data.rename(columns=symptoms_name_dict, inplace=True)
leukimia_full.rename(columns=symptoms_name_dict, inplace=True)
#print(leukimia_full['class'])

clusters = 10
kmeans = KMeans(n_clusters=clusters)
kmeans.fit(leukemia_data)
#print(kmeans.labels_)

#

# Split data randomly in two. One group for training and one for testing
#leukemia_train, leukemia_test = train_test_split(leukemia_data, test_size=0.5, random_state=42)
leuk_class = leukimia_full.iloc[:,20:21].values
leuk_rest = leukimia_full.iloc[:,0:20].values


rskf = RepeatedStratifiedKFold(n_splits=2, n_repeats=10, random_state=36851234)
for train_index, test_index in rskf.split(leuk_rest, leuk_class):
    #print("TRAIN:", train_index, "TEST:", test_index, sep="\n")
    X_train, X_test = leuk_rest[train_index], leuk_rest[test_index]
    y_train, y_test = leuk_class[train_index], leuk_class[test_index]

#

pca = PCA(3)
pca.fit(leukemia_data)
pca_data = pd.DataFrame(pca.transform(leukemia_data))

''' 
Generating different colors in ascending order  of their hsv values
'''

colors = list(zip(*sorted((
    tuple(mcolors.rgb_to_hsv(
        mcolors.to_rgba(color)[:3])), name)
            for name, color in dict(
                mcolors.BASE_COLORS, **mcolors.CSS4_COLORS
).items())))[1]

# number of steps taken to generate n(clusters) colors
skips = math.floor(len(colors[5: -5]) / clusters)
cluster_colors = colors[5: -5: skips]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(pca_data[0], pca_data[1], pca_data[2],
           c=list(map(lambda label: cluster_colors[label],
                      kmeans.labels_)))

str_labels = list(map(lambda label: '% s' % label, kmeans.labels_))

list(map(lambda data1, data2, data3, str_label:
         ax.text(data1, data2, data3, s=str_label, size=16.5,
                 zorder=20, color='k'), pca_data[0], pca_data[1],
         pca_data[2], str_labels))

plt.show()
sns.set(rc={'figure.figsize': (20, 10)})
sns.heatmap(leukemia_data.corr(), annot=True)
plt.show()

from matplotlib import cm

# generating correlation data
df = leukemia_data.corr()
df.index = range(0, len(df))
df.rename(columns=dict(zip(df.columns, df.index)), inplace=True)
df = df.astype(object)

''' Generating coordinates with  
corresponding correlation values '''
for i in range(0, len(df)):
    for j in range(0, len(df)):
        if i != j:
            df.iloc[i, j] = (i, j, df.iloc[i, j])
        else:
            df.iloc[i, j] = (i, j, 0)

df_list = []

# flattening dataframe values
for sub_list in df.values:
    df_list.extend(sub_list)

# converting list of tuples into trivariate dataframe
plot_df = pd.DataFrame(df_list)

fig = plt.figure()
ax = Axes3D(fig)

# plotting 3D trisurface plot
ax.plot_trisurf(plot_df[0], plot_df[1], plot_df[2],
                cmap=cm.jet, linewidth=0.2)

plt.show()