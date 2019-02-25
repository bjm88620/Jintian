import pandas as pd
import numpy as np
from sklearn.decomposition import pca
from sklearn.preprocessing import minmax_scale
from sklearn.cluster import KMeans


df = pd.read_excel(u'/Users/haru/Documents/zhaowo/AgentIncentive/Factors.xlsx')

df = df.dropna(axis = 0)

df['婚期'] = pd.to_datetime(df['婚期'])
df['year'] = df['婚期'].dt.year
df['month'] = df['婚期'].dt.month

l1 = ['婚礼ID','尾款前审美能力分数','尾款前形象气质分数','尾款前效果还原度分数','首付出方案速度']
data = df[l1]
data = data.reset_index().drop('index',axis = 1)
data_temp = data.iloc[:,1:]
#model = pca.PCA(n_components=1).fit(data_temp)
#Z = pd.DataFrame(model.transform(data_temp))
#Z.columns = ['e']
df['e'] = (df['尾款前审美能力分数']+df['尾款前形象气质分数']+df['尾款前效果还原度分数']+df['首付出方案速度'])/4

N = minmax_scale(df['e'])
N = pd.DataFrame(N)
N.columns = ['Reflec']
data = pd.concat([data,N],axis =1)
data = data[['婚礼ID','Reflec']]
df = df.join(data.set_index('婚礼ID'),on='婚礼ID')
df = df.reset_index()

#判断scale的大小
dataprevious = pd.read_excel(u'/Users/haru/Documents/zhaowo/AgentIncentive/Jan_Resu.xlsx')
max = dataprevious['raw2'].max()
min = dataprevious['raw2'].min()
if (max > 200):
    scale1 = 200/max
else:
    scale1 = 1
if (min < -200):
    scale2 = 200/abs(min)
else:
    scale2 = 1
if (scale1 > scale2):
    scale = scale2
else:
    scale = scale1
print(scale)

max = dataprevious['raw3'].max()
min = dataprevious['raw3'].min()
if (max > 20):
    scale11 = 20/max
else:
    scale11 = 1
if (min < -20):
    scale21 = 20/abs(min)
else:
    scale21 = 1
if (scale11 > scale21):
    scale_ = scale21
else:
    scale_ = scale11
print(scale_)



#方法1

# d_p = pd.pivot_table(df,index = ['year','month'],values = ['e'],aggfunc = np.mean)
# d_p= d_p.reset_index()
# n1 = d_p['e'][(d_p['year'] == 2018) & (d_p['month'] == 6)]
# n2 = d_p['e'][(d_p['year'] == 2018) & (d_p['month'] == 7)]
# n3 = d_p['e'][(d_p['year'] == 2018) & (d_p['month'] == 8)]
# n4 = d_p['e'][(d_p['year'] == 2018) & (d_p['month'] == 9)]
# n5 = d_p['e'][(d_p['year'] == 2018) & (d_p['month'] == 10)]
# n6 = d_p['e'][(d_p['year'] == 2018) & (d_p['month'] == 11)]
# n7 = d_p['e'][(d_p['year'] == 2018) & (d_p['month'] == 12)]
# n8 = d_p['e'][(d_p['year'] == 2019) & (d_p['month'] == 1)]
#
#
# data_temp1 = df[(df['year'] == 2018) & (df['month'] == 12)]
# data_temp1['Avg_e'] = n6.tolist()[0]
# data_temp1['Diff_e'] = data_temp1['e'] - data_temp1['Avg_e']
# N = minmax_scale(data_temp1['e'])
# N = pd.DataFrame(N)
# N.columns = ['Reflec']
#data_temp1['奖惩'] = data_temp1['服务费'] * data_temp1['Diff_e']

#方法2

