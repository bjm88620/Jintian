import pandas as pd
import numpy as np

data = pd.read_excel(u'/Users/haru/Documents/zhaowo/AgentIncentive/Cost.xlsx')
data = data.reset_index()
F = data['Cost']
e = data['Reflec']


sep_tb = pd.pivot_table(data,index = ['cu'],values = ['Reflec'],aggfunc = np.mean)
sep_tb.reset_index()
e_upper = sep_tb['Reflec'].loc[1]   #有效率的e的平均
e_lower = sep_tb['Reflec'].loc[0]   #无效率的e的平均


zero_tb = data[(data['cu']==0)]
ones_tb = data[(data['cu']==1)]

e_eff = ones_tb['Reflec']
F_eff = ones_tb['Cost']
e_ineff = zero_tb['Reflec']
F_ineff = zero_tb['Cost']
S = data['完成订单总金额']

class PA:

    def __init__(self, F, e, e_upper, e_lower, S, e_ineff, e_eff, F_ineff, F_eff, data):
        self.F = F
        self.e = e
        self.e_upper = e_upper
        self.e_lower = e_lower
        self.S = S
        self.e_ineff = e_ineff
        self.e_eff = e_eff
        self.F_ineff = F_ineff
        self.F_eff = F_eff
        self.data = data



    def Transfer(self):
        TransferEff = (self.e_eff * self.F_eff + (self.e_eff - self.e_lower) * self.F_eff + self.F_eff)
        UtilityEff = TransferEff - (self.e_upper * self.F_eff + self.F_eff)
        TransferEff = TransferEff.tolist()
        UtilityEff = UtilityEff.tolist()
        Index_eff = ones_tb['index'].tolist()
        Eff = list(zip(Index_eff, TransferEff))
        Eff2= list(zip(Index_eff, UtilityEff))

        TransferIneff = self.e_ineff * self.F_ineff + self.F_ineff
        UtilityIneff = TransferIneff - (self.e_lower * self.F_ineff + self.F_ineff)
        TransferIneff = TransferIneff.tolist()
        Index_ineff = zero_tb['index'].tolist()
        Ineff = list(zip(Index_ineff, TransferIneff))
        Ineff2 = list(zip(Index_ineff, UtilityIneff))

        Transfer = Eff + Ineff
        Transfer = pd.DataFrame(Transfer)
        Transfer.columns = ['Index', 'Transfer']

        UtilityE = Eff2 + Ineff2
        UtilityE = pd.DataFrame(UtilityE)
        UtilityE.columns = ['Index', 'UtilityE']

        data1 = data.merge(Transfer, left_on='index', right_on='Index', how='outer')
        data2 = data1.merge(UtilityE, left_on='index', right_on='Index', how='outer')
        data2 = data2.sort_values(by='index')
        return data2['Transfer'], data2['UtilityE']

    def Cost(self):
        Cost = self.e + self.F
        return Cost


    def Utility(self):
        Utility = self.Transfer()[0] - self.Cost()
        return Utility


    def PrincipalProfit(self):
        TransferSum = self.Transfer()[0].sum()
        NewCost = self.e * self.Cost()
        NewCostSum = NewCost.sum()
        FSum = self.F.sum()
        SSum = self.S.sum()
        PrincipalProfit =  FSum + SSum - (2 * TransferSum) + (2 * NewCost)
        return PrincipalProfit



    def main(self):
        TransferList = []
        TransferRaw = self.Transfer()[0].tolist()
        UtilityE = self.Transfer()[1].tolist()
        for i,v in enumerate(TransferRaw):
            if (self.Utility()[i] > 0 and (self.Utility()[i] - UtilityE[i]) > 0):
                TransferList.append(v)
            else:
                TransferList.append(0)


        TransferList = pd.DataFrame(TransferList)
        TransferList = TransferList.reset_index()
        TransferList.columns = ['index','TransferList']
        data3 = data.merge(TransferList, left_on='index', right_on='index', how='outer')
        data3.to_excel(u'/Users/haru/Documents/zhaowo/AgentIncentive/Result.xlsx')
        return TransferList


pa = PA(F, e, e_upper, e_lower, S, e_ineff, e_eff, F_ineff, F_eff, data)
pa.main()
