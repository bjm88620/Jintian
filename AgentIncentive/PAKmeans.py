import pandas as pd
import numpy as np
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from sklearn.cluster import KMeans

data = pd.read_excel(u'/Users/haru/Documents/zhaowo/AgentIncentive/PCA_Resu.xlsx')
df = pd.DataFrame(data['Reflec'])
#data = data.drop(['策划师名称'],axis = 1)
clf =  KMeans(n_clusters=2, random_state=0).fit(df)

L = clf.labels_
L0 = [i for i,v in enumerate(L) if v==0]
L1 = [i for i,v in enumerate(L) if v==1]
print("The Cluster centers are :%s"%clf.cluster_centers_)
print("The total distance is %s"%clf.inertia_)
print("The number of elements in cluster 1 is %s"%np.sum(L==0))
print("The number of elements in cluster 1 is %s"%np.sum(L==1))

#tb = pd.concat([],axis =1 )
ol = data.columns.tolist()
new = ['cu']
tb = pd.concat([data,pd.DataFrame(L)],axis =1)
tb.columns = ol + new
tb.to_excel(u'/Users/haru/Documents/zhaowo/AgentIncentive/PCA_Resu2.xlsx')
# writer = pd.ExcelWriter(u'/Users/haru/Documents/zhaowo/PrincipalAgent/PCA_Resu.xlsx')
# tb.to_excel(writer,'Sheet2')
# writer.save()
# print(tb.head())
# print(tb.info())


