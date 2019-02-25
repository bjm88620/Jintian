import pandas as pd
import numpy as np
from sklearn.preprocessing import minmax_scale

data = pd.read_excel(u'/Users/haru/Documents/zhaowo/AgentIncentive/PCA_Resu2.xlsx')
s = data['完成订单总金额']
N = minmax_scale(s)

Cost = []
a = 0
for i in range(len(N)):
    a = 100+200+100+30+50+50+400+50+100+200+N[i]*(100+50+400+200+170+950+100+50+50+200+400+250+100+300)
    Cost.append(a)

Cost = pd.DataFrame(Cost)
Cost.columns = ['Cost']
data = pd.concat([data,Cost],axis =1)
data.to_excel(u'/Users/haru/Documents/zhaowo/AgentIncentive/Cost.xlsx')

