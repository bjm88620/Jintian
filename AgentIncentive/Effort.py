import pandas as pd
import numpy as np
from sklearn.decomposition import pca
from sklearn.preprocessing import minmax_scale

df = pd.read_excel(u'/Users/haru/Documents/zhaowo/AgentIncentive/Factors.xlsx')
df = df.dropna(axis = 0)
l1 = ['婚礼ID','尾款前审美能力分数','尾款前形象气质分数','尾款前效果还原度分数','首付出方案速度']
data = df[l1]
data = data.reset_index().drop('index',axis = 1)
data_temp = data.iloc[:,1:]

model = pca.PCA(n_components=1).fit(data_temp)
Z = pd.DataFrame(model.transform(data_temp))
Z.columns = ['PCA']
N = minmax_scale(Z)
N = pd.DataFrame(N)
N.columns = ['Reflec']
data = pd.concat([data,Z,N],axis =1)
data = data[['婚礼ID','Reflec']]
df = df.join(data.set_index('婚礼ID'),on='婚礼ID')

df = pd.read_excel(u'/Users/haru/Documents/zhaowo/AgentIncentive/PCA_Resu.xlsx')