d_p = pd.pivot_table(df,index = ['year','month'],values = ['Reflec'],aggfunc = np.mean)
d_p= d_p.reset_index()
n1 = d_p['Reflec'][(d_p['year'] == 2018) & (d_p['month'] == 6)]
n2 = d_p['Reflec'][(d_p['year'] == 2018) & (d_p['month'] == 7)]
n3 = d_p['Reflec'][(d_p['year'] == 2018) & (d_p['month'] == 8)]
n4 = d_p['Reflec'][(d_p['year'] == 2018) & (d_p['month'] == 9)]
n5 = d_p['Reflec'][(d_p['year'] == 2018) & (d_p['month'] == 10)]
n6 = d_p['Reflec'][(d_p['year'] == 2018) & (d_p['month'] == 11)]
n7 = d_p['Reflec'][(d_p['year'] == 2018) & (d_p['month'] == 12)]
n8 = d_p['Reflec'][(d_p['year'] == 2019) & (d_p['month'] == 1)]

data_temp1 = df[(df['year'] == 2019) & (df['month'] == 2)]
N = minmax_scale(data_temp1['e'])
N = pd.DataFrame(N)
N.columns = ['Reflec']
data_temp1['Avg_Reflec'] = n8.tolist()[0]
data_temp1['Diff_Reflec'] = data_temp1['Reflec'] - data_temp1['Avg_Reflec']
data_temp1['raw2'] = ((data_temp1['服务费'] * data_temp1['Diff_Reflec']))
data_temp1['奖惩2'] = ((data_temp1['服务费'] * data_temp1['Diff_Reflec']))*scale


#方法3

#订单按努力程度分类
df2 = pd.DataFrame(df['e'])
clf =  KMeans(n_clusters=2, random_state=0).fit(df2)

L = clf.labels_
L0 = [i for i,v in enumerate(L) if v==0]
L1 = [i for i,v in enumerate(L) if v==1]
print("The Cluster centers are :%s"%clf.cluster_centers_)
print("The total distance is %s"%clf.inertia_)
print("The number of elements in cluster 0 is %s"%np.sum(L==0))
print("The number of elements in cluster 1 is %s"%np.sum(L==1))

ol = df.columns.tolist()
new = ['cu']
df = pd.concat([df,pd.DataFrame(L)],axis =1)
df.columns = ol + new


#个人成本：cost
N = minmax_scale(df['总订单金额'])
Cost = []
a = 0
for i in range(len(N)):
    a = 100+200+100+30+50+50+400+50+100+200+N[i]*(100+50+400+200+170+950+100+50+50+200+400+250+100+300)-500
    Cost.append(a)
Cost = pd.DataFrame(Cost)
Cost.columns = ['Cost']
df = pd.concat([df,Cost],axis =1)


#奖惩计算过程
sep_tb = pd.pivot_table(df,index = ['cu'],values = ['Reflec'],aggfunc = np.mean)
sep_tb.reset_index()

e_upper = sep_tb['Reflec'].loc[1]   #有效率的e的平均
e_lower = sep_tb['Reflec'].loc[0]   #无效率的e的平均

zero_tb = df[(df['cu']==0)]
ones_tb = df[(df['cu']==1)]

e_eff = ones_tb['Reflec']
F_eff = ones_tb['Cost']
e_ineff = zero_tb['Reflec']
F_ineff = zero_tb['Cost']


TransferEff = (e_eff * F_eff + (e_eff - e_lower) * F_eff + F_eff)
TransferEff = TransferEff.tolist()
Index_eff = ones_tb['index'].tolist()
Eff = list(zip(Index_eff, TransferEff))


TransferIneff =  F_ineff - (e_ineff * F_ineff)
TransferIneff = TransferIneff.tolist()
Index_ineff = zero_tb['index'].tolist()
Ineff = list(zip(Index_ineff, TransferIneff))


Transfer = Eff + Ineff
Transfer = pd.DataFrame(Transfer)
Transfer.columns = ['Index', 'Transfer']


data = df.join(Transfer.set_index('Index'), on='index')
data = data.sort_values(by='index')
data['raw3'] = (data['服务费'] - data['Transfer'])
data['奖惩3'] = (data['服务费'] - data['Transfer'])*scale_
dt = data[['婚礼ID','Transfer','raw3','奖惩3']]

data_temp1 = data_temp1.join(dt.set_index('婚礼ID'),on='婚礼ID')

data_temp1.to_excel(u'/Users/haru/Documents/zhaowo/AgentIncentive/Feb_Resu.xlsx')